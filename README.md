# Motivation

A
[PIC](https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/how-to-participate/participant-register)
(Participant Identification Code) is a unique identifier that the
European Union assigns to organisations that register when
participating in EU funding and tender opportunities.

The [ROR](https://ror.org/) (Research Organization Registry) is a
community-led project to assign a unique identifier for every research
organisation in the world.

Currently there is no link between an organisation's PIC and its ROR
identifier.

[An issue](https://github.com/ror-community/ror-api/issues/189) was
created, requesting that ROR metadata is updated so it may hold an
organisation's PIC.  This would be similar to ROR's support for other
external identifiers.

While updating ROR to include an organisation's PIC is the preferred
solution, it is not clear that this change matches ROR's vision.  ROR
is community-driven and such change would require consultation.
Additionally, (at time of writing) building the infrastructure to
maintain the existing ROR metadata is a higher priority changing the
data model is not a priority.

This repository exists to fill this gap.

It contains the code needed to generate a link between an
organisation's PIC and it's ROR identifier.

There are two main reasons why this repository exists:


  1. To document the process through which the two idenfiers are
     matched.

     This allows people to verify the methology, point out any
     problems, and potentially suggest ways of improving the output.


  2. By automating the process, the process may be re-run as more
     organisations are included in CORDIS and ROR.


The goal is to provide a database of PIC to ROR values.  The latest
results are available [from this
link](https://paulmillar.github.io/cordis/pic-to-ror.json).

Therefore, although the code should be runnable by anyone, the
intention is not that people need to run this code to obtain the list
of corresponding identifiers.


# Contents

This repository contains several files.  Here is a list of the most
important ones and what is their function.

<dl>
<dt><tt>bin/acquire-data</tt></dt>

<dd>Acquire CORDIS and ROR data dumps.  This caches data, so the same
function may be used to check for any updates.</dd>

<dt><tt>process.py</tt></dt>

<dd>Build a mapping of PIC to ROR identifiers and store the result as
the file <tt>pic-to-ror.json</tt></dd>

<dt><tt>print-cordis.py</tt></dt>

<dd>Parse the CORDIS <tt>organization.csv</tt> file from the data dump
and print the results.</dd>

<dt><tt>print-wikidata.py</tt></dt>

<dd>Query Wikidata for EU VAT number to ROR identifier mapping and
print the result.</dd>

<dt><tt>scan-wikidata-for-orphans</tt></dt>

<dd>This queries Wikidata for all organisations for which it has
a corresponding ROR identifier and then compares those identifiers
with those present in the ROR data dump.  This catches orphaned
links.</dd>
</dl>

# How to run

You will need to run `bin/acquire-data` at least once, to obtain the
CORDIS and ROR data dumps.

You can rerun this command to check for any updates.  This is safe
because the downloaded data is cached and the script checks to see if
the cached copy is up-to-date before downloading it.

Once you've have the CORDIS and ROR data dumps, run `process.py` to
generate the mapping file: `pic-to-ror.json`.
