# pip install geopy
# https://pypi.org/project/geopy/

from geopy.distance import geodesic
import statistics

class MissingDataError(Exception):
    """Exception raised because required data is missing.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message


def distance(pic, cordis_data, rorId, ror_data):
    cordis_org_metadata = cordis_data[pic]
    ror_org_metadata = ror_data[rorId]

    if "location" not in cordis_org_metadata:
        raise MissingDataError("No location information for PIC {} in CORDIS data".format(pic))

    cordis_location = cordis_org_metadata["location"]
    (cordis_latitude, cordis_longitude) = cordis_location.split(",")
    cordis_loc = (cordis_latitude, cordis_longitude)

    if "location" not in ror_org_metadata:
        raise MissingDataError("No location information for {} in ROR datadump".format(rorId))

    ror_loc = (ror_org_metadata["location"]["lat"], ror_org_metadata["location"]["long"])

    return geodesic(cordis_loc, ror_loc).km


def build_statistics(mapping, cordis_data, ror_data):
    distances=[]
    for pic in mapping:
        rorId = mapping[pic]["ror"]

        try:
            dist = distance(pic, cordis_data, rorId, ror_data)
            distances.append(dist)
        except MissingDataError:
            pass

    median = statistics.median(distances)
    print("MEDIAN DISTANCE: {} km".format(median))
    # TODO Calculate average deviation
    # TODO Return discriminator as distance predicate.


def validate(mapping, cordis_data, ror_data):
    accepted={}

    build_statistics(mapping, cordis_data, ror_data)

    for pic in mapping:
        rorId = mapping[pic]["ror"]

        try:
            dist = distance(pic, cordis_data, rorId, ror_data)

            # TODO apply discriminator

            accepted[pic] = rorId
        except MissingDataError as error:
            print("Skipping {} --> {}: {}".format(pic, rorId, error))
            pass

    return accepted
