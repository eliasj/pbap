#!/usr/bin/env python
""" Discribe the libary"""
import re
import StringIO
import uuid
import lightblue

from _vcardparser import split_vcards, vcard_to_dict

class PBAP(object):
    """ Phonebook Access Profile (PBAP) """
    PBAP_TARGET_UUID = uuid.UUID('{796135f0-f0c5-11d8-0966-0800200c9a66}').bytes
    __port = 0
    def __init__(self, device_address):
        self.__device_address = device_address
        self.__find_service_port()
        self.__client = lightblue.obex.OBEXClient(device_address, self.__port)
        response = self.__client.connect({'target': self.PBAP_TARGET_UUID})
        if (response.reason != 'OK'):
            raise Exception("Could not connect " + response)
		    # TODO build a better exeption
        self.connection_id = response.headers['connection-id']

    def __find_service_port(self):
        """ Find which bluetooth port PBAP is usning on the device """
        for (a, port, service) in lightblue.findservices(self.__device_address):
            try :
                match = re.search("Phonebook Access", service)
                if (match != None):
                    self.__port = port
            except TypeError:
                continue


    def pull_phonebook(self):
        """ Get the all the contacts from the phonebook """
        body_of_response = StringIO.StringIO()
        response = self.__client.get({'connection-id':self.connection_id,
                    'type':'x-bt/phonebook',
                    'name':'pb.vcf'}, body_of_response)
		# TODO check the response
        return [vcard_to_dict(x) for x in split_vcards(body_of_response.getvalue())]

    def set_phonebook(self):
        """ Set which phonebook that should be used"""
        pass

    def pull_vcard_listning(self):
        """ List all the contacts (vcards) """
        pass

    def pull_vcard_entry(self):
        """ Get a vcard """
        pass

