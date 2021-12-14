
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


The goal is to provide a database of PIC to ROR values.  These will be
placed somewhere so they may be freely downloaded.

Therefore, although the code should be runnable by anyone, the
intention is not that people need to run this code to obtain the list
of corresponding identifiers.

