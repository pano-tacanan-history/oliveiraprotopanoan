from collections import defaultdict
import re

def block(number, text, ddct):
    #print(text)
    concept_entries = []
    line_list = text.split(":")
    # print(line_list)
    # print(number)
    idf = line_list[0]
    #print(idf)
    rest = line_list[1:]
    #print(rest)
    for entry in rest:
        #print(entry)
        lang = [x for x in entry.split() if x]
        #print(lang)
        lng = lang[0]
        #print(lng)
        new_entry1 = " ".join(entry.split(" ")[1:])
        new_entry2 = " ".join(entry.split(" ")[2:])
        new_entry3 = list(new_entry2.split(" "))
        #print(new_entry3)
        concepts = new_entry2[new_entry2.find("‘") + 1:new_entry2.find("’")]
        if not "‘" in new_entry2:
            concepts = ''
        #print(concepts)
        concepts_2 = list(concepts.split(" "))
        #concepts_2 = " ".join(concepts.split())
        #print(type(concepts_2))
        #print(concepts_2)
        new_entry4 = [x for x in new_entry3 if x not in concepts_2]
        #forms = list(new_entry3.split(" "))
        #forms = "".join(new_entry3)
        #print(type(new_entry4))
        #print(new_entry4)
        #forms = list(new_entry3.split())
        #print(type(forms))
       # print(forms)
        #print("Language: {0} | entry: {1} | concept: {2}".format(lng, forms, concepts_2))



    #entry_list = []

    #for line in line_list:
        #print(line)
    #    if line == idf:
     #       protoform = line.split("‘")[0]
      #      protoform = protoform.split("(")[0]
            #print(protoform)
       #     pass
        #else:
         #   lang = line.split(" ")
            #print(lang)
          #  while ("" in lang):
           #     lang.remove("")
                #print(lang)


            #if "‘" in line:
                #print(line)
        #source = line[line.find("(") + 1:line.find(")")]
        # print(source)
        # if not source:
           # source = ''


        # print(f"{protoform} || {concept} || {source} ")
    #    for entry in line_list:
    #        print(entry)
    #        concept_entries.append(entry)
    #        break


ddct = defaultdict(list)
text = open('raw_oliveira.txt', 'r', encoding="utf8").read()
text = text.split("\n")
#print(text)
for l in text:
    l_splitted = l.split(".")
    start = l_splitted[0]
    final_entry = l_splitted[1:]
    block(start, "".join(final_entry), ddct)

    # break


# parse(text)



#text = open('raw_oliveira.txt', 'r', encoding="utf8").read()
#for l in text:
    #start = l.split(":")[0]
#print(start)
