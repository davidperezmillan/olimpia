from rest_framework import serializers
from .models import Series, Genero


class SeriesListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        data = data.filter(usuario=self.context['request'].user)
        return super(SeriesListSerializer, self).to_representation(data)

class GeneroSerializer(serializers.ModelSerializer):
    # series = SeriesSerializer(many=False, read_only=True)

    url = serializers.HyperlinkedIdentityField(
        'genero-detail',
        source='nombre',
        read_only=True)
    
    
    class Meta:
        model = Genero
        fields = ('id','nombre', 'url',)


class SeriesSerializer(serializers.ModelSerializer):
    genero = GeneroSerializer(many=False, read_only=True)
    
    url = serializers.HyperlinkedIdentityField(
        'series-detail',
        source='id',
        read_only=True)
    
    class Meta:
        model = Series
        fields = ('id', 'nombre', 'ep_start', 'ep_end', 'quality','ultima','paussed','skipped','genero', 'url',)




    
