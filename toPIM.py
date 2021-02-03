import json
import requests
import csv
import collections
import pandas as pd
import time

#OWL Turtle format

def assemble_DataProperties(i):
    global main_content
    if 5 in range(len(main_content[i])):
        valueOfIndividual = main_content[i][5].replace('"', "'")
        #valueOfIndividual = valueOfIndividual.replace(".", ",")
        try:
            valueOfIndividual = str(float(valueOfIndividual))
        except:
            valueOfIndividual = '"'+ valueOfIndividual + '"'

        DataPropertiesOfIndividual = """;
                                                          <http://www.co-ode.org/ontologies/ont.owl#valor> """+ valueOfIndividual +""" .

"""
    else:
        DataPropertiesOfIndividual = """ .
                                                                   
"""                                   
    return(DataPropertiesOfIndividual)

def assemble_classes():
    key_component = ["ptolemy.actor.lib.gui.MonitorValue",
                    "ptolemy.data.expr.Parameter",
                    "ptolemy.actor.lib.DiscreteClock",
                    "ptolemy.actor.parameters.IntRangeParameter",
                    "ptolemy.actor.TypedCompositeActor",
                    "ptolemy.actor.lib.CurrentTime",
                    "ptolemy.actor.lib.Const",
                    "ptolemy.domains.continuous.kernel.ContinuousDirector",
                    "ptolemy.actor.lib.conversions.Round",
                    "ptolemy.actor.lib.gui.TimedPlotter",
                    "ptolemy.actor.lib.gui.Display",
                    "ptolemy.domains.modal.modal.ModalModel",
                    "ptolemy.domains.modal.kernel.State",
                    "ptolemy.actor.lib.Expression",
                    "ptolemy.actor.lib.MultiplyDivide",
                    "ptolemy.domains.modal.modal.ModalModel",
                    "ptolemy.domains.modal.kernel.State",
                    "ptolemy.domains.modal.kernel.Transition",
                    "ptolemy.actor.lib.BooleanSwitch",
                    "ptolemy.actor.lib.Counter",
                    "ptolemy.actor.lib.LookupTable",
                    "ptolemy.actor.lib.Discard",
                    "ptolemy.actor.lib.logic.LogicGate",
                    "ptolemy.actor.lib.AddSubtract",
                    "ptolemy.actor.lib.Limiter",
                    "ptolemy.actor.lib.Accumulator",     
                    "ptolemy.actor.lib.logic.Comparator",
                    "ptolemy.actor.lib.RecordUpdater",
                    "ptolemy.actor.lib.io.LineReader",
                    "ptolemy.actor.lib.string.StringSubstring",
                    "ptolemy.actor.lib.conversions.ExpressionToToken",
                    "ptolemy.actor.lib.ElementsToArray",
                    "ptolemy.actor.TypedCompositeActor",
                    "ptolemy.actor.TypedIORelation"
                    ]
    classes_pim = ""
    for i in range(len(key_component)):
        classType = key_component[i]
        while(True):
            if classType.find('.') == -1:
                break
            else:
                dotPosition = classType.find('.')
                classType = classType.replace(classType[0:dotPosition+1], "")
        classes_pim = classes_pim + """
###  http://www.co-ode.org/ontologies/ont.owl#"""+ classType +"""
<http://www.co-ode.org/ontologies/ont.owl#"""+ classType +"""> rdf:type owl:Class .
    
"""
    return(classes_pim)

def assemble_individuals():
    global main_content
    individual_pim = ""
    for i in range(len(main_content)):
        if i != 0:    
            if len(main_content[i][3]) != 0 and main_content[i][3] != "textSize" and main_content[i][3] != "scale":
                individual = main_content[i][3]
                individual = individual.replace(" ", "_")
                classTypeOfindividual = main_content[i][1]
                while(True):
                    if classTypeOfindividual.find('.') == -1:
                        break
                    else:
                        dotPosition = classTypeOfindividual.find('.')
                        classTypeOfindividual = classTypeOfindividual.replace(classTypeOfindividual[0:dotPosition+1], "")
    
                individual_pim = individual_pim + """###  http://www.co-ode.org/ontologies/ont.owl#"""+ individual +"""
                <http://www.co-ode.org/ontologies/ont.owl#"""+ individual +"""> rdf:type owl:NamedIndividual ,
                                                                       [ rdf:type owl:Restriction ;
                                                                         owl:onProperty owl:topObjectProperty ;
                                                                         owl:someValuesFrom <http://www.co-ode.org/ontologies/ont.owl#"""+classTypeOfindividual+""">
                                                                       ]"""+ assemble_DataProperties(i)
    return(individual_pim)

def assemble_allContent(mounClasses, mounIndividuals):
    content = """@prefix : <http://www.semanticweb.org/user/ontologies/2021/0/"""+ main_content[0][3] +"""#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@base <http://www.semanticweb.org/user/ontologies/2021/0/"""+ main_content[0][3] +"""> .

<http://www.semanticweb.org/user/ontologies/2021/0/"""+ main_content[0][3] +"""> rdf:type owl:Ontology .

#################################################################
#    Data properties
#################################################################
###  http://www.co-ode.org/ontologies/ont.owl#valor
<http://www.co-ode.org/ontologies/ont.owl#valor> rdf:type owl:DatatypeProperty ;
                                                 rdfs:subPropertyOf owl:topDataProperty .
#################################################################
#    Classes
#################################################################
"""+ mounClasses +"""
#################################################################
#    Individuals
#################################################################
"""+ mounIndividuals

    document_owl_name = main_content[0][3] + ".owl"

    with open('models/'+document_owl_name, "w") as owl_file:
        owl_file.write(content)
        owl_file.close()

def startPIMMaker():
    global main_content
    with open('files/temp_select_data_list.json', 'r') as json_content:
        main_content = json.load(json_content)
        json_content.close()

    assemble_allContent(assemble_classes(), assemble_individuals())

