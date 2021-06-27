import os
from shutil import copyfile
import csv
import json
import time
import string
import random

mainAdress = 'https://experiments.schonberglab.org/static/rani/Space_Gold_App_RS/'
commonStartAdress = mainAdress + 'index.html?subId='
commonIconsAdress = mainAdress + 'icons/'

# FUNCTIONS:

def get_random_string(length):
    letters = string.ascii_letters + string.digits
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def createSubNumDict(ranges=[(1101, 1200), (1201, 1300), (1501, 1600), (1601, 1700)], key_code_length=20):
    sub_key_dict = {}
    for i in ranges:
        for j in range(i[0], i[1]):
            #the logic here below is to prevent the last 3 characters of being the same.
            get_code = True
            while get_code:
                new_key = get_random_string(key_code_length)
                get_code = False
                for key in sub_key_dict.keys():
                    if new_key[-3:].lower() == key[-3:].lower():
                        get_code = True
                        break

            sub_key_dict[new_key] = j

    return sub_key_dict

# MANIFEST TEMPLATE:
myDynamicManifest = {
    "name": "Space Gold",
    "short_name": "Space Gold",
    "start_url": "",
    "display": "standalone",
#   "orientation": "portrait",
    "background_color": "#666666ff",
    "theme_color": "#000000",
    "icons": [
        {
            "src": "android-icon-36x36.png",
            "sizes": "36x36",
            "type": "image/png",
            "density": "0.75"
        },
        {
            "src": "android-icon-48x48.png",
            "sizes": "48x48",
            "type": "image/png",
            "density": "1.0"
        },
        {
            "src": "android-icon-72x72.png",
            "sizes": "72x72",
            "type": "image/png",
            "density": "1.5"
        },
        {
             "src": "android-icon-96x96.png",
            "sizes": "96x96",
            "type": "image/png",
            "density": "2.0"
        },
        {
            "src": "android-icon-144x144.png",
            "sizes": "144x144",
            "type": "image/png",
            "density": "3.0"
        },
        {
            "src": "android-icon-192x192.png",
            "sizes": "192x192",
            "type": "image/png",
            "density": "4.0"
        },
        {
            "src": "android-icon-512x512.png",
            "sizes": "512x512",
            "type": "image/png",
            "density": "1.0"
        }
    ]
}
# set the icons full path:
for icon in myDynamicManifest['icons']:
    icon['src'] = commonIconsAdress + icon['src']


# RUN THE CODE:
sub_key_dict = createSubNumDict()

if not os.path.exists('./mapping_key_to_subId.js'):
    # create the js file:
    with open('mapping_key_to_subId.js', 'w') as f:
        f.write('var key2subId_mapping = ')
        json.dump(sub_key_dict, f, indent=4)
    print('The file mapping_key_to_subId.js was saved')
    # backup a copy with a timestamp:
    copyfile('mapping_key_to_subId.js', 'backup/mapping_key_to_subId' + str(time.time()) + '.js')

    # saving a csv file with url's:
    with open('mapping_key_to_subId.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Sub_ID", "URL", "key_code"])
        for key, val in sub_key_dict.items():
            writer.writerow([val, commonStartAdress + key, key])
    print('The file mapping_key_to_subId.csv was saved')
    # backup a copy with a timestamp:
    copyfile('mapping_key_to_subId.csv', 'backup/mapping_key_to_subId.' + str(time.time()) + '.csv')

    # creating manifest files:
    if not os.path.exists('manifests'):
        os.makedirs('manifests')
    for key, val in sub_key_dict.items():
        myDynamicManifest["start_url"] = commonStartAdress + key
        with open('manifests/manifest_' + key + '.json', 'w') as f:
            json.dump(myDynamicManifest, f, indent=4)
    print('The manifest files were saved')

else:
    print('STOPPING! *** The files already exists ***')
