import re


def vcard_to_dict(vcard):
	reg = re.compile("\\n(\w+:.+?)\\r",re.DOTALL)
	properties = [split_property(x) for x in reg.findall(vcard)]
	return dict(properties)

def split_vcards(vcards):
	vcard_regex = re.compile("BEGIN:VCARD.+?END:VCARD", re.DOTALL)
	return vcard_regex.findall(vcards)

def split_property(prop):
	prop_par = tuple(re.split(":", prop))
	if (len(prop_par) != 2):
		raise ValueError()
	return prop_par
