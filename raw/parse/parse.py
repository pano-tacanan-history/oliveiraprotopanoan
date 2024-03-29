import re
from csvw.dsv import UnicodeDictReader
from collections import OrderedDict
import codecs
from lingpy import *

# load and apply replacements file
with open("replacements.tsv", encoding="utf8") as f:
    rep = {}
    for line in f.readlines():
        a, b = line.split("\t")
        if a != "CHAR":
            rep[eval('"'+a+'"')] = b.strip()


concept_replace = {}
with UnicodeDictReader("concept_replacements.tsv", delimiter='\t') as reader:
    for line in reader:
        concept_replace[line["OLD"]] = line["NEW"]

source_replace = {}
with UnicodeDictReader("source_replacements.tsv", delimiter='\t') as reader:
    for line in reader:
        # print(line)
        source_replace[line["OLD"]] = line["NEW"]

# load languages to check entries
with codecs.open("../../etc/languages.tsv", "r", "utf-8") as f:
    langs = {}
    for row in f:
        ents = row.split("\t")
        langs[ents[2]] = ents[1]

# load the data and parse it directly
bad_lines = []
bad_entries = []
# bracket_count = 0
oid = 1
with open("raw_oliveira-mod.txt", encoding="utf-8") as f:
    data = OrderedDict()
    additional_comments = []
    for line in f:
        line = "".join([rep.get(c, c) for c in line])
        # get first parts with indices
        idx, rest = line[:line.index(".")], line[line.index(".")+1:].strip()

        # if "(también" in line:
        #     print(line)

        # we ignore lines that are difficult
        if idx.startswith("!"):
            additional_comments.append(line)

        else:
            # start by separating proto-forms
            proto, rest = rest[:line.index(" : ")-3].strip(), rest[rest.index(" : ")+3:]

            # proto-form and concept
            if "‘" in proto:
                pform, pconcept = proto.strip()[:-1].split("‘")
                pconcept = pconcept.strip().strip("’")
                pform = pform.strip()
                if ":" in pconcept:
                    bad_lines += [idx]
            else:
                # take concept declared previously
                pform = proto.strip()
            # print(idx, pform, pconcept)
            if pconcept.startswith("**"):
                proto_conc = pconcept[2:]
                concept_uncertain = "1"
            else:
                proto_conc = pconcept
                concept_uncertain = "0"

            proto_conc = re.sub("  ", " ", proto_conc)
            proto_conc = proto_conc.replace(";;", ",")
            pform = pform.replace("*", "")

            if proto_conc in concept_replace:
                proto_conc = concept_replace[proto_conc]

            proto_tokens = " ".join(ipa2tokens(pform))
            data[oid] = [
                "§"+idx,
                "Proto-Panoan",
                "Proto",
                proto_conc,
                "",  # added from proto - not relevant
                concept_uncertain,
                pform,  # Value
                "",  # Uncertainty
                proto_tokens,  # Tokens
                "",  # Note
                "Oliveira2014",  # Source
                pform.replace("*", ""),  # pform
                pconcept.replace(";;", ","),  # pconcept
                proto  # whole entry
                ]
            oid += 1

            # split entries now to get individual entries here with regexes
            for entry in rest.split(" : "):
                if (":" in entry and not "::" in entry) or not " " in entry:
                    bad_entries += [(idx, entry)]
                else:
                    entry = entry.replace("::", ":")
                    # print(entry)
                    bad_entry = False
                    language = entry[:entry.index(" ")]
                    if language in langs:
                        erest = entry[entry.index(" "):].strip()
                        if "," in erest:
                            erests = [x.strip() for x in erest.split(",")]
                        else:
                            erests = [erest]
                            # print(erest)
                        for erest in erests:
                            erest = erest.replace(";;", ",")
                            if "‘" in erest:
                                try:
                                    form, concept = erest.split("‘")
                                    form = form.strip()
                                    if concept.endswith("’"):
                                        concept = concept[:-1]
                                        note = ""
                                    else:
                                        if "’" in concept:
                                            note = concept.split("’")[1]
                                            concept = concept.split("’")[0]
                                        else:
                                            note = ""
                                except:
                                    if entry == "Ksh ʔotanɔɔ ‘demonio del bosque’ (nɔɔ < nawa ‘gente’; juego 261)":
                                        form = "ʔotanɔɔ"
                                        concept = "demonio del bosque"
                                        note = "nɔɔ < nawa ‘gente’,  juego 261"
                                    elif entry == "Kn pisika (pisi- silbar como la serpiente)":
                                        form = "pisika"
                                        concept = "esp. de cobra"
                                        note = "pisi- 'silbar como la serpiente'"
                                    else:
                                        bad_entries += [(idx, entry)]
                                        bad_entry = True
                            else:
                                if "(" in erest and ")" in erest:
                                    try:
                                        form, note = erest.split("(")
                                        note = note.strip(")")
                                    except:
                                        bad_entries += [(idx, entry)]
                                        bad_entry = True
                                else:
                                    form = erest
                                    concept = "!!"+pconcept
                                    note = ""
                            if not bad_entry:
                                try:
                                    tokens = " ".join(ipa2tokens(form))
                                except:
                                    tokens = ""
                                # form uncertainty
                                if form.startswith("**"):
                                    form = form[2:]
                                    uncertainty = "1"
                                else:
                                    uncertainty = ""
                                # concept from base form
                                if concept.startswith("!!"):
                                    concept = concept[2:]
                                    from_base = "1"
                                else:
                                    from_base = ""
                                if concept.startswith("**"):
                                    concept = concept[2:]
                                    concept_uncertain = "1"
                                else:
                                    concept_uncertain = ""

                                # Compile sources from notes
                                if re.search("[A-Z]*, [0-9]{4}", note):
                                    if re.search("[a-z]", note):
                                        pass
                                    else:
                                        source = re.sub(r'(\(|\)|,|\s|\.)', '', note)
                                        source = re.sub(r'([A-Z]+);([A-Z]+)', '\\1', source)
                                        # print(source)
                                        note = ""
                                    # replace sources through replacement table

                                else:
                                    source = ""
                                    # print(note)

                                if source in source_replace:
                                    source = source_replace[source]
                                    # print(source)

                                if "II" in form:
                                    note = "II"
                                    form = form.replace("II", "")
                                if "I" in form and language == "Amawaka":
                                    note = "I"
                                    form = form.replace("I", "")

                                concept = re.sub("  ", " ", concept)
                                concept = re.sub("^ ", "", concept)
                                concept = concept.replace(";;", ",")

                                if concept in concept_replace:
                                    concept = concept_replace[concept]

                                data[oid] = [
                                    "§"+idx,
                                    langs[language],
                                    language,
                                    concept,
                                    from_base,
                                    concept_uncertain,
                                    form,
                                    uncertainty,
                                    tokens,
                                    note.strip("(").strip(")"),
                                    source,
                                    pform,
                                    pconcept.replace(";;", ","),
                                    entry
                                    ]
                                # if "[" in form:
                                #   print(form)
                                #   bracket_count += 1
                                #   print(idx, language, form, concept)
                                oid += 1
                    else:
                        bad_entries += [(idx, entry)]


print("")

# print out bad lines
print("# Found {0} lines without spaces\n".format(len(bad_lines)))
print("Number | Line\n--- | ---")
for i, line in enumerate(bad_lines):
    print("{0:5} | {1}".format(i+1, line))
print("")
print("# Found {0} entries with individual problematic entries\n".format(
    len(bad_entries)))
print("Number | Line ID | Entry\n--- | --- | ---")
for i, (a, b) in enumerate(bad_entries):
    print("{0} | {1:20} | {2}".format(i+1, a, b))

with codecs.open("../parsed-entries2.tsv", "w", "utf-8") as f:
    f.write("\t".join([
        "ID",
        "IDX",
        "DOCULECT",
        "DOCULECTID",
        "CONCEPT",
        "CONCEPT_FROM_PROTO",
        "CONCEPT_ADDED",
        "VALUE",
        "VALUE_UNCERTAIN",
        "TOKENS",
        "NOTE",
        "SOURCE",
        "PROTOFORM",
        "PROTOCONCEPT",
        "ENTRY_IN_SOURCE"
        ])+"\n")
    for idx, vals in data.items():
        if vals[6].strip() in ["--"] or not vals[6].strip():
            pass
        else:
            f.write(str(idx)+"\t"+"\t".join(vals)+"\n")


with open('../additional_comments.txt', 'w', encoding="utf8") as file:
    file.write('\n'.join(str(i) for i in additional_comments))
# print(bracket_count)
