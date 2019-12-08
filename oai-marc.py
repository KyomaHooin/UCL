#!/usr/bin/python
#
# Harvested OAI-PMH 2.0 MARCXML Record validator.
#
# https://aleph.mzk.cz/OAI?verb=GetRecord&identifier=oai:aleph.mzk.cz:MZK01-000152782&metadataPrefix=marc21
#

# INCLUDE -------------------

from __future__ import print_function

import argparse,StringIO,sys,os,re

from datetime import datetime
from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry
from pymarc import marcxml,MARCWriter,JSONWriter,XMLWriter
from lxml.etree import tostring

# VAR -------------------

URL='https://aleph.mzk.cz/OAI'
LOG='oai-marc.log'

# DEF -------------------

def MarcXML(xml):
	handler = marcxml.XmlHandler()
	marcxml.parse_xml(StringIO.StringIO(tostring(xml, encoding='utf-8')), handler)
	return handler.records[0]

def valid_date(s):
	try:
		return datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
	except:
		msg = 'Invalid date format.'
		raise argparse.ArgumentTypeError(msg)

def valid_format(s):
	if s in ('json', 'marc', 'xml'): return s
	else:
		msg = 'Invalid export format.'
		raise argparse.ArgumentTypeError(msg)

def valid_display(s):
	if s in ('ident', 'json', 'marc'): return s
	else:
		msg = 'Invalid display format.'
		raise argparse.ArgumentTypeError(msg)

def valid_request(s):
	if s in ('record', 'set', 'meta'): return s
	else:
		msg = 'Invalid request format.'
		raise argparse.ArgumentTypeError(msg)

# ARG -------------------

parser = argparse.ArgumentParser(description="OAI PMH 2.0 MARCXML Validator.")
listing = parser.add_argument_group('info')
listing.add_argument('--get', help='Request type. [record] [set] [meta]', type=valid_request, default='record')
required = parser.add_argument_group('validation')
required.add_argument('--set', help='Records set.')
required.add_argument('--from', help='Records from. [YYYY-mm-dd HH:MM:SS]', type=valid_date, dest='from_date')
required.add_argument('--until', help='Records until. [YYYY-mm-dd HH:MM:SS]', type=valid_date, dest='until_date')
optional = parser.add_argument_group('output')
optional.add_argument('--export', help='Export data format. [json] [marc] [xml]', type=valid_format)
optional.add_argument('--display', help='Display output format. [ident] [json] [marc]', nargs='?', type=valid_display, const='ident')
args = parser.parse_args()

if args.get == 'record':
	if not args.set:
		parser.error('argument --set is required.')
	if not args.from_date:
		parser.error('argument --from is required.')
	if not args.until_date:
		parser.error('argument --until is required.')

# INIT -------------------

try:
	log = open(LOG,'a',0)
except:
	print("Read only FS exiting..")
	exit(1)

registry = MetadataRegistry()
registry.registerReader('marc21', MarcXML)

oai = Client(URL, registry)

try:
	if args.get == 'record':
		records = oai.listRecords(metadataPrefix='marc21', set=args.set, from_=args.from_date, until=args.until_date)
	if args.get == 'set':
		records = oai.listSets()
	if args.get == 'meta':
		records = oai.listMetadataFormats()
except:
	print('No records.')
	sys.exit(1)

if args.get == 'record': print('Validating..')
if args.display or args.get != 'record': print('------------------')

# MAIN -------------------

counter = 0

for record in records:

	if args.get == 'set' or args.get == 'meta':
		print(record[0])
		counter+=1
		continue

	header = record[0]
	metadata = record[1]
	
	# skip deleted records
	if header.isDeleted(): continue

	# retry missing metadata(?)
	if not metadata:
		print(header.identifier() + ' Missing matadata. Retrying..')
		retry = oai.getRecord(metadataPrefix='marc21', identifier=header.identifier())
		if not retry[1]:
			print(header.identifier() + ' Missing retry metadata.')
			continue
		else:
			header = retry[0]
			metadata = retry[1]

	# DISPLAY ------------------

	if args.display:
		if args.display == 'ident':
			print(header.identifier())
		if args.display == 'json':
			print(metadata.as_json(indent=4, sort_keys=True))
		if args.display == 'marc':
			print(metadata)

	# VALIDATION ------------------
	
	#TEST: TAG EXISTS
	if not '001' in metadata: log.write(header.identifier() + ' Missing 001 tag.\n')
	#TEST: TAG SUBFIELD EXISTS
	if '100' in metadata:
		if not('a' and 'd' and '7') in metadata['100']:
			log.write(header.identifier() + ' Missing a,d,7 subfield group in 100 tag.\n')
	#TEST: TAG + TAG SUBFIELD EXISTS
	if '072' in metadata:
		if 'x' in metadata['072']:
			if not '245' in metadata:
				log.write(header.identifier() + ' Missing 245 tag when x subfield in 072 tag.\n')
	#TEST: EQUAL VALUE
	if '100' in metadata:
		if '260' in metadata:
			if metadata['100'].value() != metadata['260'].value():
				log.write(header.identifier() + ' Value of 100 and 260 not equal.\n')
	#TEST: VALUE IN LIST
	LIST = ('auto','kolo','vlak')
	if '260' in metadata:
		if not metadata['260'].value() in LIST:
				log.write(header.identifier() + ' Value of 260 not in list.\n')
	#TEST: PRINT VALUE FROM LIST
	for TAG in ('001','005','007'):
		if TAG in metadata:
			log.write(header.identifier() + ' Tag ' + TAG + ' value: ' + metadata[TAG].value() + '\n')
	#TEST: VALUE DATE FORMAT
	if '001' in metadata:
		if not re.match('\d+', metadata['001'].value()):
			log.write(header.identifier() + ' Tag 001 invalid data format.\n')

	# EXPORT -------------------

	if args.export:
		try:
			os.mkdir('export')
			os.mkdir('export/' + args.export)
		except: pass
		if args.export == 'marc':# MARC 21
			writer = MARCWriter(open('export/marc/' + header.identifier() + '.dat', 'wb'))
			writer.write(metadata)
			writer.close()
		if args.export == 'json':# JSON
			writer = JSONWriter(open('export/json/'+ header.identifier() + '.json', 'wt'))
			writer.write(metadata)
			writer.close()
		if args.export == 'xml':# MARCXML
			writer = XMLWriter(open('export/xml/' + header.identifier() + '.xml', 'wb'))
			writer.write(metadata)
			writer.close()

	counter+=1

# EXIT -------------------
log.write('TOTAL: ' + str(counter) + '\n')
log.close()
if args.display or args.get != 'record': print('------------------')
print('Done.')
print('Total: ' + str(counter))

