import json
import requests
import csv
import collections
import xmltodict
from xml.etree import ElementTree as ET_xml
import pandas as pd
import time

all_content = ""
select_content = ""
select_content_list = []
all_content_list = []
all_content_list_aux = []

def save_files():
    global all_content_list

def checkList(ele, prefix):
    for i in range(len(ele)):
        if (isinstance(ele[i], list)):
            checkList(ele[i], prefix+"["+str(i)+"]")
        elif (isinstance(ele[i], str)):
            printField(ele[i], prefix+"["+str(i)+"]")
        else:
            checkDict(ele[i], prefix+"["+str(i)+"]")

def checkDict(jsonObject, prefix):
    for ele in jsonObject:
        if (isinstance(jsonObject[ele], dict)):
            checkDict(jsonObject[ele], prefix+"."+ele)

        elif (isinstance(jsonObject[ele], list)):
            checkList(jsonObject[ele], prefix+"."+ele)

        elif (isinstance(jsonObject[ele], str)):
            printField(jsonObject[ele],  prefix+"."+ele)

        else:
            print("Erro de instancia no json. None Value")
            ##print(jsonObject[ele])


def printField(ele, prefix):
    global select_content
    global all_content
    global select_content_list
    global all_content_list
    global all_content_list_aux
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
                    "ptolemy.actor.TypedCompositeActor"
                    ]
    
    all_content_list_aux.append([prefix, ele])
    #while(True):
    #    if classTypeOfEntity.find('.') == -1:
    #        break
    #    else:
    #        dotPosition = classTypeOfEntity.find('.')
    #        classTypeOfEntity = classTypeOfEntity[dotPosition+1:len(classTypeOfEntity)]

    for i in range(len(key_component)):
        if ele == key_component[i]:
            select_content = select_content + prefix + ":" + ele+ "\n"
            select_content_list.append([prefix, ele]) 
            select_content_list[-1].append(all_content_list[-1][0])
            select_content_list[-1].append(all_content_list[-1][1])

    if str(all_content_list_aux[-1]).find("value") != -1:
        select_content_list[-1].append(all_content_list_aux[-1][0])
        select_content_list[-1].append(all_content_list_aux[-1][1])

    all_content = all_content + prefix + ":" + ele+ "\n"
    
    all_content_list.append([prefix, ele])
    
def makeFiles(mainFile):
    global select_content
    global all_content
    global select_content_list
    global all_content_list
    global all_content_list_aux
    with open(mainFile) as xml_file:
        data_dict = xmltodict.parse(xml_file.read())
        xml_file.close()

    json_data = json.dumps(data_dict, indent=2)

    with open("files/temp_data.json", "w") as json_file:
        json_file.write(json_data)
        json_file.close()

    with open('files/temp_data.json', 'r') as json_content:
        input_dict = json.load(json_content)
        json_content.close()
    
    #iterando todos os campos do JSON
    for element in input_dict:
      #se o valor do campo Json for um Json aninhado
        if (isinstance(input_dict[element], dict)):
            checkDict(input_dict[element], element)
        #se o valor do campo Json for uma lista
        elif (isinstance(input_dict[element], list)):
            checkList(input_dict[element], element)
        #se o valor do campo Json for uma String
        elif (isinstance(input_dict[element], str)):
            printField(input_dict[element], element)
        
    #classes em string contínua
    with open("files/temp_data.txt", "w") as temp_data_list:
        temp_data_list.write(select_content)
        temp_data_list.close()

    #todo o conteúdo em string contínua
    with open("files/temp_all_data.txt", "w") as temp_data_list:
        temp_data_list.write(all_content)
        temp_data_list.close()

    all_content_list = json.dumps(all_content_list, indent=2)

    #somente nome e classe de todo o conteúdo com arraylist de strings em json
    with open("files/temp_data_list.json", "w") as temp_data_list:
        temp_data_list.write(all_content_list)
        temp_data_list.close()

    select_content_list = json.dumps(select_content_list, indent=2)

    #conteúdo selecionado(nome, valor, classe) com arraylist de strings em json
    with open("files/temp_select_data_list.json", "w") as temp_data_list:
        temp_data_list.write(select_content_list)
        temp_data_list.close()

mainFile = "D:/Developer Projects/ptl2sml/Insulin_Pump_Actuator2.xml"
makeFiles(mainFile)