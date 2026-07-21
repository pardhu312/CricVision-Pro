import zipfile
import json
from datetime import datetime
target_date=datetime.strptime("2021-01-01","%Y-%m-%d")
odi_data=[]
icc_data=[]
camp_data=[]
india_matches=[]
with zipfile.ZipFile("odis_json.zip","r") as zip_ref:
    for file in zip_ref.namelist():
        if file.endswith("json"):
            with zip_ref.open(file) as f:
                data = json.load(f)
                odi_data.append(data)
for match in odi_data: 
    match_data=datetime.strptime(match["info"]["dates"][0],"%Y-%m-%d")
    if "India" in match["info"]["teams"] and match["info"]["gender"]=="male" and match_data>=target_date :
        india_matches.append(match)

with zipfile.ZipFile("icc_mens_cricket_world_cup_male_json.zip","r") as zip_ref:
    for file in zip_ref.namelist():
        if file.endswith("json"):
            with zip_ref.open(file) as f:
                data = json.load(f)
                icc_data.append(data)
for match in icc_data: 
    match_data=datetime.strptime(match["info"]["dates"][0],"%Y-%m-%d")
    if "India" in match["info"]["teams"] and match["info"]["gender"]=="male" and match["info"]["match_type"]=="ODI" and match_data>=target_date :
        india_matches.append(match)        
with open("india.json","w") as z:
        json.dump(india_matches,z,indent=4)  




print("done")            
