#!/usr/bin/python
#
# JSON to MARC convertor.
# 

# INCLUDE -----------------

from __future__ import print_function

import argparse,json,sys,os,re

from pymarc import JSONReader,JSONWriter,MARCWriter,XMLWriter
from pymarc.record import Record
from pymarc.field import Field

# VAR -----------------

LOG='json-marc.log'

# DEF -----------------

def valid_dir(s):
	if os.path.isdir(s): return s
	else:
		msg = 'Invalid directory.'
		raise argparse.ArgumentTypeError(msg)

def valid_format(s):
	if s in ('json', 'marc', 'xml'): return s
	else:
		msg = 'Invalid export format.'
		raise argparse.ArgumentTypeError(msg)

#  ARG -------------------

#parser = argparse.ArgumentParser(description="JSON - MARC Convertor.")
#required = parser.add_argument_group('required arguments')
#required.add_argument('--in', help='Import directory.', dest='in_dir', type=valid_dir, required=True)
#required.add_argument('--format', help='Export format. [json] [marc] [xml]', type=valid_format, required=True)
#args = parser.parse_args()

# INIT -----------------

#try:
#	log = open(LOG,'a',0)
#except:
#	print('Read only FS exiting.')
#	sys.exit(1)

# MAIN -----------------

# LOAD BROKEN JSON SOURCE

with open('in/in2.json','rb') as f:
	j = json.loads(f.read(), strict=False)# ignore control char garbage

#print(json.dumps(j, indent=2))
#print(j['_rev'])
#print(j['drawer'])

# UPDATE TEMPLATE

# THE JSON WAY
#
#          Core: {'fields':[], 'leader':'foo'}
#   Basic field: {'001':'foo'}
# Complex field: {'040':{'ind1':'', 'ind2':'', 'subfields':[{'a':''}, {'b':''}]}}
#

template = {'leader':'foo', 'fields':[{'001':'foo'}]}
reader = JSONReader(json.dumps(template))

for record in reader: print(record)

# THE RECORD WAY
#
# field = Field(tag='001',data='foo')
# field = Field(tag='040', indicators=['1','0'], subfields=['a','','b',''])
#

record = Record()
record.leader = 'foo'
field = Field(tag='001', data='foo')
record.add_field(field)

print(record)

# EXPORT -----------------

#try:
#	os.mkdir('export')
#	os.mkdir('export/' + args.format)
#except: pass

#for record in reader:
#	if args.format == 'json':# JSON
#		writer = JSONWriter(open('export/json/' + re.sub('(.*)\.json', '\\1', f) + '.json', 'wt'))
#		writer.write(record)
#		writer.close()
#	if args.format == 'marc':# MARC21
#		writer = MARCWriter(open('export/marc/' + re.sub('(.*)\.json', '\\1', f)  + '.dat', 'wb'))
#		writer.write(record)
#		writer.close()
#	if args.format == 'xml':# MARCXML
#		writer = XMLWriter(open('export/xml/' + re.sub('(.*)\.json', '\\1', f) + '.xml', 'wb'))
#		writer.write(record)
#		writer.close()

# EXIT -------------------

#log.close()
#print('Done.')

