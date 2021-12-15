# Copyright 2021 A. Paul Millar
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# This module is responsible for parsing the CORDIS dataset; in
# particular, the file 'organization.csv' which contains information
# about organisation participation within H2020-funded projects.

import csv
import re
import json
import sys

keyMapping={
    "vat": "vatNumber",
    "name": "name",
    "shortName": "shortName",
    "street": "street",
    "postcode": "postCode",
    "city": "city",
    "country": "country",
    "location": "geolocation",
    "url": "organizationURL"}

def normalise_vatNumber(id, value):
    if value == "MISSING":
        return ""
    return value.replace(" ", "")

def normalise_street(id, value):
    return " ".join(value.split())

def normalise_city(id, value):
    return value.upper()
    
def normalise_name(id, value):
    return " ".join(value.split()).upper()
    
def normalise_shortName(id, value):
    if id == "997579817": # Sometimes the short name includes country
        return value.split('-')[0]
    return value
    
def normalise_postCode(id, value):
    if id == "999851460": # Confusion on dash in code
        return value.replace(" ", "-")
    elif value == "None": # "None" used as a place-holder
        return ""
    else:
        return value
    
def normalise_country(id, value):
    match = re.match(r"(\w+);\1", value) # Entries like "ES;ES"
    if match:
        return match.group(1)
    else:
        return value
        
def normalise(id, type, value):
    """Normalise and otherwise pre-process input data."""
    switcher = {
        "vatNumber": normalise_vatNumber,
        "street": normalise_street,
        "name": normalise_name,
        "shortName": normalise_shortName,
        "country": normalise_country,
        "city": normalise_city,
        "postCode": normalise_postCode
        }
    fn = switcher.get(type, lambda i,v: v)
    return fn(id, value)

def reconcile(id, type, existing, existingValue, newValue):
    """How to handle inconsistencies in the input data."""
    print("Diff in {} for {} detected (\"{}\" != \"{}\"), using \"{}\"".format(thisKey, id, existingValue, newValue, existingValue), \
          file=sys.stderr)
    return existingValue

def is_known_bad(id, row):
    """Whether to reject an organisation's association with a project
    This is sometimes needed because the entry contain out-of-date
    information about an institute."""    
    projectID = row['projectID']

    return (id == "934242018" and \
            (projectID=="812780" or \
             projectID=="884823" or \
             projectID=="955643" or \
             projectID=="845036" or \
             projectID=="752277" or \
             projectID=="840577" or \
             projectID=="739759" or \
             projectID=="842299" or \
             projectID=="675737" or \
             projectID=="813873" or \
             projectID=="859890")) or \
             (id == "999561915" and projectID == "633053") or \
             (id == "999969412" and projectID == "633053")

def parse_organization(filename):
    """Parse an 'organization.csv' file from CORDIS data dump.  This
       function returns the information as a dict, with each
       organisation is represented as a single entry in this dict.
       The dict's key is the organisation's PIC and the value is a
       dict that contains metadata about the organisation.

       Not all information is available for all organisations.  If
       some data is missing then the organisation's metadata dict is
       missing the corresponding key.

       The following keys may be defined in an organisation's dict:

           vat        --  The EU VAT number.
           name       --  The full name for this organisation.
           shortName  --  An abbreviation or some shorter version
                          of the organisation's name.
           street     --  The first line of the organisation address,
                          typically containing the name of the street
                          and a street/house number.
           postcode   --  The postcode part of the organisation
                          address.
           city       --  The city part of the organisation address.
           country    --  The country, using XX encoding.
           location   --  Comma-separated decimal longitude and
                          latitute values.
           url        --  A contact URL (or just host name).
    """
    data={}

    with open(sys.argv[1], newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            id=row['organisationID']
        
            if is_known_bad(id, row):
                continue
        
            if id not in data:
                details={}
                for thisKey in keyMapping:
                    cordisKey = keyMapping[thisKey]
                    value = normalise(id, cordisKey, row[cordisKey])
                    if value:
                        details[thisKey] = value
                        data[id] = details;
                continue

            details = data[id]
            for thisKey in keyMapping:
                cordisKey = keyMapping[thisKey]
                newValue = normalise(id, cordisKey, row[cordisKey])
                if not newValue:
                    continue
                
                if thisKey not in details:
                    details[thisKey] = newValue
                    continue
                
                existingValue = details[thisKey]
                if existingValue != newValue:
                    details[thisKey] = reconcile(id, thisKey, details, existingValue, newValue)

    return data
