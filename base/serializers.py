from rest_framework.serializers import ModelSerializer
from .models import Batch

class BatchSerializer(ModelSerializer):
    class Meta:
        model = Batch
        fields = '__all__'
