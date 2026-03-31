from rest_framework import serializers
from .models import ArtifactTask

class ArtifactTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtifactTask
        fields = '__all__'
