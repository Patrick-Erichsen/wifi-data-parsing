import unittest
from parse import get_ssid_intersections, remove_non_intersection_scans

sample_data = [
    [
        {
            "SSID": "AndroidWifi1",
            "BSSID": "02:15:b2:00:01:00",
            "frequency": 2447,
            "level": -50,
            "timestamp": 51496683
        },
        {
            "SSID": "AndroidWifi2",
            "BSSID": "02:15:b2:00:01:00",
            "frequency": 2447,
            "level": -50,
            "timestamp": 51496683
        }
    ],
    [
        {
            "SSID": "AndroidWifi1",
            "BSSID": "02:15:b2:00:01:00",
            "frequency": 2447,
            "level": -50,
            "timestamp": 51496683
        }
    ]
]


class TestParse(unittest.TestCase):

    def test_get_ssid_intersections(self):
        self.assertEqual(get_ssid_intersections(sample_data), ['AndroidWifi1'])

    def test_remove_non_intersection_scans(self):
        intersections = ['AndroidWifi1']
        intersected_data = [[sample_data[0][0]], [sample_data[1][0]]]

        self.assertEqual(remove_non_intersection_scans(
            intersections, sample_data), intersected_data)


if __name__ == '__main__':
    unittest.main()
