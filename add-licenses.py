#!/usr/bin/python

import lxml
from lxml import etree
import string
import sys

theSix=["by-nc","by","by-nc-nd","by-nc-sa","by-sa","by-nd"]

#Error-checking conditions.

if len(sys.argv)!=4:
    print "Usage: <script> <file> <version> <jurisdiction>"
    sys.exit()

if sys.argv[3].islower()!=1 and sys.argv[3]!='-':
    print "Usage: <script> <file> <version> <jurisdiction>"
    print "<jurisdiction> must be lower-case"
    sys.exit()

try:
    float(sys.argv[2])
except:
    print "Usage: <script> <file> <version> <jurisdiction>"
    print "<version> must be digit"
    sys.exit()

try:
    f=open(sys.argv[1],'r')
except:
    print "Usage: <script> <file> <version> <jurisdiction>"
    print "<file> must exist"
    sys.exit()

#Let's begin. First check: Find the six active licenses.

tree=etree.ElementTree(file=sys.argv[1])
root=tree.getroot()
firstit=root.getiterator('license')
for v in firstit:
    found=0
    if theSix.count(v.get('id'))>0:
        #When you find an active license, now check for an existing jurisdiction.
        print "Adding to "+v.get('id')+" license..."
        tempit=v.getiterator('jurisdiction')
        for w in tempit:
            if w.get('id')==sys.argv[3]:
                #If it's there, add in the new version.
                found=1
                print "Adding version "+sys.argv[2]+" to existing jurisdiction "+sys.argv[3]
                newelem=w.makeelement('version',None)
                newelem.set('id',sys.argv[2])
                j=''
                if sys.argv[3]!='-':
                    j=sys.argv[3]+'/'
                newelem.set('uri',"http://creativecommons.org/licenses/"+v.get('id')+'/'+sys.argv[2]+'/'+j)
                newelem.tail='\n'
                w.append(newelem)
        if found==0:
            #If it's not there, add a new jurisdiction too.
            print "Creating new jurisdiction "+sys.argv[2]
            newelem=v.makeelement('jurisdiction',None)
            newelem.set('id',sys.argv[3])
            newelem.text='\n'
            v.append(newelem)
            print "Adding version "+sys.argv[2]+" to new jurisdiction "+sys.argv[3]
            newelem2=newelem.makeelement('version',None)
            newelem2.set('id',sys.argv[2])
            j=''
            if sys.argv[3]!='-':
                j=sys.argv[3]+'/'
            newelem2.set('uri',"http://creativecommons.org/licenses/"+v.get('id')+'/'+sys.argv[2]+'/'+j)
            newelem2.tail='\n'
            newelem.append(newelem2)


#And write the new file.
fileopen=open(sys.argv[1],'w')
tree.write(fileopen)
