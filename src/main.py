import ast
import requests
import os
import json

gridDownloadLink = "https://dota2protracker.com/downloads/meta-hero-grid"

def readSettingsFile():
    #get each line
    #read the file, format it to:
    #[[key, value], [key, value]]
    with open("../config.config") as f:
        data = [[x.strip() for x in y.split("=", 1)] for y in f.read().split("\n") if "=" in y]
    f.close()
    out = {}
    for k,v in data:
        try:
            out[k] = ast.literal_eval(v)
        except:
            #check if integer
            if v.isdigit():
                out[k] = int(v)
            elif v.replace(".","",1).isdigit():
                out[k] = float(v)
            out[k] = v
    return out

settings = readSettingsFile()
gridPath = os.path.join(settings["hero_grid_folder"], "hero_grid_config.json")

print("\n"*100)
#download the file
print("Downloading dota2protracker_hero_grid_config.json")
r = requests.get(gridDownloadLink)
content = r.content.decode("utf-8") #decode bytes to string
content = ast.literal_eval(content)
d2ptGrids = content["configs"]

#read the current hero grid folder
print("Reading your current hero grid")
heroGridData = ast.literal_eval(open(gridPath, "r").read())
heroGrids = heroGridData["configs"].copy()

#go through the grid and remove d2pt grids
for grid in heroGrids:
    if "Dota2ProTracker" in grid["config_name"]: 
        heroGridData["configs"].remove(grid)
#add the new d2pt grids
for grid in d2ptGrids:
    heroGridData["configs"].append(grid)

#update
with open(gridPath, "w") as f:
    f.write(json.dumps(heroGridData, indent=2))

print("D2pt grid successfully merged with your existing grids")