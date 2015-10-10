import requests
import ast
import sqlite3

__author__ = 'Existanza'

key_file = open('/home/mz/PycharmProjects/osukey.txt', 'r')
api_key = key_file.read()
api_key = api_key[:-1]
user = '2063607'
limit = '3'  # 1-50
game_mode = '1'  # 0 = osu!, 1 = Taiko, 2 = CtB, 3 = osu!mania
convert = '0'   # specify whether converted beatmaps are included (0 = not included, 1 = included).
# Only has an effect if m is chosen and not 0. Optional, default is 0.
conn = sqlite3.connect('taikopersonal2015.db')
c = conn.cursor()


def beatmap_info(map_id, user_score):
    map_url = 'https://osu.ppy.sh/api/get_beatmaps' + '?k=' + api_key + '&b=' + map_id + '&m=' + game_mode + '&a=' + convert
    print('Getting map info: ' + map_id)
    rc_map = requests.get(map_url)
    rc_map_text = rc_map.text.replace(":null", ":\"null\"")
    map_info = ast.literal_eval(rc_map_text)
    if map_info:
        for i in range(len(map_info)):
            dict = ast.literal_eval(str(map_info[i]))
            if dict['approved'] == '1':
                ret = get_scores(map_id, dict['title'], dict['version'], dict['approved_date'], dict['difficultyrating'],
                           dict['bpm'], dict['hit_length'], user_score)
                return ret


def get_scores(key, title, version, approved_date, stars, bpm, hit_length, user_score):
    scores_url = 'https://osu.ppy.sh/api/get_scores' + '?k=' + api_key + '&b=' + key + '&m=1'
    print('Getting scores: ' + key)
    rc2 = requests.get(scores_url)
    res2 = ast.literal_eval(rc2.text)
    hr_found, dt_found, hrdt_found, no_mod_found = (False,)*4
    for i in range(len(res2)):
        dic = ast.literal_eval(str(res2[i]))
        score = dic['pp']
        mode = dic['enabled_mods']
        mode_dic = {'0': '', '16': 'HR', '64': 'DT', '80': 'HRDT', '576': 'DT', '592': 'HRDT'}
        if mode in mode_dic:
            if mode_dic[mode] == 'HR' and not hr_found:
                c.execute('''INSERT INTO maps VALUES (?,?,?,?,?,?,?,?,?,?)''',
                          (key, title, version, approved_date, stars, score, mode_dic[mode], bpm, hit_length, user_score))
                hr_found = True
            elif mode_dic[mode] == 'DT' and not dt_found:
                c.execute('''INSERT INTO maps VALUES (?,?,?,?,?,?,?,?,?,?)''',
                          (key, title, version, approved_date, stars, score, mode_dic[mode], bpm, hit_length, user_score))
                dt_found = True
            elif mode_dic[mode] == 'HRDT' and not hrdt_found:
                c.execute('''INSERT INTO maps VALUES (?,?,?,?,?,?,?,?,?,?)''',
                          (key, title, version, approved_date, stars, score, mode_dic[mode], bpm, hit_length, user_score))
                hrdt_found = True
            elif mode_dic[mode] == '' and not no_mod_found:
                c.execute('''INSERT INTO maps VALUES (?,?,?,?,?,?,?,?,?,?)''',
                          (key, title, version, approved_date, stars, score, mode_dic[mode], bpm, hit_length, user_score))
                no_mod_found = True
    return approved_date


def user_best(user, game_mode, limit):
    best_url = 'https://osu.ppy.sh/api/get_user_best' + '?k=' + api_key + '&u=' + user + '&m=' + game_mode + '&limit=' + limit
    rc = requests.get(best_url)
    res = ast.literal_eval(rc.text)
    for i in range(len(res)):
        di = ast.literal_eval(str(res[i]))
        beatmap_info(di['beatmap_id'], di['pp'])


def get_all(game_mode):
    date = '2005-01-01'
    total = 0
    while date is not None:
        maps_url = 'https://osu.ppy.sh/api/get_beatmaps' + '?k=' + api_key + '&m=' + game_mode + \
                   '&a=' + convert + '&since=' + date + '&limit=5'
        rc_maps = requests.get(maps_url)
        rc_maps_text = rc_maps.text.replace(":null", ":\"null\"")
        maps_info = ast.literal_eval(rc_maps_text)
        for i in range(len(maps_info)):
            print(str(total + i) + '/' + str(total + len(maps_info)))
            di = ast.literal_eval(str(maps_info[i]))
            date = beatmap_info(di['beatmap_id'], '0')
            if date is None:
                break
            print(date)
        total += len(maps_info)


user_best(user, game_mode, limit)
#
# get_all(game_mode)


conn.commit()
i = 0
for row in c.execute('''SELECT * FROM maps ORDER BY score'''):
    i += 1
print(i)
conn.close()
