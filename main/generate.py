##########################################################################################
## Semantic Web Form                                                                    ##
## Authors : Chris Andrew, Santhoshini Reddy                                            ##
## Email: chris.g14@iiits.in ; santhoshini.g14@iiits.in                                 ##
## Github: https://github.com/chrizandr ; https://github.com/Sanny26                    ##
###################################################################                     ##
## Description: This project was developed as part of the SEFP course at IIIT Sri City  ##
## All code is available for free usage for educational purposes                        ##
## Authors do not authorize commercial use of the source code                           ##
##########################################################################################

# Script is to generate the source RDF/OWL code for a given set of classes, attributes and their values.

################### Imports ##################
# NONE
##################### Global ####################

filestring = """<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE rdf:RDF [
  <!ENTITY xsd "http://www.w3.org/2001/XMLSchema#">
  <!ENTITY rdf "http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <!ENTITY rdfs "http://www.w3.org/2000/01/rdf-schema#">
  <!ENTITY owl "http://www.w3.org/2002/07/owl#">
]>

<rdf:RDF
  xmlns:xsd="&xsd;"
  xmlns:rdf="&rdf;"
  xmlns:rdfs="&rdfs;"
  xmlns:owl="&owl;"
>
<owlx:Ontology owlx:name="#instance"
  xmlns:owlx="http://www.w3.org/2003/05/owl-xml">
%s
</owlx:Ontology>
</rdf:RDF>"""


new_individual =  '<owlx:Individual owlx:name="%s">'
individual_type = '<owlx:type owlx:name="%s"/>'
obj_prop = '<owlx:ObjectPropertyValue owlx:property="%s">'
old_individual = '<owlx:Individual owlx:name="#%s" />'
end_obj_prop = '</owlx:ObjectPropertyValue>'
end_individual = '</owlx:Individual>'
data_prop = '<owlx:DataPropertyValue owlx:property="%s">'
data_val = '<owlx:DataValue owlx:datatype="&xsd;%s">%s</owlx:DataValue>'
end_data_prop = '</owlx:DataPropertyValue>'

##################### Source ####################

def get_file(obj):
    del obj['csrfmiddlewaretoken']
    finalstring = ''
    flag = 0
    for key,value in obj.iteritems():
        newentry = key.split('_')

        if newentry[0] == 'c':
            if flag == 0:
                flag = 1
                finalstring += new_individual%(value) + "\n\t" + individual_type%(newentry[1]) + "\n"
            else:
                finalstring += end_individual + "\n\n"
                finalstring += new_individual%(value) + "\n\t" + individual_type%(newentry[1]) + "\n"

        elif newentry[0] == 'o':
            finalstring += "\t" + obj_prop%(newentry[1]) + "\n\t\t" + old_individual%(value) +"\n\t" + end_obj_prop + "\n"

        elif newentry[0] == 'd':
            finalstring += "\t" + data_prop%(newentry[2]) + "\n\t\t" + data_val%(newentry[1],value) + "\n\t" + end_data_prop + "\n"
    finalstring += end_individual + "\n"
    result = filestring%(finalstring)
    return result
