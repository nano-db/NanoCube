from datetime import datetime
from copy import copy

from nose.tools import assert_equals, assert_is_instance, assert_is_none

from libs.server.timeserietable import TimeSerieTable
from libs.server.nanocube import NanoCube


class TestNanoCube:
    def create_sample_cube(slef, **kargs):
        dimensions = ["Description", "Type"]
        if 'loc' in kargs:
            return NanoCube(dimensions, loc_granularity=kargs['loc'])
        else:
            return NanoCube(dimensions, loc_granularity=4)

    def test_get_location_key(self):
        cube = self.create_sample_cube()
        sf = {
            'Longitude': -122.394685,
            'Latitude': 37.803015
        }
        ret = cube._get_location_keys(sf, 2)
        assert_equals(ret, ["0,1", "00,10"])

        australia = {
            'Longitude': 133.281323,
            'Latitude': -23.249397
        }
        ret = cube._get_location_keys(australia, 2)
        assert_equals(ret, ["1,0", "11,01"])

    def test_get_category_keys(self):
        cube = self.create_sample_cube()
        entry = {
            'Description': 'Foo',
            'Type': 'Bar',
        }
        assert_equals(cube._get_category_keys(entry, 2), ["0"])
        assert_equals(cube._get_category_keys(entry, 3), ["0"])

        entry = {
            'Description': 'Bar',
            'Type': 'Bar',
        }
        assert_equals(cube._get_category_keys(entry, 2), ["1"])
        assert_equals(cube._get_category_keys(entry, 3), ["0"])

    def test_keys_at_level(self):
        cube = self.create_sample_cube(loc=2)
        entry = {
            'Longitude': -122.394685,
            'Latitude': 37.803015,
            'Description': 'Foo',
            'Type': 'Bar'
        }

        keys = [["0,1", "00,10"], ["0"], ["0"]]
        for i, keys in enumerate(keys):
            print(i, keys)
            ret = cube._keys_at_level(entry, i + 1)
            assert_equals(ret, keys)

        entry = {
            'Longitude': -122.394685,
            'Latitude': 37.803015,
            'Description': 'Bar',
            'Type': 'Bar'
        }

        keys = [["0,1", "00,10"], ["1"], ["0"]]
        for i, keys in enumerate(keys):
            print(i, keys)
            ret = cube._keys_at_level(entry, i + 1)
            assert_equals(ret, keys)


    def test_simple_add(self):
        cube = self.create_sample_cube(loc=2)
        entry = {
            'Longitude': -122.394685,
            'Latitude': 37.803015,
            'Description': 'Foo',
            'Type': 'Bar',
            'Time': datetime(2005, 7, 12, 10, 5, 1)
        }
        cube.add(entry)

        world = cube.world
        assert_equals(len(world.proper_children), 1)
        node = world.get_child('0,1')
        assert_equals(len(node.proper_children), 1)
        node = node.get_child('00,10')
        assert_equals(len(node.proper_children), 0)
        node = node.content
        assert_equals(len(node.proper_children), 1)
        node = node.get_child('0').content
        assert_equals(len(node.proper_children), 1)
        node = node.get_child('0').content
        assert(isinstance(node, TimeSerieTable))

        table = world.shared_content.shared_content.shared_content
        assert(isinstance(table, TimeSerieTable))

    def test_2_simple_add(self):
        cube = self.create_sample_cube(loc=2)
        entry = {
            'Longitude': -122.394685,
            'Latitude': 37.803015,
            'Description': 'Foo',
            'Type': 'Bar',
            'Time': datetime(2005, 7, 12, 10, 5, 1)
        }
        cube.add(entry)
        entry['Time'] = datetime(2005, 7, 12, 10, 10, 1)
        cube.add(entry)

        world = cube.world
        table = world.shared_content.shared_content.shared_content
        assert_equals(table.table[0]['sum'], 2)

    def test_add_2_sub_elements(self):
        cube = NanoCube(["Type"], 2)
        entry = {
            'Longitude': -122.394685,
            'Latitude': 37.803015,
            'Type': 'IPhone',
            'Time': datetime(2005, 7, 12, 10, 5, 1)
        }
        cube.add(entry)
        entry['Type'] = 'Android'
        entry['Time'] = datetime(2005, 7, 12, 10, 7, 1)
        cube.add(entry)

        assert_is_none(cube.world.shared_content.shared_content)
        assert_is_instance(cube.world.shared_content.content, TimeSerieTable)

    def test_add_2_sub_elements(self):
        cube = NanoCube(["Type"], 2)
        o1 = {
            'Longitude': -122.394685,
            'Latitude': 37.803015,
            'Type': 'Android',
            'Time': datetime(2005, 7, 12, 10, 5, 1)
        }

        o2 = copy(o1)
        o2['Type'] = 'Iphone'

        o3 = copy(o1)
        o3['Type'] = 'Iphone'
        o3['Longitude'] = -25.721672
        o3['Latitude'] =  28.232283

        cube.add(o1)
        cube.add(o2)
        cube.add(o3)

    def test_schema(self):
        cube = NanoCube(["Type"], loc_granularity=2)
        o1 = {
            'Longitude': -122.394685,
            'Latitude': 37.803015,
            'Type': 'Android',
            'Time': datetime(2005, 7, 12, 10, 5, 1)
        }

        o2 = copy(o1)
        o2['Type'] = 'Iphone'

        o3 = copy(o1)
        o3['Type'] = 'Iphone'
        o3['Longitude'] = -25.721672
        o3['Latitude'] =  28.232283

        cube.add(o1)
        cube.add(o2)
        cube.add(o3)

        schema = cube.schema()
        assert_equals(len(schema['dimensions']), 2)

        loc_dim = schema['dimensions'][0]
        assert_equals(loc_dim['type'], 'quad_tree_2')
        assert_equals(loc_dim['name'], 'Location')

        devise_dim = schema['dimensions'][1]
        assert_equals(devise_dim['type'], 'cat_1')
        assert_equals(devise_dim['name'], 'Type')
        assert('Iphone' in devise_dim['values'].keys())
        assert('Android' in devise_dim['values'].keys())
