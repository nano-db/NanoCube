from nose.tools import assert_equals
from libs.nanocube import NanoCube


class TestNanoCube:
    def create_sample_cube():
        dimensions = ["Description", "Type"]
        return NanoCube(dimensions, 4)

    def test_get_location_key(self):
        cube = TestNanoCube.create_sample_cube()
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
        cube = TestNanoCube.create_sample_cube()
        entry = {
            'Description': 'Foo',
            'Type': 'Bar',
        }
        ret = cube._get_category_keys(entry, 6)
        assert_equals(ret, ["0", "0"])
        entry = {
            'Description': 'Bar',
            'Type': 'Bar',
        }
        ret = cube._get_category_keys(entry, 6)
        assert_equals(ret, ["1", "0"])
