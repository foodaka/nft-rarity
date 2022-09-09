import requests
import time
import json
import os
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

MONGO_URI = os.environ.get("MONGO_URI")
OPENSEA_KEY = os.environ.get("OPENSEA_KEY")

client = MongoClient(MONGO_URI)
import requests



headers = {"accept": "application/json", "content-type": "application/json", "X-API-KEY": OPENSEA_KEY}

#doodles-official
# main_collection_name = "cryptopunks"
main_collection_name = "doodles-official"
# main_collection_name = "mutant-ape-yacht-club"

api_url = f"https://api.opensea.io/api/v1/collection/{main_collection_name}"

response = requests.get(api_url, headers=headers)

#print(response)
#print(response.status_code)
#print(response.content)
#print(response.json())

data = response.json()

primary_asset_address = data['collection']['primary_asset_contracts'][0]['address']
print ("primary_asset_address :", primary_asset_address)

collection_name = data['collection']['name']
print ("collection_name :", collection_name)

tot_count = data['collection']['stats']['count']

# Iterating through the json
# list

main_traits_dic = {}

for i in data['collection']['traits']:
    i = str(i)
    print(i)
    main_traits_dic[i.lower()] = {}
    traits_dic = {}
    total = 0
    for key, value in data['collection']['traits'][i].items():
        traits_dic[str(key).lower()] = value
        total += value

    traits_dic["Total"] = total
    
    main_traits_dic[i.lower()] = traits_dic

print ("traits :", main_traits_dic)

def calculate_rarity_score(d, main_traits_dic, tot_count):  ### Read single asset
    
    rarity_score = 0
    traits = d["traits"]
    print (traits)

    for trait in traits:
        try:
            for k,v in trait.items():
                if str(v).lower() in main_traits_dic:
                    trait_type = str(v).lower()
                    break

            trait_value = str(trait["value"]).lower()
            print ("trait_type : ", trait_type)
            print ("trait_value : ", trait_value)

            #rar_val = (1)/(main_traits_dic[trait_type][trait_value]/main_traits_dic[trait_type]["Total"])
            rar_val = (1)/(main_traits_dic[trait_type][trait_value]/tot_count)
            print ("rar_val :", round(rar_val,2))
            rarity_score += rar_val
        except:
            rarity_score += 0

    rarity_score = round(rarity_score, 2)
    print ("rarity_score :", rarity_score)
    return rarity_score

final_results = []
tot_count = int(tot_count)

for index in range(0,tot_count+2,50):

    time.sleep(4)
    
    collection_id = primary_asset_address

    headers = {"accept": "application/json", "content-type": "application/json", "X-API-KEY": OPENSEA_KEY}

    api_url = f"https://api.opensea.io/api/v1/assets?asset_contract_addresses={collection_id}&offset={index}&limit=50"

    response = requests.get(api_url, headers=headers)

    #len(response.json()["assets"])

    print(response)
    print(response.status_code)
    #print(response.content)
    #print(response.json())

    if response.status_code == 200:
        assets = response.json()['assets']

        for asset_index in range(len(assets)):
            asset = assets[asset_index]
            obj = {}
            obj['collection'] = collection_name
            obj['id'] = asset['id']
            obj['token_id'] = asset['token_id']
            print ("asset_index :", asset_index, "token_id : ", asset['token_id'])
            rarity_score = calculate_rarity_score(asset, main_traits_dic, tot_count)
            obj['rarity_score'] = rarity_score
            final_results.append(obj)
    
#print(response.url)
final_results.sort(key=lambda x: x["rarity_score"], reverse=True)

for result_index in range(len(final_results)):
    final_results[result_index]["rank"] = result_index + 1
    
print ("RESULTS", final_results)    


dbname = client['collections']
print (dbname)

collection_id = dbname['rarity_scores']

new_collection = {}


dbcollection = client["collections"]
mycol = dbcollection["assets"]
print (dbcollection)


new_collection['name'] = collection_name
new_collection['_id'] = primary_asset_address
mycol.insert_one(new_collection)

# final_dic = {}
# for result in final_results:
#     if (result['token_id'] not in final_dic):
#         final_dic[result['token_id']] = result
        
collection_id.insert_one({
    "_id": primary_asset_address,
    "data":final_results,
    "collection": collection_name
    })

# print (final_dic)