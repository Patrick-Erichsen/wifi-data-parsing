import unittest
from parse import get_bssid_intersections, remove_non_intersection_scans, calculate_rssi_var

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
            "BSSID": "02:15:b2:00:01:01",
            "frequency": 2447,
            "level": -5,
            "timestamp": 51496683
        }
    ],
    [
        {
            "SSID": "AndroidWifi1",
            "BSSID": "02:15:b2:00:01:00",
            "frequency": 2447,
            "level": -55,
            "timestamp": 51496683
        }
    ]
]

common_bssid = "02:15:b2:00:01:00"


class TestParse(unittest.TestCase):

    def test_get_ssid_intersections(self):
        self.assertEqual(get_bssid_intersections(
            sample_data), [common_bssid])

    def test_remove_non_intersection_scans(self):
        intersections = [common_bssid]
        intersected_data = [[sample_data[0][0]], [sample_data[1][0]]]

        self.assertEqual(remove_non_intersection_scans(
            intersections, sample_data), intersected_data)

    def test_calculate_rssi_var(self):
        self.assertEqual(calculate_rssi_var(
            common_bssid, sample_data), 12.5)


if __name__ == '__main__':
    unittest.main()
