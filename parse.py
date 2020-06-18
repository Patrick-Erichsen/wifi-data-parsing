import json
import sys
from statistics import variance


def intersection(set1, set2):
    return list(set(set1) & set(set2))


def get_bssid_intersections(data):
    '''
    Get a set of all bssid values that
    appeared in every network scan
    '''

    bssid_intersection = []

    # Initialize `bssid_intersection` with first index
    for scan in data[0]:
        bssid_intersection.append(scan['BSSID'])

    for scan_group in data:
        bssids = []

        for scan in scan_group:
            bssids.append(scan['BSSID'])

        bssid_intersection = intersection(bssid_intersection, bssids)

    return bssid_intersection


def remove_non_intersection_scans(intersections, data):
    '''
    Iterate through our array of wifi scans and remove the scans
    whose bssid did not appear in every scan group
    '''

    for scan_group in data:
        for scan in scan_group:
            if scan['BSSID'] not in intersections:
                scan_group.remove(scan)

    return data


def calculate_rssi_var(bssid, data):
    '''
    Calculates the variance in RSSI for a single bssid
    '''

    rssi_values = []

    for scan_group in data:
        for scan in scan_group:
            if scan['BSSID'] == bssid:
                rssi_values.append(scan['level'])

    return variance(rssi_values)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("a path to the json data file must be passed")

    file_path = sys.argv[1]

    file = open(file_path)
    data = json.load(file)

    wifi_data = data['WIFI_DATA']

    bssid_intersection = get_bssid_intersections(wifi_data)

    intersected_wifi_data = remove_non_intersection_scans(
        bssid_intersection, wifi_data)

    for bssid in bssid_intersection:
        var = calculate_rssi_var(bssid, intersected_wifi_data)
        print('bssid:', bssid, 'rssi variance:', var)
