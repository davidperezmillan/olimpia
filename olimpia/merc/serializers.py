from rest_framework import serializers
from .models import Series


class SeriesListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        data = data.filter(usuario=self.context['request'].user)
        return super(SeriesListSerializer, self).to_representation(data)


class SeriesSerializer(serializers.ModelSerializer):
    
    url = serializers.HyperlinkedIdentityField(
        'series-detail',
        source='id',
        read_only=True)
    
    class Meta:
        model = Series
        fields = ('id','author', 'nombre', 'ep_start', 'ep_end', 'quality','ultima','paussed','skipped', 'url',)




    
