import base64
from xml.dom.minidom import Element

import signxml
from django.template.loader import get_template
from lxml import etree
from signxml import XMLSigner


class BillToXMLAdapter:
    # template_name = 'file_bill_xml_order.xml'

    def __init__(self, settings, template_name):
        self.settings = settings
        self.template_name = template_name

    def build_file(self):
        template = get_template(self.template_name)
        content = template.render(self.get_context())
        content_signed = self.sign(content)
        return etree.tostring(content_signed, pretty_print=True, xml_declaration=True, encoding='UTF-8')

    def sign(self, content):
        private_key = self.settings.certificate_private_key.read()
        certificate = self.settings.certificate_pem.read()
        root = etree.fromstring(content.encode())

        signed_root = XMLSigner(
            method=signxml.methods.enveloped,
            signature_algorithm='rsa-sha1',
            digest_algorithm="sha1",
            c14n_algorithm='http://www.w3.org/TR/2001/REC-xml-c14n-20010315'
        ).sign(
            root,
            key=private_key,
            cert=certificate
        )
        self.__move_sign__(root=signed_root)
        verified_data = signxml.XMLVerifier().verify(signed_root, x509_cert=certificate).signed_xml
        return signed_root

    @staticmethod
    def __move_sign__(root: Element):
        signature = root.getchildren()[-1]
        ubl_extension = root.getchildren()[0].getchildren()[0].getchildren()[0]
        ubl_extension.append(signature)

    def get_context(self):
        return {
            'settings': self.settings
        }


class BillOrderToXMLAdapter(BillToXMLAdapter):

    def __init__(self, order, settings):
        template_name = 'file_bill_xml_order.xml'
        current_order = order.order
        if current_order.payment_document.electronic_document == current_order.payment_document.ElectronicDocument.ELECTRONIC_BILL:
            template_name = 'file_bill_xml_order.xml'
        elif current_order.payment_document.electronic_document == current_order.payment_document.ElectronicDocument.TICKET:
            template_name = 'file_invoice_xml_order.xml'
        elif current_order.payment_document.electronic_document == current_order.payment_document.ElectronicDocument.CREDIT_NOTE:
            template_name = 'file_credit_xml_order.xml'
        super(BillOrderToXMLAdapter, self).__init__(settings, template_name)
        self.order = order

    def get_context(self):
        context = super(BillOrderToXMLAdapter, self).get_context()
        context['bill'] = self.order
        return context


class BillToXMLSenderAdapter:

    def __init__(self, bill, settings):
        self.bill = bill
        self.certificate_settings = settings

    def build_file(self):
        template = get_template('file_send_order.xml')
        content = template.render(self.context)
        return content

    @property
    def context(self):
        base64_bytes = base64.b64encode(self.bill.zip_file.read()).decode()
        return {
            'bill': self.bill,
            'settings': self.certificate_settings,
            'base64': base64_bytes
        }
