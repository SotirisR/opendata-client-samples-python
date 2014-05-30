#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import json
import opendata

# Decision metadata
json_file = open('SampleDecisionMetadata.json', 'r')
metadata = json.load(json_file)
json_file.close()

# Decision document
pdf_file = open('SampleDecision.pdf', 'rb')

# Attachments
att1 = open('Attachment.docx', 'rb')
att2 = open('Attachment.xlsx', 'rb')
attachments = [(att1, 'First attachment'), (att2, 'Second attachment')]

# Send request
client = opendata.OpendataClient()
client.set_credentials('10599_api', 'User@10599')
response = client.submit_decision(metadata, pdf_file, attachments)

pdf_file.close()
att1.close()
att2.close()

if response.status_code == 200:
    decision = response.json()
    print "ΑΔΑ: " + decision['ada'].encode('utf8')
elif response.status_code == 400:
    print "Σφάλμα στην υποβολή της πράξης"
    err_json = response.json()
    for err in err_json['errors']:
        print("{0}: {1}".format(err['errorCode'], err['errorMessage'].encode('utf8')))
elif response.status_code == 401:
    print "Σφάλμα αυθεντικοποίησης"
elif response.status_code == 403:
    print "Απαγόρευση πρόσβασης"
else:
    print("ERROR " + str(response.status_code))

