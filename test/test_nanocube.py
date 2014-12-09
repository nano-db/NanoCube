from nose.tools import assert_equals
from datetime import datetime
from libs.nanocube import NanoCube


class TestNanoCube:
    def create_sample_cube(slef, **kargs):
        dimensions = ["Description", "Type"]
        if 'loc' in kargs:
            return NanoCube(dimensions, kargs['loc'])
        else:
            return NanoCube(dimensions, 4)

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


    def test_add_node(self):
        cube = self.create_sample_cube(loc=2)
        entry = {
            'Longitude': -122.394685,
            'Latitude': 37.803015,
            'Description': 'Foo',
            'Type': 'Bar',
            'Time': datetime(2005, 7, 12, 10, 5, 1)
        }
        cube.add(entry)
