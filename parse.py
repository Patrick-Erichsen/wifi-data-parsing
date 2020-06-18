import json
import sys


def intersection(set1, set2):
    return list(set(set1) & set(set2))


def get_ssid_intersections(data):
    '''
    Get a set of all SSID values that
    appeared in every network scan
    '''

    ssid_intersection = []

    # Initialize `ssid_intersection` with first index
    for scan in data[0]:
        ssid_intersection.append(scan['SSID'])

    for scan_group in data:
        ssids = []

        for scan in scan_group:
            ssids.append(scan['SSID'])

        ssid_intersection = intersection(ssid_intersection, ssids)

    return ssid_intersection


def remove_non_intersection_scans(intersections, data):
    '''
    Iterate through our array of wifi scans and remove the scans
    whose SSID did not appear in every scan group
    '''

    for scan_group in data:
        for scan in scan_group:
            if scan['SSID'] not in intersections:
                scan_group.remove(scan)

    return data


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("a path to the json data file must be passed")

    file_path = sys.argv[1]

    file = open(file_path)
    data = json.load(file)

    wifi_data = data['WIFI_DATA']

    ssid_intersection = get_ssid_intersections(wifi_data)

    intersected_wifi_data = remove_non_intersection_scans(
        ssid_intersection, wifi_data)
