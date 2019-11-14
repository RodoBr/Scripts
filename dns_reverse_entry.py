import requests
import falcon
import os
import re
import xml.etree.ElementTree as ET
from lxml import etree
from datetime import datetime

class TestResource(object):
	def on_post(self, req, resp):
		xml = req.stream.read()
		e = ET.ElementTree(ET.fromstring(xml))
		resp.set_header('Content-Type', 'application/xml')
		resp.set_header('Content-Encoding', 'utf-8')
		resp.status = falcon.HTTP_200

		# Variable à modifier
		zone_path = "/test/prod/"

		# Variable à renommer éventuellement pour la prod
		zone_file = ""
		ip = ""
		fqdn = ""

		# Variables fixes à ne pas modifier
		today = datetime.today().strftime('%Y%m%d')
		entry = ""
		old_entry = []

		# Fonction d'incrémentation du serial number
		def serial():
			tmp = []

			with open(zone_path + zone_file) as fichier:
				for line in fichier.readlines():
					if re.search(r'^(.*?(\Serial\b)[^$]*)$', line):                
						tmp.append(line)

			tmp = str(tmp)
			tmp = re.search(r'(?<!\d)\d{10}(?!\d)', tmp).group()
			old_serial = str(tmp)
			old_serial_date = str(tmp)[:8]
			tmp = tmp[-2:]
			tmp = int(tmp)
			if old_serial_date == today:
				tmp = "{:02d}".format(tmp + 1)
				serial = str(today + tmp)
			else:
				serial = today + "01"

			o = open("tmp_file","w")
			data = open(zone_path + zone_file).read()
			o.write(re.sub(old_serial, serial, data))
			o.close()
			os.system("mv tmp_file " + zone_path + zone_file)

		# Lecture de la demande d'entrée
		for elt in e.iter():

			if elt.tag == "ip":
				ip = elt.text

			if elt.tag == "fqdn":
				fqdn = elt.text

			if elt.tag == "zone_file":
				zone_file = elt.text

		# Création de la nouvelle entrée
		ptr = str(ip.split('.')[-1:]).replace('[', '').replace('\'', '').replace(']', '')
		entry += ptr + "\tIN\tPTR\t" + fqdn + ".\n"

		# Récupération de l'ancienne valeur de l'entrée
		with open(zone_path + zone_file) as fichier:
			for line in fichier.readlines():
				if re.search(r'^' + re.escape(ptr) + '\s', line):
					old_entry.append(line)
		old_entry = str(old_entry)
		old_entry = old_entry.replace('[', '').replace('\'', '').replace(']', '')

		# Recherche et remplacement de l'ancienne entrée par la nouvelle
		o = open("tmp_file","w")
		data = open(zone_path + zone_file).read()
		o.write(re.sub(old_entry, entry, data, 1))
		o.close()
		os.system("mv tmp_file " + zone_path + zone_file)

		# Incrémentation du serial number
		serial()

		ptr = int(ptr)
		if ptr <= 255:
			resp.body = ("Entry succesfully created.\n")
			os.system('rndc reload')
		else:
			resp.body = ("Invalid IP.\n")

app = falcon.API()

test_resource = TestResource()

app.add_route('/test', test_resource)
