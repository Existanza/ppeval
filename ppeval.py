__author__ = 'Existanza'

import requests
import ast
import sqlite3

key_file = open('C:/pyton/keys/osu.txt', 'r')
api_key = key_file.read()
# save = open('C:/pyton/ppeval/osu.txt', 'a')
user = '2063607'
limit = '1'  # 1-50
mode = '1'  # 0 = osu!, 1 = Taiko, 2 = CtB, 3 = osu!mania
convert = '0'   # specify whether converted beatmaps are included (0 = not included, 1 = included).
# Only has an effect if m is chosen and not 0. Optional, default is 0.
conn = sqlite3.connect('taiko.db')
c = conn.cursor()


# def beatmap_info(map_id, user_score):
def beatmap_info(map_id):
    map_url = 'https://osu.ppy.sh/api/get_beatmaps' + '?k=' + api_key + '&b=' + map_id + '&m=' + mode + '&a=' + convert
    rc_map = requests.get(map_url)
    map_info = ast.literal_eval(rc_map.text)
    if map_info:
        for i in range(len(map_info)):
            dict = ast.literal_eval(str(map_info[i]))
            for key, val in dict.items():
                if key == 'title':
                    title = val
                if key == 'version':
                    version = val
                if key == 'approved':
                    ranked = val
                if key == 'last_update':
                    last_update = val
                if key == 'difficultyrating':
                    stars = val
                if key == 'bpm':
                    bpm = val
                if key == 'hit_length':
                    hit_length = val
        # print(map_id + ' - ' + title + ' - ' + version)
        # save.write(map_id + ' - ' + title + ' - ' + version + '\n')
        # print(user_score, end=' -> ')
        # save.write(user_score + ' -> ')
        if ranked == '1':
            get_scores(map_id, title, version, last_update, stars, bpm, hit_length)


def get_scores(key, title, version, last_update, stars, bpm, hit_length):
    scores_url = 'https://osu.ppy.sh/api/get_scores' + '?k=' + api_key + '&b=' + key + '&m=1'
    rc2 = requests.get(scores_url)
    res2 = ast.literal_eval(rc2.text)
    score = 0
    hr, hr_found, dt, dt_found, hrdt, hrdt_found, no_mod, no_mod_found = (False,)*8
    for i in range(len(res2)):
        dic = ast.literal_eval(str(res2[i]))
        for key2, val2 in dic.items():
            if key2 == 'pp':
                score = val2
            if key2 == 'enabled_mods' and val2 == '16':
                hr = True
            if key2 == 'enabled_mods' and val2 == '64':
                dt = True
            if key2 == 'enabled_mods' and val2 == '80':
                hrdt = True
            if key2 == 'enabled_mods' and val2 == '0':
                no_mod = True
        if hr and not hr_found:
            # print(score + ' (HR) ', end='')
            # save.write(score + ' (HR) ')
            mod = 'HR'
            c.execute('''INSERT INTO maps VALUES (?,?,?,?,?,?,?,?,?)''',
                      (key, title, version, last_update, stars, score, mod, bpm, hit_length))
            hr_found = True
        if dt and not dt_found:
            # print(score + ' (DT) ', end='')
            # save.write(score + ' (DT) ')
            mod = 'DT'
            c.execute('''INSERT INTO maps VALUES (?,?,?,?,?,?,?,?,?)''',
                      (key, title, version, last_update, stars, score, mod, bpm, hit_length))
            dt_found = True
        if hrdt and not hrdt_found:
            # print(score + ' (HRDT) ', end='')
            # save.write(score + ' (HRDT) ')
            mod = 'HRDT'
            c.execute('''INSERT INTO maps VALUES (?,?,?,?,?,?,?,?,?)''',
                      (key, title, version, last_update, stars, score, mod, bpm, hit_length))
            hrdt_found = True
        if no_mod and not no_mod_found:
            # print(score, end='')
            # save.write(score)
            mod = ''
            c.execute('''INSERT INTO maps VALUES (?,?,?,?,?,?,?,?,?)''',
                      (key, title, version, last_update, stars, score, mod, bpm, hit_length))
            no_mod_found = True
    print(last_update)
    # print('\n')
    # save.write('\n\n')

# best_url = 'https://osu.ppy.sh/api/get_user_best' + '?k=' + api_key + '&u=' + user + '&m=' + mode + '&limit=' + limit
# rc = requests.get(best_url)
# res = ast.literal_eval(rc.text)
# for i in range(len(res)):
#     dic = ast.literal_eval(str(res[i]))
#     for key, val in dic.items():
#         if key == 'beatmap_id':
#             beatmap_id = val
#         if key == 'pp':
#             pp = val
#     beatmap_info(beatmap_id, pp)

maps_url = 'https://osu.ppy.sh/api/get_beatmaps' + '?k=' + api_key + '&m=' + mode + '&a=' + convert + '&since=2015-04-08&limit=200'
rc_maps = requests.get(maps_url)
maps_info = ast.literal_eval(rc_maps.text)
for i in range(len(maps_info)):
    print(str(i) + '/' + str(len(maps_info)))
    dic = ast.literal_eval(str(maps_info[i]))
    for key, val in dic.items():
        if key == 'beatmap_id':
            print(val)
            beatmap_info(val)

conn.commit()
i = 0
for row in c.execute('''SELECT * FROM maps ORDER BY score'''):
    i += 1
print(i)
conn.close()
# save.close()