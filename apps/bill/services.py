import io
from lxml import etree
from zeep import Client
import datetime
from zeep.wsse.username import UsernameToken
from apps.bill.adapters import BillToXMLSenderAdapter
from apps.bill.models import BillOrder, BillingSetting
from pathlib import Path
from apps.operations.models import Order
from django.core.files.base import ContentFile
from zeep.wsse.utils import WSU


def save_bill_response(bill: BillOrder):
	content = dict()
	bill.extract_response_zip()
	xml_file = open(bill.response_xml_file.path, 'rb')
	tree = etree.fromstring(xml_file.read())
	standard = '{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}'
	reference = tree.find(f'.//{standard}ReferenceID')
	code = tree.find(f'.//{standard}ResponseCode')
	description = tree.find(f'.//{standard}Description')
	notes = tree.findall(f'.//{standard}Note')
	xml_file.close()
	content['ReferenceID'] = reference.text if reference is not None else None
	content['ResponseCode'] = code.text if code is not None else None
	content['info'] = description.text if description is not None else None
	content['notes'] = [{'note': note.text} for note in notes]
	bill.response_code = content['ResponseCode'] if code is not None else None
	bill.save()
	return content


class Services:

	def __init__(self, settings: BillingSetting):
		self.certificate_settings = settings
		self.bill_wsdl_url = 'https://e-factura.sunat.gob.pe/ol-ti-itcpfegem/billService?wsdl'
		self.consult_wsdl_url = 'https://e-factura.sunat.gob.pe/ol-it-wsconscpegem/billConsultService?wsdl'

	def authenticate(self, wsdl_url: str):
		username = f'{self.certificate_settings.restaurant.ruc}{self.certificate_settings.second_user}'
		password = f'{self.certificate_settings.second_user_password}'
		timestamp_token = WSU.Timestamp()
		today_datetime = datetime.datetime.today()
		expires_datetime = today_datetime + datetime.timedelta(minutes=10)
		timestamp_elements = [
			WSU.Created(today_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")),
			WSU.Expires(expires_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"))
		]
		timestamp_token.extend(timestamp_elements)
		username_token = UsernameToken(username, password, timestamp_token=timestamp_token)
		return Client(wsdl_url, wsse=username_token)

	def send_bill(self, bill: BillOrder):
		bill.write_xml()
		bill.write_zip()
		content = BillToXMLSenderAdapter(bill, self.certificate_settings).build_file()
		bill.send_file.save(bill.filename + '.xml', io.StringIO(content))
		zip_file = bill.zip_file
		file = open(zip_file.path, 'rb')
		data_file = file.read()
		filename = Path(zip_file.path).name
		try:
			response = self.authenticate(wsdl_url=self.bill_wsdl_url).service.sendBill(
				filename,
				data_file
			)
			bill.response_zip_file.save(f'{bill.filename}.zip', ContentFile(response))
			return save_bill_response(bill)
		except Exception as e:
			return {'info': str(e)}
		finally:
			file.close()

	def consult_bill(self, order: Order):
		try:
			request_data = {
				'rucComprobante': f'{self.certificate_settings.restaurant.ruc}',
				'tipoComprobante': f'0{order.payment_document.electronic_document}',
				'serieComprobante': f'{order.serie}',
				'numeroComprobante': f'{order.correlative}'
			}
			response = self.authenticate(wsdl_url=self.consult_wsdl_url).service.getStatus(**request_data)
			return {
				'message': f'{response.statusMessage}',
				'code': f'{response.statusCode}'
			}
		except Exception as e:
			return {'message': str(e)}
