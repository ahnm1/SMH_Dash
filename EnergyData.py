#%% 
import json
import requests
from pyscbwrapper import SCB
import pandas as pd

#%%
## definitions

raw_file = 'raw_energy.json'
url     = \
    'https://api.scb.se/OV0104/v1/doris/sv/ssd/' + \
        'START/EN/EN0108/EN0108A/Elprod'
payload = {
  "query": [
    {
      "code": "Tid",
      "selection": {
        "filter": "item",
        "values": [
          "2021M11",
          "2021M12",
          "2022M01",
          "2022M02",
          "2022M03",
          "2022M04",
          "2022M05",
          "2022M06",
          "2022M07",
          "2022M08",
          "2022M09",
          "2022M10"
        ]
      }
    }
  ],
  "response": {
    "format": "json"
  }
}
request = requests.post(url, str(payload))
request

#%%
## save raw json

json_dump = json.dumps(request.json())
with open(raw_file, 'w') as outfile:
    outfile.write(json_dump)

#%%
## load raw json for transformation USE PANDAS = 7 rows

# from collections import defaultdict
# def_dict = defaultdict(int)

# with open('raw_energy.json', 'r') as infile, \
#     open('data_energy.csv') as outfile:

#         data_dict = json.loads(infile.read())
#         # print(data_dict.keys())

#         for key, value in data_dict.items():
#             # print(key)

#             if key == 'columns':
#                 for val in value:
#                     # print(len(val))
#                     outfile.write(f"{val['text']};")
#                     pass

#             elif key == 'comments':
#                 print(';;;')
        
#             elif key == 'data':
#                 for val in value:
#                     print(f"{val['key'][0]};{val['key'][1].replace('M','-')}-01 00:00:00;{val['values'][0]}")

#             elif key == 'metadata':
#                 pass

#%%
## pandas

df = pd.read_json(raw_file, orient = 'index', typ = 'series')

data_list = []

for item in df['data']:
    data_list.append([item['key'][0], item['key'][1].replace('M','-')  + '-01', item['values'][0]])

df_data = pd.DataFrame(data_list, columns = ['type', 'month', 'amount'])
# dfc = df.pivot(columns = 0)
df_data = df_data[['month', 'type', 'amount']]
df_data.to_csv('full_clean_energy.csv', index=False)
# %%
