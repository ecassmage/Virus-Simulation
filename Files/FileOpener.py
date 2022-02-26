import json
import os


def openStg():
    try:
        file = open(os.path.abspath(os.curdir) + '\\Files\\settings.json')
    except FileNotFoundError:
        file = open(os.path.dirname(os.path.abspath(os.curdir)) + '\\Files\\settings.json')
    jsonFile = json.load(file)
    file.close()
    return jsonFile
