#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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

import sys
import json
import datetime
import git
import cordis
import wikidata
import ror
import validation

# pip install gitpython

if len(sys.argv) != 2:
    print("Need argument: CSV projects file (e.g., \"data/organization.csv\")", file=sys.stderr)
    sys.exit(1)

ror_data = ror.parse_datadump("data/ror-data.json") # FIXME make this configurable.
print("Loaded {} organisations from ROR data dump".format(len(ror_data)))

cordis_data = cordis.parse_organization(sys.argv[1])
print("Loaded {} organisations from CORDIS data".format(len(cordis_data)))

wikidata_orgs_by_pic = wikidata.pic_to_ror()
print("Wikidata has {} organisations with PIC and ROR information".format(len(wikidata_orgs_by_pic)))

wikidata_orgs_by_vat = wikidata.vat_to_ror()
print("Wikidata has {} organisations with EU VAT and ROR information".format(len(wikidata_orgs_by_vat)))

skip_no_vat=0
skip_wikidata_entry_missing=0
found_by_pic=0
found_by_vat=0

#
#  Build mapping from PIC to ROR
#
mapping={}
for pic in cordis_data:

    # Wikidata already knows some mappings
    if pic in wikidata_orgs_by_pic:
        wikidata = wikidata_orgs_by_pic[pic]
        mapping[pic] = {"ror": wikidata["ror"],
                       "context": {
                           "matched-by": "PIC",
                           "source": "wikidata",
                           "id": wikidata["id"]
                       }}
        found_by_pic += 1
        continue

    metadata = cordis_data[pic]

    # Use EU VAT number to identify organisations without PIC
    if "vat" in metadata:
        vat = metadata["vat"]
        if vat in wikidata_orgs_by_vat:
            wikidata = wikidata_orgs_by_vat[vat]
            mapping[pic] = {"ror": wikidata["ror"],
                           "context": {
                               "matched-by": "VAT",
                               "source": "wikidata",
                               "id": wikidata["id"]
                           }}
            found_by_vat += 1
            continue

    # TODO: try something else, match by name perhaps?


#
# Validate the results
#

# 1. remove inconsistent results
to_remove = []
for pic in mapping:
    match = mapping[pic]
    rorId = match["ror"]
    if pic not in cordis_data:
        print("Unknown PIC {}".format(pic))
        to_remove.append(pic)
        continue

    if rorId not in ror_data:
        print("Unknown ROR ID {} for match {}".format(
              rorId, match["context"]))
        to_remove.append(pic)
        continue

for pic in to_remove:
    del mapping[pic]


#
# 2. Run validator
#
results = validation.validate(mapping, cordis_data, ror_data)

print("Summary:")
print("    {} Total mapped".format(len(results)))

output={}
output["generated"] = datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()
repo = git.repo.Repo('./')
output["generator"] = repo.git.describe()
output["count"] = len(results)
output["mapping"] = results

json_object = json.dumps(output, indent = 4)
with open('pic-to-ror.json', "wt") as output:
    output.write(json_object)
print("Mapped organisations written as \"pic-to-ror.json\".")
