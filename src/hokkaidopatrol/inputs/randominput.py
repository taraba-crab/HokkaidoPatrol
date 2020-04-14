from random import sample
from .. import cities
from .distances import to_distance_dict

def random_select(k):
    sample_cities = sample(cities.keys(), k)
    return [cities[city] for city in sample_cities], to_distance_dict(sample_cities)
