__author__ = 'Existanza'

import requests
import ast

key_file = open('C:/pyton/keys/osu.txt', 'r')
api_key = key_file.read()
save = open('C:/pyton/ppeval/osu.txt', 'w')
user = '2063607'
limit = '50'  # 1-50
mode = '1'  # 0 = osu!, 1 = Taiko, 2 = CtB, 3 = osu!mania
convert = '1'   # specify whether converted beatmaps are included (0 = not included, 1 = included).
# Only has an effect if m is chosen and not 0. Optional, default is 0.


def beatmap_info(map_id, user_score):
    map_url = 'https://osu.ppy.sh/api/get_beatmaps' + '?k=' + api_key + '&b=' + map_id + '&m=' + mode + '&a=' + convert
    rc_map = requests.get(map_url)
    map_info = ast.literal_eval(rc_map.text)
    for i in range(len(map_info)):
        dict = ast.literal_eval(str(map_info[i]))
        for key, val in dict.items():
            if key == 'title':
                title = val
            if key == 'version':
                version = val
    print(map_id + ' - ' + title + ' - ' + version)
    save.write(map_id + ' - ' + title + ' - ' + version + '\n')
    print(user_score, end=' -> ')
    save.write(user_score + ' -> ')


# for key, val in beatmaps.items():
def get_scores(key):
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
            print(score + ' (HR) ', end='')
            save.write(score + ' (HR) ')
            hr_found = True
        if dt and not dt_found:
            print(score + ' (DT) ', end='')
            save.write(score + ' (DT) ')
            dt_found = True
        if no_mod and not no_mod_found:
            print(score, end='')
            save.write(score)
            no_mod_found = True
    print('')
    print('')
    save.write('\n\n')

best_url = 'https://osu.ppy.sh/api/get_user_best' + '?k=' + api_key + '&u=' + user + '&m=' + mode + '&limit=' + limit
rc = requests.get(best_url)
res = ast.literal_eval(rc.text)
for i in range(len(res)):
    dic = ast.literal_eval(str(res[i]))
    for key, val in dic.items():
        if key == 'beatmap_id':
            beatmap_id = val
        if key == 'pp':
            pp = val
    beatmap_info(beatmap_id, pp)
    get_scores(beatmap_id)
save.close()