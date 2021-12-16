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
# This module is responsible for parsing the ROR dataset.

import json
import sys

def parse_datadump(filename):
    """Read the JSON information in a ROR data dump.  The returned value
       is

    """
    data={}

    with open(filename, newline='') as rorfile:
        ror_data = json.load(rorfile)
        for org in ror_data:
            id = org["id"]
            metadata = {}
            data[id] = metadata
            
            address = org["addresses"][0]
            longitude = address["lng"]
            latitude = address["lat"]
            metadata["location"] = {"long": longitude, "lat": latitude}
            
    return data
