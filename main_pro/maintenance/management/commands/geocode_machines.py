# maintenance/management/commands/geocode_machines.py
from django.core.management.base import BaseCommand
from predictive.utils.geocode import enrich_machines_with_coordinates

class Command(BaseCommand):
    help = "Ajoute longitude/latitude aux machines via géocodage"

    def handle(self, *args, **kwargs):
        enrich_machines_with_coordinates()
        self.stdout.write(self.style.SUCCESS("Coordonnées mises à jour"))
