import json

def loadJson(filePath : str):
    with open(filePath, 'r', encoding='utf8') as f:
        return json.loads("".join(map(lambda x : x.replace("\n", ""), f.readlines())))
    
def saveJson(filePath : str, data):
    with open(filePath, 'w', encoding='utf8') as f:
        f.write(json.dumps(data))