#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 - 2019 Syrian Programmer.
#
# Email: Syrian.Programmer@Gmail.com
#
#
# Extract information from app: Outils OBD Facile
# https://play.google.com/store/apps/details?id=com.outilsobdfacile.obd.connecteur.dlc
#

import requests
import os


class OBDConnector:
    """
    Class to connection site and get info
    """

    def __init__(self):

        self.cookies = {
            'PHPSESSID': 'vk35c3rtfg80u41gl2nsk7jk40',
            'test_cookie': '1',
            '_omappvp': 'k0Xhn8GII6EmYD540Q7iQFbBjD36n5ul8JlMZb0eb2KrGBAeHw2KpXbmh1gWHr7jZWITSwrL4uxa2GcLC8Xn6m6QvpgsrykZ',
            'pali_visit_-L24zYJ1_nrRp8GB3mKc': 'true',
            'pali_visit_-L24zYJ1_nrRp8GB3mKc_outilsobdfacile_fr': 'true',
        }

        self.headers = {
            'Host': 'www.outilsobdfacile.fr',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
        }

    def get_details_all_facile(self):
        """
        get info facile and model.
        :return: response as json.
        """
        url = 'https://www.outilsobdfacile.fr/vehicle/conn-webservice/index.php/obd/getconnectorsV2'
        respone = requests.get(url, headers=self.headers, cookies=self.cookies)

        if not respone.status_code == 200:
            return False

        if not respone.json()['statut'] == 'OK':
            return False

        return respone.json()

    def get_photo(self, url: str):
        """
        get photo
        :param url:
        :return: response as byte.
        """

        base_url = 'https://www.outilsobdfacile.com/base_connecteur/{}'.format(url)
        response = requests.get(base_url, headers=self.headers, cookies=self.cookies)

        if not response.status_code == 200:
            return False

        return response.content


def create_folder(path: str):
    os.makedirs(path, exist_ok=True)


def write_file_txt(path: str, string: str):
    with open(path, 'w') as file:
        file.write(string)


def write_image(path: str, photo: bytes):
    with open(path, 'wb') as file:
        file.write(photo)


if __name__ == '__main__':
    obd_connector = OBDConnector()
    response = obd_connector.get_details_all_facile()

    info_all_facile = response['result']
    count_all_facile = len(info_all_facile)

    print('Count all model facile: {}'.format(count_all_facile))

    for index, facile in enumerate(info_all_facile, start=1):

        brand = facile['b']
        model = facile['c']
        print('Request brand: {}, model: {}.'.format(brand, model))

        path_folder = os.path.join('media', brand, model)
        create_folder(path_folder)

        path_file_txt = os.path.join(path_folder, 'info.txt')
        text = '{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n'.format(facile['b'], facile['c'], facile['d'],
                                                                             facile['e'], facile['f'], facile['g'],
                                                                             facile['h'], facile['i'], facile['j'],
                                                                             facile['k'], facile['l'], facile['m'],
                                                                             facile['r'])

        for link in ['n', 'o', 'p', 'q']:
            if not facile[link]:
                continue

            photo = obd_connector.get_photo(facile[link])
            name_photo = facile[link].split('/')[-1]
            path_photo = os.path.join(path_folder, name_photo)
            write_image(path_photo, photo)

        write_file_txt(path_file_txt, text)
