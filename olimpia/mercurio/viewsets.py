from .models import Series
from .serializers import SeriesSerializer
from rest_framework import viewsets

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
# from rest_framework.filters import DjangoFilterBackend


class SeriesViewSet(viewsets.ModelViewSet):
 
    serializer_class = SeriesSerializer
    queryset = Series.objects.all()
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    


 