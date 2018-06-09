######################################################
# Program: parseGO_Object.py
# Author: Alekhya Akkunuri
# Date: 11-21-2017
# Description: This program parses the Gene 
# Ontology file as objects and puts the results in a dictionary
######################################################

import re

go_dictionary = {}
output = open("outputGO_OO.txt", "w")

class GeneOntology(object):
      # Constructor
      def __init__(self, contents):
          # search for the first match of the fields in the text using re.search
          ID = re.search(r"^id:\s+(.*?)\n", contents)
          name = re.search(r"name:\s+(.*?)\n", contents)
          namespace = re.search(r"namespace:\s+(.*?)\n", contents)
          # check to make sure ID was found
          if ID:
             self.ID = ID.group(1)
             self.name = name.group(1)
             self.namespace = namespace.group(1)
             # find all the is_a per record 
             self.isa = re.findall(r"is_a:\s+(.*?)\n", contents)     
          else:
               self.ID = None
      # method to store the records in required format      
      def store_all(self):
          output.write(self.ID + "\t" +  go_dictionary[self.ID].namespace + "\n\t" + go_dictionary[self.ID].name)
          output.write("\n")
          for fields in go_dictionary[self.ID].isa:
              output.write("\t" + fields)
              output.write("\n")
          output.write("\n")

# create a function that reads in the file and splits it into records.
def split_file(my_file):
    with open(my_file) as f:
         file_contents = f.read()
         # find every match in the text and split into records
         split_records =  re.findall(r"(id:.*?)\[Term" ,file_contents, re.DOTALL)
         for file_contents in split_records:
             # add each valid GO term to a dictionary
             go = GeneOntology(file_contents)
             go_dictionary[go.ID] = go
             go.store_all()
     
split_file(my_file = "go-basic.obo")
