from rest_framework import generics


# Create your views here.
from rest_framework.response import Response

from apps.bill.models import BillingSetting
from apps.bill.serializers import BillingSettingSerializer
from restaurant.permissions import DjangoModelPermissionsWithRead


class BillingSettingsRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [DjangoModelPermissionsWithRead]
    serializer_class = BillingSettingSerializer
    queryset = BillingSetting.objects.all()

    def get_object(self):
        return BillingSetting.objects.get_or_create(
            restaurant=self.request.user.profile.restaurant
        )[0]
