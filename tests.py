import unittest
import os
import sys

home = os.environ['PROJECT_HOME']
sys.path.append(home + '/geocatalog/sources/lib')

import json

from geocatalog import create_app, db


class GeoCatalogTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(home + os.environ['CFG_FILE'])
        self.client = self.app.test_client
        self.root_region = {'name': 'Region'}
        self.child_region = {'name': 'Child Region', 'parent_id': 1}
        self.sub_child_region = {'name': 'Child Region', 'parent_id': 2}
        self.root_region_changed = {'name': 'Region edited'}
        self.child_region_changed = {'name': 'Child Region edited', 'parent_id': 2}
        self.empty_region = {'name': ''}
        self.city = {'name': 'City', 'region_id': 1}
        self.city_changed_without_region = {'name': 'City edited'}
        self.city_changed_with_region = {'name': 'City edited', 'region_id': 2}


        with self.app.app_context():
            db.create_all()

    def test_empty_regions_list(self):
        """Проверка, что реггионов нет"""
        res = self.client().get('/regions/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, list())

    def test_region_creation(self):
        """Test API can create a region"""
        res = self.client().post('/regions/', json=self.root_region)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, dict(success=True))

        """Проверка, что возвращается один регион"""
        res = self.client().get('/regions/')
        self.assertEqual(res.status_code, 200)

        data = res.json
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0].get('name'), self.root_region.get('name'))

    def test_region_update(self):
        """Test API can update a region"""
        res = self.client().post('/regions/', json=self.root_region)
        self.assertEqual(res.status_code, 200)

        res = self.client().get('/regions/1/')
        self.assertEqual(res.status_code, 200)

        data = res.json
        self.assertEqual(data.get('name'), self.root_region.get('name'))

        res = self.client().put('/regions/1/', json=self.empty_region)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, dict(success=False, error='Name not specified'))
        
        res = self.client().put('/regions/1/', json=self.root_region_changed)
        self.assertEqual(res.status_code, 200)

        self.assertEqual(res.json, dict(success=True))

        res = self.client().get('/regions/1/')
        self.assertEqual(res.status_code, 200)

        data = res.json
        self.assertEqual(data.get('name'), self.root_region_changed.get('name'))

    def test_region_delete(self):
        """Test API can delete a region"""
        res = self.client().post('/regions/', json=self.root_region)
        self.assertEqual(res.status_code, 200)

        res = self.client().delete('/regions/1/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, dict(success=True))

        res = self.client().get('/regions/1/')
        self.assertEqual(res.status_code, 404)

    def test_child_region_create_update_delete(self):
        """Test API can create, update and delete child region"""
        res = self.client().post('/regions/', json=self.root_region)
        self.assertEqual(res.status_code, 200)

        res = self.client().post('/regions/', json=self.root_region)
        self.assertEqual(res.status_code, 200)

        res = self.client().post('/regions/', json=self.child_region)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, dict(success=True))

        res = self.client().get('/regions/3/')
        self.assertEqual(res.status_code, 200)

        data = res.json
        self.assertEqual(data.get('name'), self.child_region.get('name'))
        self.assertEqual(data.get('parent_id'), self.child_region.get('parent_id'))

        res = self.client().put('/regions/3/', json=self.child_region_changed)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, dict(success=True))

        res = self.client().get('/regions/3/')
        self.assertEqual(res.status_code, 200)

        data = res.json
        self.assertEqual(data.get('parent_id'), self.child_region_changed.get('parent_id'))
        self.assertEqual(data.get('name'), self.child_region_changed.get('name'))

        res = self.client().put('/regions/3/', json=self.root_region)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, dict(success=True))

        res = self.client().get('/regions/3/')
        self.assertEqual(res.status_code, 200)

        data = res.json
        self.assertEqual(data.get('parent_id'), None)
        self.assertEqual(data.get('name'), self.root_region.get('name'))
        
        res = self.client().put('/regions/3/', json=self.child_region_changed)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, dict(success=True))

        res = self.client().delete('/regions/1/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, dict(success=True))

        res = self.client().get('/regions/1/')
        self.assertEqual(res.status_code, 404)
        
    def test_circular_ref_in_regions_updateing_region(self):
        """Test API cant set a circular reference to the parent region"""
        res = self.client().post('/regions/', json=self.root_region)
        self.assertEqual(res.status_code, 200)

        res = self.client().post('/regions/', json=self.child_region)
        self.assertEqual(res.status_code, 200)

        res = self.client().post('/regions/', json=self.sub_child_region)
        self.assertEqual(res.status_code, 200)

        res = self.client().put('/regions/2/', json=self.sub_child_region)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, dict(success=False, error='Cirdular reference for parent region id'))

        res = self.client().put('/regions/1/', json=self.sub_child_region)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, dict(success=False, error='Cirdular reference for parent region id'))
        

    def test_delete_no_empty_region(self):
        """Test API cant delete region whith childs"""
        res = self.client().post('/regions/', json=self.root_region)
        self.assertEqual(res.status_code, 200)

        res = self.client().post('/regions/', json=self.child_region)
        self.assertEqual(res.status_code, 200)

        res = self.client().get('/regions/1/')
        self.assertEqual(res.status_code, 200)

        data = res.json
        self.assertEqual(len(data.get('childs', [])), 1)

        res = self.client().delete('/regions/1/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, dict(success=False, error='Region already has cties or childs regions'))

    def test_create_update_and_delete_city(self):
        """Test API can create, update and delete cities"""
        res = self.client().post('/regions/', json=self.root_region)
        self.assertEqual(res.status_code, 200)

        res = self.client().post('/regions/', json=self.root_region)
        self.assertEqual(res.status_code, 200)

        res = self.client().post('/regions/1/cities/', json=self.city)
        self.assertEqual(res.status_code, 200)

        res = self.client().get('/regions/1/cities/')
        self.assertEqual(res.status_code, 200)

        data = res.json
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0].get('name'), self.city.get('name'))
        self.assertEqual(data[0].get('region_id'), self.city.get('region_id'))

        res = self.client().put('/regions/1/cities/1/', json=self.empty_region)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, dict(success=False, error='Name not specified'))

        res = self.client().put('/regions/1/cities/1/', json=self.city_changed_without_region)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, dict(success=True))

        res = self.client().get('/regions/1/cities/')
        self.assertEqual(res.status_code, 200)

        data = res.json
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0].get('name'), self.city_changed_without_region.get('name'))
        self.assertEqual(data[0].get('region_id'), self.city.get('region_id'))

        res = self.client().put('/regions/1/cities/1/', json=self.city_changed_with_region)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, dict(success=True))

        res = self.client().get('/regions/1/cities/')
        self.assertEqual(res.status_code, 200)

        data = res.json
        self.assertEqual(len(data), 0)

        res = self.client().get('/regions/2/cities/')
        self.assertEqual(res.status_code, 200)

        data = res.json
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0].get('name'), self.city_changed_with_region.get('name'))
        self.assertEqual(data[0].get('region_id'), self.city_changed_with_region.get('region_id'))

    def test_list_cities_in_region(self):
        """Test API return cities in region"""
        res = self.client().post('/regions/', json=self.root_region)
        self.assertEqual(res.status_code, 200)

        res = self.client().post('/regions/1/cities/', json=self.city)
        self.assertEqual(res.status_code, 200)

        res = self.client().post('/regions/1/cities/', json=self.city)
        self.assertEqual(res.status_code, 200)

        res = self.client().get('/regions/1/cities/')
        self.assertEqual(res.status_code, 200)

        data = res.json
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0].get('name'), self.city.get('name'))
        self.assertEqual(data[0].get('region_id'), self.city.get('region_id'))
        self.assertEqual(data[1].get('name'), self.city.get('name'))
        self.assertEqual(data[1].get('region_id'), self.city.get('region_id'))

    def test_list_cities_in_childs_regions(self):
        """Test API return cities in childs regions"""
        res = self.client().post('/regions/', json=self.root_region)
        self.assertEqual(res.status_code, 200)

        res = self.client().post('/regions/', json=self.child_region)
        self.assertEqual(res.status_code, 200)

        res = self.client().post('/regions/', json=self.sub_child_region)
        self.assertEqual(res.status_code, 200)

        res = self.client().post('/regions/', json=self.sub_child_region)
        self.assertEqual(res.status_code, 200)
        
        for rid in range(2,4):
            city = {'name': 'city name'}
            res = self.client().post(f'/regions/{rid}/cities/', json=city)
            self.assertEqual(res.status_code, 200)

        res = self.client().get('/regions/1/cities/')
        self.assertEqual(res.status_code, 200)

        data = res.json
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0].get('region_id'), 2)
        self.assertEqual(data[1].get('region_id'), 3)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
