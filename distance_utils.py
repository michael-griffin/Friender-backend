# import geocoder library
from geopy.geocoders import Nominatim
# import distance measuring method
from geopy import distance

# instantiate geolocater - user agent is to let the creator know who is using
geolocator = Nominatim(user_agent="learning_how_toUse")


def get_distance(location_a, location_b):
    """Function for getting distance between geocoded addresses"""
    a = geolocator.geocode(f'{location_a}, USA')
    b = geolocator.geocode(f'{location_b}, USA')

    return round(distance.distance((a.latitude, a.longitude),
                                   (b.latitude, b.longitude)).miles, 1)
