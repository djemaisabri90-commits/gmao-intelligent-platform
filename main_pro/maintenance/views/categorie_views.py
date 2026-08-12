# maintenance/views/categorie_views.py

from rest_framework import viewsets
from maintenance.models import Categorie
from maintenance.serializers.categorie_serializer import CategorieSerializer
from rest_framework.permissions import IsAuthenticated

class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = [IsAuthenticated]
