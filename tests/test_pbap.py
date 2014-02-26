import unittest

import lightblue
from mock import patch, Mock

import pbap


class TestPBAP(unittest.TestCase):
    __pb = None

    @patch('lightblue.obex.OBEXClient')
    def setUp(self, obex_mock):
        lightblue.findservices = Mock(
            return_value=[
                (
                    "fake address",
                    '15',
                    "Phonebook Access")])
        self.__mc = obex_mock.return_value
        self.__mc.connect.return_value = lightblue.obex.OBEXResponse(
            lightblue.obex.OK, {195: 35288, 203: 1})
        self.__pb = pbap.PBAP("fake address")
        self.__mc.setpath.return_value = lightblue.obex.OBEXResponse(
            lightblue.obex.OK, {195: 35288, 203: 1})

    def test__init__(self):
        self.assertEqual(1, self.__pb.connection_id)

    @patch('StringIO.StringIO')
    def test_pull_phonebook(self, mock_stringio):
        self.__mc.get.return_value = lightblue.obex.OBEXResponse(
            lightblue.obex.OK, {195: 35288, 203: 1})
        mock_stringio.return_value.getvalue.return_value = """
            BEGIN:VCARD\r\nVERSION:2.1\r\nFN:Mitt namn\r\nN:Mitt namn\r\n
            END:VCARD\r\nBEGIN:VCARD\r\nVERSION:2.1\r\nN:Cha;Willy;;;\r\n
            FN:Willy Cha\r\nTEL;CELL:0707707043\r\nEND:VCARD\r\nBEGIN:VCARD\r\n
            VERSION:2.1\r\nN:Rickard;Vaktis;;;\r\nFN:Vaktis Rickard\r\n
            TEL;WORK:0313321231\r\nEND:VCARD\r\nBEGIN:VCARD\r\nVERSION:2.1\r\n
            N:F;F;;;\r\nFN:F F\r\nTEL;VOICE:9837\r\nEND:VCARD\r\n
            BEGIN:VCARD\r\nVERSION:2.1\r\nN:M;M;;;\r\nFN:M M\r\n
            TEL;VOICE:9958\r\nEND:VCARD\r\nBEGIN:VCARD\r\nVERSION:2.1\r\n
            N:I;I;;;\r\nFN:I I\r\nTEL;VOICE:9774\r\nEND:VCARD"""
        self.assertEqual(6, len(self.__pb.pull_phonebook()))

    def test_set_phonebook_not_phonebook(self):
        self.assertRaises(Exception, self.__pb.set_phonebook, "cake")

    def test_set_phonebook(self):
        self.__pb.set_phonebook("telecom")
        self.assertEqual("/telecom", self.__pb.path)

    def test_set_phonebook_depth_2(self):
        self.__pb.set_phonebook("telecom")
        self.__pb.set_phonebook("pb")
        self.assertEqual("/telecom/pb", self.__pb.path)

    def test_set_phonebook_depth_2_error(self):
        self.__pb.set_phonebook("telecom")
        self.assertEqual("/telecom", self.__pb.path)
        self.assertRaises(Exception, self.__pb.set_phonebook, "telecom")

    def test_set_phonebook_wrong_order(self):
        self.__pb.set_phonebook("telecom")
        self.assertEqual("/telecom", self.__pb.path)
        self.assertRaises(Exception, self.__pb.set_phonebook, "SIM1")

    def test_set_phonebook_back_to_root(self):
        self.__pb.set_phonebook("telecom")
        self.assertEqual("/telecom", self.__pb.path)
        self.__pb.set_phonebook("")
        self.assertEqual("/", self.__pb.path)

    def test_set_phonebook_go_up_a_level(self):
        self.__pb.set_phonebook("SIM1")
        self.assertEqual("/SIM1", self.__pb.path)
        self.__pb.set_phonebook("telecom")
        self.assertEqual("/SIM1/telecom", self.__pb.path)
        self.__pb.set_phonebook("ich")
        self.assertEqual("/SIM1/telecom/ich", self.__pb.path)
        self.__pb.set_phonebook("..")
        self.assertEqual("/SIM1/telecom", self.__pb.path)

    def test_pull_vcard_listing_wrong_folder(self):
        self.assertRaises(Exception, self.__pb.pull_vcard_listing, "cake")

    @patch('StringIO.StringIO')
    def test_pull_vcard_listing_with_space(self, mock_stringio):
        self.__mc.get.return_value = lightblue.obex.OBEXResponse(
            lightblue.obex.OK, {195: 35288, 203: 1})
        mock_stringio.return_value.getvalue.return_value = """
            <?xml version="1.0"?> <!DOCTYPE vcard_listning SYSTEM
            "vcard-listing.dtd"> <vCard-listing version="1.0">
            <card handle = "0.vcf" name = "Doung;My"/>
            </vCard-listing>"""
        self.assertEqual(1, len(self.__pb.pull_vcard_listing("pb")))

    @patch('StringIO.StringIO')
    def test_pull_vcard_listing_without_space(self, mock_stringio):
        self.__mc.get.return_value = lightblue.obex.OBEXResponse(
            lightblue.obex.OK, {195: 35288, 203: 1})
        mock_stringio.return_value.getvalue.return_value = """
            <?xml version="1.0"?><!DOCTYPE vcard-listing SYSTEM
            "vcard-listing.dtd"><vCard-listing version="1.0">
            <card handle="0.vcf" name="Mitt namn"/>
            </vCard-listing>"""
        self.assertEqual(1, len(self.__pb.pull_vcard_listing("pb")))

    def test_pull_vcard_entry_wrong_name(self):
        self.assertRaises(Exception, self.__pb.pull_vcard_entry, "cookie")

    @patch('StringIO.StringIO')
    def test_pull_vcad_entry(self, mock_stringio):
        self.__mc.get.return_value = lightblue.obex.OBEXResponse(
            lightblue.obex.OK, {195: 35288, 203: 1})
        mock_stringio.return_value.getvalue.return_value = """
            BEGIN:VCARD\r\nVERSION:2.1\r\nFN:Mitt namn\r\nN:Mitt namn\r\n
            END:VCARD"""
        self.assertEqual(3, len(self.__pb.pull_vcard_entry("1.vcf")))
        self.assertEqual(3, len(self.__pb.pull_vcard_entry("1")))


class TestFunctions(unittest.TestCase):

    def test_find_pbap_port_found(self):
        lightblue.findservices = Mock(
            return_value=[
                ("fake address", '15', "Phonebook Access")])
        self.assertEqual('15', pbap.find_pbap_port("fake"))

    def test_find_pbap_port_not_found(self):
        lightblue.findservices = Mock(
            return_value=[
                ("fake address", '15', "Voice")])
        self.assertIsNone(pbap.find_pbap_port("fake"))

    def test_have_pbap_service_found(self):
        lightblue.findservices = Mock(
            return_value=[
                ("fake address", '15', "Phonebook Access")])
        self.assertTrue(pbap.have_pbap_service(["fake", "15", "SK17i"]))

    def test_have_pbap_service_not_found(self):
        lightblue.findservices = Mock(
            return_value=[
                ("fake address", '15', "Voice")])
        self.assertFalse(pbap.have_pbap_service(["fake", "15", "SK17i"]))

    def test_find_devices(self):
        lightblue.finddevices = Mock(
            return_value=[
                ("fake address", '15', "SK17i"),
                ("fake address", '15', "MT15i")])
        lightblue.findservices = Mock(
            return_value=[
                ("fake address", '15', "Phonebook Access")])
        result = pbap.find_devices()
        self.assertEqual(2, len(result))
        self.assertEqual(
            [
                ("fake address", '15', "SK17i"),
                ("fake address", '15', "MT15i")],
            result)
