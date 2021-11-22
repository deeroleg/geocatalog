"""
 Описание роутов приложения
"""

from geocatalog import views


main_routes = {
    'regions': {
        'class': views.RegionsView,
        'rules': ['/regions/']
    },
    'region': {
        'class': views.RegionView,
        'rules': ['/regions/<region_id>/']
    },
    'region_cities': {
        'class': views.CitiesView,
        'rules': ['/regions/<region_id>/cities/']
    },
    'city': {
        'class': views.CityView,
        'rules': ['/regions/<region_id>/cities/<city_id>/']
    },
}
