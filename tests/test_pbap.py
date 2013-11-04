import unittest

import lightblue
from mock import patch, Mock

import pbap


class TestPBAP(unittest.TestCase):
    __pb = None
    @patch('lightblue.obex.OBEXClient')
    def setUp(self, obex_mock):
        lightblue.findservices = Mock(return_value=[("fake address", '15', "Phonebook Access")])
        self.__mc = obex_mock.return_value
        self.__mc.connect.return_value = lightblue.obex.OBEXResponse(lightblue.obex.OK, {195: 35288, 203: 1})
        self.__pb = pbap.PBAP("fake address")

    def test__init__(self):
        self.assertEqual(1, self.__pb.connection_id)


    @patch('StringIO.StringIO')
    def test_pull_phonebook(self, mock_stringio):
        self.__mc.get.return_value = lightblue.obex.OBEXResponse(lightblue.obex.OK, {195: 35288, 203: 1})
        mock_stringio.return_value.getvalue.return_value = "BEGIN:VCARD\r\nVERSION:2.1\r\nFN:Mitt namn\r\nN:Mitt namn\r\nEND:VCARD\r\nBEGIN:VCARD\r\nVERSION:2.1\r\nN:Cha;Willy;;;\r\nFN:Willy Cha\r\nTEL;CELL:0707707043\r\nEND:VCARD\r\nBEGIN:VCARD\r\nVERSION:2.1\r\nN:Rickard;Vaktis;;;\r\nFN:Vaktis Rickard\r\nTEL;WORK:0313321231\r\nEND:VCARD\r\nBEGIN:VCARD\r\nVERSION:2.1\r\nN:F;F;;;\r\nFN:F F\r\nTEL;VOICE:9837\r\nEND:VCARD\r\nBEGIN:VCARD\r\nVERSION:2.1\r\nN:M;M;;;\r\nFN:M M\r\nTEL;VOICE:9958\r\nEND:VCARD\r\nBEGIN:VCARD\r\nVERSION:2.1\r\nN:I;I;;;\r\nFN:I I\r\nTEL;VOICE:9774\r\nEND:VCARD"
        self.assertEqual(6, len(self.__pb.pull_phonebook()))
