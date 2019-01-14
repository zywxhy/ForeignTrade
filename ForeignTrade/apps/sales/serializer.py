from rest_framework.serializers import ModelSerializer
from .models import SalesContract


class SalesContractModelSerializer(ModelSerializer):
    class Meta:
        model = SalesContract
        fields = '__all__'
