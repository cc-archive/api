#!/bin/sh

mv ../../licenses.rdf ../../licenses.rdf.old
/usr/local/python241/bin/python makerdf.py -v -l ../licenses.xml -o ../../licenses.rdf

