from rest_framework import serializers

from rural_norte.core.models import Lote


class LoteHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lote
        fields = '__all__'

class LoteModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lote
        fields = '__all__'
