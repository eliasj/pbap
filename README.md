PBAP
====

This is a implementation of Phonebook Access Profile (PBAP) for bluetooth using Python and the lightblue package. The lightblue package is no longer maintained.

This packages should work on both Mac OS X and Linux, but is only tested on Mac OS X 10.9

Installation
------------

./setup.py install


Usage
-----

``` python
import pbap
devices = pbap.find_devices()

# Connect to the first device, you probably want to select your device manually.
pb = pbap.PBAP(devices[0][0])
# Get the whole phonebook from the device.
phonebook = pb.pull_phonebook()

# To be able to list all the contacts, you have to select which type of phonebook to use. The phones or the sim cards.
pb.set_phonebook("telecom")
# You can list following phonebooks: pb, ich, och, mch, cch, spd and fav.
list_of_all_contacts = pb.pull_vcard_listing("pb")

# Set the phonebook you will use to get the contact from.
pb.set_phonebook("pb")
first_contact = pb.pull_vcard_entry(list_of_all_contacts[0][0])
print first_contact
```

Links
-----

* [Phonebook Access Profile Specification](https://www.bluetooth.org/DocMan/handlers/DownloadDoc.ashx?doc_id=281299)
* [Lightblue](https://github.com/pebble/lightblue-0.4) version the I have used.
