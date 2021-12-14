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

organisation={}

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


if len(sys.argv) != 2:
    print("Need argument: CSV projects file (e.g., \"data/project/organization.csv\"", file=sys.stderr)
    sys.exit(1)
    
with open(sys.argv[1], newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        id=row['organisationID']
        
        if is_known_bad(id, row):
            continue
        
        if id not in organisation:
            details={}
            for thisKey in keyMapping:
                cordisKey = keyMapping[thisKey]
                value = normalise(id, cordisKey, row[cordisKey])
                if value:
                    details[thisKey] = value
            organisation[id] = details;
            continue
        
        details = organisation[id]
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


print(json.dumps(organisation, indent = 4))
