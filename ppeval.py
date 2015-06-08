__author__ = 'Existanza'

import requests
import ast

key_file = open('C:/pyton/keys/osu.txt', 'r')
api_key = key_file.read()

user = '2063607'
limit = '20'
mode = '1'
best_url = 'https://osu.ppy.sh/api/get_user_best' + '?k=' + api_key + '&u=' + user + '&m=' + mode + '&limit=' + limit
rc = requests.get(best_url)

res = ast.literal_eval(rc.text)
beatmaps = {}
for i in range(len(res)):
    dic = ast.literal_eval(str(res[i]))
    for key, val in dic.items():
        if key == 'beatmap_id':
            beatmap_id = val
        if key == 'pp':
            pp = val
    beatmaps[beatmap_id] = pp

for key, val in beatmaps.items():
    scores_url = 'https://osu.ppy.sh/api/get_scores' + '?k=' + api_key + '&b=' + key + '&m=1'
    rc2 = requests.get(scores_url)
    res2 = ast.literal_eval(rc2.text)
    score = 0
    hr = False
    hr_found = False
    dt = False
    dt_found = False
    no_mod = False
    no_mod_found = False
    for i in range(len(res2)):
        dic = ast.literal_eval(str(res2[i]))
        for key2, val2 in dic.items():
            if key2 == 'pp':
                score = val2
            if key2 == 'enabled_mods' and val2 == '16':
                hr = True
            if key2 == 'enabled_mods' and val2 == '64':
                dt = True
            if key2 == 'enabled_mods' and val2 == '0':
                no_mod = True
        if hr and not hr_found:
            print(key + '  ' + val + '  ' + score + ' (HR)')
            hr_found = True
        if dt and not dt_found:
            print(key + '  ' + val + '  ' + score + ' (DT)')
            dt_found = True
        if no_mod and not no_mod_found:
            print(key + '  ' + val + '  ' + score)
            no_mod_found = True