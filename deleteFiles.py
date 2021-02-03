import os
def deleteFile(fileToDelete):  
    try:
        os.remove(fileToDelete)
    except OSError as e:
        print(e)
    else:
        print("File is deleted successfully")

def limpaTudo():
    arrFiles = os.listdir('files/')
    for el in arrFiles:
        pathEl = 'files/'+el
        deleteFile(pathEl)

    arrFiles = os.listdir('models/')
    for el in arrFiles:
        pathEl = 'models/'+el
        deleteFile(pathEl)
        