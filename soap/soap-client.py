#!/usr/bin/env python
"""
soap-client.py
$Id$

Creative Commons SOAP API sample implementation (command line)
(c) 2004, Nathan R. Yergler, Creative Commons
"""

import SOAPpy
import sys

server = SOAPpy.SOAPProxy('http://api.creativecommons.org/soap')

licenses = server.licenses()

for l in licenses:
    print l

print

l = raw_input("Enter your desired license:")
print

answers = {}
for f in server.fields(l):

    f_info = dict(server.fieldDetail(l, f))

    print f_info['label'],
    if f_info['type'] == 'enum':
        print " (",
        for e in server.fieldEnum(l, f):
            foo = dict(e)
            print foo['id'], ", ",

        print "): ",

    answers[f] = raw_input()

print answers

print server.getLicense(l, answers)
