#!/usr/local/bin python3
#
# -----------------------------------------------------------
# Program to parse WiFi data exported in JSON format
# from PrivateKit and calculate the variance in RSSI
# for access points.
#
# Data is written to a CSV file with the same name as the JSON
# file.
# -----------------------------------------------------------

import json
import sys
import csv
import os
from pathlib import Path
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


def get_bssid_vars(bssids, data):
    '''
    Returns an array of tuples where the first index is the bssid,
    and the second index is the variance for that bssid
    '''

    bssid_vars = []

    for bssid in bssids:
        var = calculate_rssi_var(bssid, data)
        bssid_vars.append([bssid, var])

    return bssid_vars


def write_to_csv(file_name, bssid_var_tuple):
    '''
    Write the tuple data from `data` to the csv `file_name`
    '''

    try:
        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["MAC Address", "Variance"])

            for data in bssid_var_tuple:
                writer.writerow([data[0], data[1]])

        print('successfully wrote BSSID variance data to', file_name)
    except:
        os.remove(file_name)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("a path to the json data file must be passed")

    file_path = sys.argv[1]
    file_name = os.path.basename(file_path).split('.')[0] + '.csv'

    # CSV file we will try to write to already exists - error out
    if Path(file_name).is_file():
        print('overwriting', file_name)
        os.remove(file_name)

    file = open(file_path)
    data = json.load(file)

    wifi_data = data['WIFI_DATA']

    bssid_intersection = get_bssid_intersections(wifi_data)

    intersected_wifi_data = remove_non_intersection_scans(
        bssid_intersection, wifi_data)

    bssid_vars = get_bssid_vars(bssid_intersection, intersected_wifi_data)

    write_to_csv(file_name, bssid_vars)
