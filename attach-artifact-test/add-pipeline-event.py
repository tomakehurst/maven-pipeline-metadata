#!/usr/bin/python

import json
import os
import sys
import getopt
from datetime import datetime

META_FILE_PATH='target/pipeline-metadata.json'

if len(sys.argv) < 3:
	print('Usage: ', sys.argv[0], ' <event> <triggeredBy> <notes>')
	sys.exit(2)

event=sys.argv[1]
triggeredBy=sys.argv[2]
notes=sys.argv[3]
date=datetime.now().strftime('%Y%m%dT%H:%M:%SZ')

print("Downloading existing pipeline metadata")
os.system('mvn -Ppipe-meta clean dependency:copy')

if os.path.isfile(META_FILE_PATH):
	pipelineMetaFile=open(META_FILE_PATH, 'r')
	metadata=json.load(pipelineMetaFile)
	pipelineMetaFile.close()
else:
	metadata=[]

metadata.append({ "event": event, "triggeredBy": triggeredBy, "date": date, "notes": notes })

pipelineMetaFile=open(META_FILE_PATH, 'w')
json.dump(metadata, pipelineMetaFile)
pipelineMetaFile.close()

print("Uploading updated pipeline metadata")
os.system('mvn -Ppipe-meta deploy:deploy-file')
