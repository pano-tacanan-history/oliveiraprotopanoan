import csv
import re
from lingpy import Wordlist
from pysem.glosses import to_concepticon

wl = Wordlist("parsed-entries2.tsv")

proto_concepts = [[
    "GLOSS",
    "CONCEPTICON_ID",
    "CONCEPTICON_GLOSS",
    "PROTO_ID",
    "PROTO_CONCEPT"
    ]]

other_concepts = [[
    "GLOSS",
    "PROTO_ID",
    "PROTO_CONCEPT"
    ]]
concept_exists = []

for i in wl:
    ID = wl[i, "IDX"]
    concept = re.sub("  ", " ", wl[i, "concept"])
    concept = re.sub("^ ", "", wl[i, "concept"])

    # Proto-Concepts
    if wl[i, "doculect"] == "Proto-Panoan":
        PP = 1
        mapped = to_concepticon([{"gloss": concept}], language="pt")

        if mapped[concept]:
            cid, cgl = mapped[concept][0][:2]
        else:
            cid, cgl = "", ""

        proto_concepts.append([
            concept, cid, cgl, ID, PP
        ])

    # Other concepts
    elif (concept, ID) not in concept_exists:
        PP = 0
        other_concepts.append([
            concept, ID, PP
        ])

    concept_exists.append((concept, ID))

with open("../etc/other_concepts.tsv", "w", encoding="utf8") as file:
    writer = csv.writer(file, delimiter="\t")
    writer.writerows(other_concepts)

# with open("../etc/proto_concepts.tsv", "w", encoding="utf8") as file:
#     writer = csv.writer(file, delimiter="\t")
#     writer.writerows(proto_concepts)
