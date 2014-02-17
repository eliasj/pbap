import unittest

from pbap._vcardparser import *


class TestVcardparser(unittest.TestCase):
    two_vcards = "BEGIN:VCARD\r\nEND:VCARD\r\nBEGIN:VCARD\r\nEND:VCARD"
    three_vcards = """BEGIN:VCARD\r\nVERSION:2.1\r\nFN:Mitt namn\r\n
    N:Mitt namn\r\nEND:VCARD\r\nBEGIN:VCARD\r\nVERSION:2.1\r\n
    N:Cha;Willy;;;\r\nFN:Willy Cha\r\nTEL;CELL:0707707043\r\nEND:VCARD\r\n
    BEGIN:VCARD\r\nVERSION:2.1\r\nN:Rickard;Vaktis;;;\r\nFN:Vaktis Rickard\r\n
    TEL;WORK:0313321231\r\nEND:VCARD"""
    vcard = """BEGIN:VCARD\r\nVERSION:2.1\r\nFN:Mitt namn\r\n
    N:Mitt namn\r\nEND:VCARD"""

    def test_split_two_vcard(self):
        self.assertEquals(len(split_vcards(self.two_vcards)), 2)

    def test_split_three_vcard(self):
        self.assertEquals(len(split_vcards(self.three_vcards)), 3)

    def test_vcard_to_dict(self):
        expected = {'VERSION': '2.1', 'FN': 'Mitt namn', 'N': 'Mitt namn'}
        self.assertEquals(vcard_to_dict(self.vcard), expected)

    def test_split_property(self):
        expected = ("test", "test")
        self.assertEquals(split_property("test:test"), expected)

    def test_split_property_URL(self):
        expected = ("URL", "http://webpage.com")
        self.assertEquals(split_property("URL:http://webpage.com"), expected)
