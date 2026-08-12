# predictive/utils/geocode.py
from geopy.geocoders import Nominatim
from maintenance.models import Machine

def enrich_machines_with_coordinates():
    geolocator = Nominatim(user_agent="main_pro")

    for machine in Machine.objects.all():
        if machine.localisation and (machine.latitude is None or machine.longitude is None):
            location = geolocator.geocode(machine.localisation)
            if location:
                machine.latitude = location.latitude
                machine.longitude = location.longitude
                machine.save()


"""
LOCALISATION REELLE
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="gmao_app")
location = geolocator.geocode("Tunis, Tunisie")
print(location.latitude, location.longitude)


"""