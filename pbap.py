#!/usr/bin/env python
""" Discribe the libary"""
import re
import StringIO
import uuid
import lightblue

from _vcardparser import split_vcards, vcard_to_dict

def find_devices():
    """ Find the devices that are running PBAP on. Return a list with
        divices
    """
    return [dev for dev in lightblue.finddevices() if have_pbap_service(dev)]


def have_pbap_service(device):
    """ Check if a device have PBAP running. """
    try:
        if (find_pbap_port(device[0]) != None):
            return True
        else:
            return False
    except AttributeError, error:
        return False


def find_pbap_port(device_address):
    """ Find which bluetooth port PBAP is usning on the device """
    for (address, port, service) in lightblue.findservices(device_address):
        match = re.search("Phonebook Access", service)
        if (match != None):
            return port
    return None



class PBAP(object):
    """ Phonebook Access Profile (PBAP) """
    PBAP_TARGET_UUID = uuid.UUID('{796135f0-f0c5-11d8-0966-0800200c9a66}').bytes
    __port = 0
    def __init__(self, device_address):
        self.__device_address = device_address
        self.__port = find_pbap_port(device_address)
        self.__client = lightblue.obex.OBEXClient(device_address, self.__port)
        response = self.__client.connect({'target': self.PBAP_TARGET_UUID})
        if (response.reason != 'OK'):
            raise Exception("Could not connect " + response)
		    # TODO build a better exception
        self.connection_id = response.headers['connection-id']

    def pull_phonebook(self):
        """ Get the all the contacts from the phonebook """
        body_of_response = StringIO.StringIO()
        response = self.__client.get({'connection-id':self.connection_id,
                    'type':'x-bt/phonebook',
                    'name':'pb.vcf'}, body_of_response)
        if (response.reason != 'OK'):
            raise Exception("Could not get the phonebook" + str(response))
            # TODO build a better exception
        return [vcard_to_dict(x) for x in split_vcards(body_of_response.getvalue())]

    def set_phonebook(self):
        """ Set which phonebook that should be used"""
        pass

    def pull_vcard_listing(self):
        """ List all the contacts (vcards) """
        body_of_response = StringIO.StringIO()
        response = self.__client.get({'connection-id':self.connection_id,
            'type':'x-bt/vcard-listing',
            'name':'pb.vcf'}, body_of_response)
        if (response.reason != 'OK'):
            raise Exception("Clould not list the vCards" + str(response))
            # TODO build a better exception
        return body_of_response.getvalue()

    def pull_vcard_entry(self):
        """ Get a vcard """
        pass

