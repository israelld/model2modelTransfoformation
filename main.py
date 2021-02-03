from tkinter import Tk
from lxml import etree as ET_lxml
import xml.etree.ElementTree as ET_xml
from tkinter.filedialog import askopenfilename
import PySimpleGUI as sg
import toMdl
import deleteFiles
import os

def sem_arquivo():
    sg.popup('Arquivo não especificado!')

filename = "...no path..." # Definindo uma variável para não ter problema quando for procurada

sg.theme('Topanga')   # Tema da janelinha

layout = [  [sg.Text('Modelo XML - Ptolemy II')], # O conteúdo da janela por "linha".
            [sg.Text('')],
            [sg.Text('Nenhum arquivo selecionado!', size=(64, 1), key="-TOUT01-")],
            [sg.Text(size=(40, 1), key="-TOUT02-")],           
            [sg.Button('Select Ptolemy II Model')],
            [sg.Text('')],
            [sg.Text('Converter para:'), sg.Button('MDL')],
            [sg.Text('')],
            [sg.Button('Visualisar Ontologia'), sg.Button('Limpar Pastas'), sg.Text(size=(25, 1)), sg.Button('Cancelar')]]

# Cria uma Janela
window = sg.Window('Model Transformation', layout, finalize=True)
#window.Maximize()
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancelar': 
        break
    if event == 'Select Ptolemy II Model': 
        Tk().withdraw()
        filename = askopenfilename()
        window["-TOUT01-"].update(filename)
        #if 

    if event == 'MDL':
        if filename == "...no path..." or filename == "" or filename == None:
            sem_arquivo()
            window["-TOUT01-"].update('Nenhum arquivo selecionado!')
        else:
            print("")    
            toMdl.startTransformation(filename) 

    if event == 'Mostrar Pasta':
            path = "D:/Developer Projects/model2modelTransfoformation/models"
            path = os.path.realpath(path)
            os.startfile(path)

    if event == 'Limpar Pastas':
        layoutConfirm = [[sg.Text('Todos os arquivos gerados serão apagados!', auto_size_text=True)],
                      [sg.Button('OK'), sg.Button('Cancelar')]]
                    
        windowConfirm = sg.Window('Confirmação', layoutConfirm)
        eventConfirm, valueConfirm = windowConfirm.read()
        while True:
            if eventConfirm == sg.WIN_CLOSED or eventConfirm == 'Cancelar': 
                break
            elif eventConfirm == "OK":
                deleteFiles.limpaTudo()
                break
        windowConfirm.close()
window.close()
