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
import cordis
import wikidata

if len(sys.argv) != 2:
    print("Need argument: CSV projects file (e.g., \"data/organization.csv\")", file=sys.stderr)
    sys.exit(1)

cordis_data = cordis.parse_organization(sys.argv[1])

print("Loaded {} organisations from CORDIS data".format(len(cordis_data)))

vat_to_ror = wikidata.vat_to_ror()
print("Wikidata has {} organisations with EU VAT and ROR information".format(len(vat_to_ror)))

skip_no_vat=0
skip_wikidata_entry_missing=0

mapping={}
for id in cordis_data:
    metadata = cordis_data[id]
    if "vat" not in metadata:
        skip_no_vat+=1
        continue

    vat = metadata["vat"]

    if vat not in vat_to_ror:
        skip_wikidata_entry_missing+=1
        continue

    mapping[id] = vat_to_ror[vat]

print("Summary:")
print("    {} skipped because CORDIS has no EU VAT information".format(skip_no_vat))
print("    {} skipped because Wikidata has insufficient data".format(skip_wikidata_entry_missing))
print("    {} mapped".format(len(mapping)))

json_object = json.dumps(mapping, indent = 4)
with open('pic-to-ror.json', "wt") as output:
    output.write(json_object)
print("Mapped organisations written as \"pic-to-ror.json\".")
