"""
 Описание роутов приложения
"""

import geocatalog.views


main_routes = {
    'regions': {
        'class': geocatalog.views.RegionsView,
        'rules': ['/regions/']
    },
    'region': {
        'class': geocatalog.views.RegionView,
        'rules': ['/regions/<region_id>/']
    },
    'region_cities': {
        'class': geocatalog.views.CitiesView,
        'rules': ['/regions/<region_id>/cities/']
    },
    'city': {
        'class': geocatalog.views.CityView,
        'rules': ['/regions/<region_id>/cities/<city_id>/']
    },
}
