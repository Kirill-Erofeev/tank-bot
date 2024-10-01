import json
import vk_api
import random
import requests
from demotivator import Demotivator
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from PIL import Image
from datetime import date





#Сервер https://cbbot.ifx.su/u6goc6:226106896?code=8dbdb95d
player_tanks = {}
battle_type = None
# GROUP_TOKEN = """vk1.a.HNKbzJjt987sI6qa1TwXBlpYpxb4RO-c-y5KF9nnDLsTkc1Mouu7X_DPGWJVmsweEJkIXUFcQR
# oTOf8YdhIn6sFtzK8h4MIFecAiwF_fSovgl7Bq1O5bJFVljxp-hf6qthNrX3GvaMi7JU4cr_Ac_LkKgf3q4y5OMbg5XOalt7F
# Og9Me5qepbqfvjoQTlxvI8Mjol24sn_ixEO5X6yPz1g""" #Японская жаба
GROUP_TOKEN = '''vk1.a.dBgqASfEk_UEHceRLCGZtxQhSc-FM6U39rfWbKR9mVzdbWO0D2trKAoC_vr26Ke9hr5ylMbwKc
veGCY_l1F01nB0hVH7EnCVsFhaB4oT1iIN79O8nwdkG-1MgaKSs6tugkAbdxp_KIX7D_5TJSWyjLRpY5JIn29U178dIrakqiP
OK_fTIbfFPE0gIDbzUIxeqmWIr4csmRkdornG17O6LQ''' #LU-XE
# GROUP_TOKEN = '''vk1.a.GqXNacaJEtuM_Ew62A_BHvKMOvqGYlO5rUdPg1CGnDmid1fzeECZtqWwXXK_I8Zdrs-WCAz3ia
# KY1azls8VI-mmrIXtVmpbKnNReWoqp3xOAwcW_bHTCDIpSQSgUeEVhqXzshoC4SxO0XWoECt3kvi7UKCB6wp71her01fGlHfh
# Ws4VX69Wv5Z0DIf-hdSTYD64DaiUUjnHu4Al0DrAesA''' #ENEMY
# GROUP_ID = 226106896 #Японская жаба
GROUP_ID = 226416696
MY_ID = 249200120
RUSLAN_ID = 303957001
CHAT_ID = 2000000000 + 163
MENTION = '[club226106896|@club226106896]'
KEYBOARD_SETTINGS = dict(inline=False, one_time=False)
DATA_FOLDER_FILE_PATH = './data/'
BOT_INFO = '''БОТ ПЕРЕСТАНЕТ ОТВЕЧАТЬ, ЕСЛИ КАКОЙ-ТО СВЕРХРАЗУМ ЕГО ПОЛОЖИТ.
Для активации бота необходимо написать "&".
Чем больше картинок участники кидают в беседу,
тем больше их становится у бота.
Аналогичная ситуация с сообщениями для демотиватора.
Функционал интуитивно понятен.

Подробнее про режим "Долгий бой":
0) Одновременно может иди только 1 бой любого вида;
1) Для выстрела необходимо написать "выстрел";
2) Если Ваш танк загорелся - необходимо написать "потушить";
3) Если у Вашего танка выбили заряжающего - необходимо написать "вылечить";
4) Во время долгого боя не нагружайте бота другими командами, поскольку
на их обработку серверу требуется время, что плохо сказывается на
самом бое.

Приглашение действительно в течение трёх минут.
Любой участник может отменить приглашение, написав "отменить приглашение"
через три минуты после его отправки.
Если бой длится больше 3 минут, можно написать "завершить бой".
Участники боя не могут воспользоваться этой опцией.
Важно: воспользоваться двумя этими опциями можно только
в том случае, если активна главная клавиатура.
'''
# Выражаю благодарность за помощь в разработке Артуру и Егору.
# '''

# BTN_LABELS = {
#     'winner': 'Игрок дня',
#     'loser': 'Банка дня',
#     'best_teams': 'Инсайдерская инфа по T8',
#     '322120408': 'Андрей Полтавский',
#     '280864946': 'Артём Хомяков',
#     '452036630': 'Артём Бондаренко',
#     '567572779': 'Егор Корчин',
#     '160348331': 'Артур Присада',
#     '249200120': 'Кирилл Ерофеев',
#     '434340601': 'Кирилл Кобец',
#     '571456262': 'Влад Марченко',
#     'haveadealwithme': 'Алексей Алдошкин',
#     'gubanvp': 'Артём Губанов',
#     '546754921': 'Фёдор Бирюков',
#     '704189756': 'Churki Cpy',
#     '650573187': 'Бодя Абхщда',
#     '284569404': 'Владимир Маркин',
#     '360581583': 'Андрей Афанасьев',
#     '388908512': 'Egor Lxtter',
# }

T12_TEAMS = [
    '[GGAME]',
    '[7STAR]',
    '[ZOMBI]',
    '[ENEMY]',
    '[LYD1K]',
    '[DELAU]',
    '[XWING]',
    '[-OGT-]',
    '[META-]',
    '[-SCAM]',
    '[VAINE]',
    '[MERCY]',
    # '[CXNTR]',
    # '[KEGLY]',
    # '[KEGLV]',
    # '[WXNCY]'
]



TANKS = [
    {'id': 'T110E4', 'class_': 'ПТ', 'hp': 2000, 'damage': 630, 'reload': 11.79, 'breakout_prob': 0.74, 'fire_prob': 0.20},
    {'id': 'T110E3', 'class_': 'ПТ', 'hp': 2067, 'damage': 680, 'reload': 14.31, 'breakout_prob': 0.68, 'fire_prob': 0.20},
    {'id': 'T110E5', 'class_': 'ТТ', 'hp': 2576, 'damage': 400, 'reload': 8.34, 'breakout_prob': 0.79, 'fire_prob': 0.20},
    {'id': 'Grille 15', 'class_': 'ПТ', 'hp': 1802, 'damage': 580, 'reload': 9.95, 'breakout_prob': 0.76, 'fire_prob': 0.15}, #0.15
    {'id': 'Jz.Pz. E 100', 'class_': 'ПТ', 'hp': 2279, 'damage': 800, 'reload': 15.66, 'breakout_prob': 0.77, 'fire_prob': 0.15},
    # {'id': 'Jz.Pz. E 100', 'class_': 'ПТ', 'hp': 2279, 'damage': 800, 'reload': 0.50, 'breakout_prob': 1, 'fire_prob': 0.15},
    {'id': 'VK 72.01 K', 'class_': 'ТТ', 'hp': 2744, 'damage': 600, 'reload': 13.47, 'breakout_prob': 0.78, 'fire_prob': 0.12},
    {'id': 'Maus', 'class_': 'ТТ', 'hp': 3192, 'damage': 460, 'reload': 10.10, 'breakout_prob': 0.87, 'fire_prob': 0.12},
    {'id': 'E 100', 'class_': 'ТТ', 'hp': 2915, 'damage': 680, 'reload': 16.67, 'breakout_prob': 0.77, 'fire_prob': 0.15}, #0.15
    {'id': 'E 50 M', 'class_': 'СТ', 'hp': 2014, 'damage': 340, 'reload': 6.06, 'breakout_prob': 0.78, 'fire_prob': 0.12}, #0.12
    {'id': 'Leopard 1', 'class_': 'СТ', 'hp': 1908, 'damage': 360, 'reload': 5.47, 'breakout_prob': 0.86, 'fire_prob': 0.10},
    {'id': 'Об. 268', 'class_': 'ПТ', 'hp': 1908, 'damage': 690, 'reload': 13.47, 'breakout_prob': 0.70, 'fire_prob': 0.12},
    {'id': 'Об. 263', 'class_': 'ПТ', 'hp': 1961, 'damage': 460, 'reload': 6.90, 'breakout_prob': 0.88, 'fire_prob': 0.15},
    {'id': 'ИС-7', 'class_': 'ТТ', 'hp': 2703, 'damage': 460, 'reload': 10.68, 'breakout_prob': 0.76, 'fire_prob': 0.15},
    {'id': 'Об. 140', 'class_': 'СТ', 'hp': 1908, 'damage': 300, 'reload': 4.72, 'breakout_prob': 0.84, 'fire_prob': 0.12},
    {'id': 'Т-62А', 'class_': 'СТ', 'hp': 2014, 'damage': 330, 'reload': 5.73, 'breakout_prob': 0.79, 'fire_prob': 0.10},
    {'id': 'Т-100 ЛТ', 'class_': 'ЛТ', 'hp': 1855, 'damage': 310, 'reload': 5.64, 'breakout_prob': 0.73, 'fire_prob': 0.10},
    {'id': 'FV215b', 'class_': 'ТТ', 'hp': 2576, 'damage': 400, 'reload': 7.33, 'breakout_prob': 0.86, 'fire_prob': 0.20},
    {'id': 'STB-1', 'class_': 'СТ', 'hp': 1961, 'damage': 330, 'reload': 5.64, 'breakout_prob': 0.79, 'fire_prob': 0.12},
    {'id': 'Type 71', 'class_': 'ТТ', 'hp': 2703, 'damage': 420, 'reload': 9.60, 'breakout_prob': 0.77, 'fire_prob': 0.12},
    {'id': 'WZ-113G FT', 'class_': 'ПТ', 'hp': 2240, 'damage': 640, 'reload': 12.63, 'breakout_prob': 0.76, 'fire_prob': 0.12},
    {'id': 'WZ-113', 'class_': 'ТТ', 'hp': 2438, 'damage': 400, 'reload': 7.33, 'breakout_prob': 0.84, 'fire_prob': 0.12},
    {'id': 'WZ-121', 'class_': 'СТ', 'hp': 1908, 'damage': 420, 'reload': 7.33, 'breakout_prob': 0.77, 'fire_prob': 0.12},
    {'id': 'CS-63', 'class_': 'СТ', 'hp': 1908, 'damage': 340, 'reload': 6.06, 'breakout_prob': 0.76, 'fire_prob': 0.10},
    {'id': 'ЛВ-1300 Уран', 'class_': 'ТТ', 'hp': 2544, 'damage': 460, 'reload': 10.53, 'breakout_prob': 0.74, 'fire_prob': 0.15},
    {'id': 'Strv K', 'class_': 'ТТ', 'hp': 2576, 'damage': 350, 'reload': 6.06, 'breakout_prob': 0.89, 'fire_prob': 0.15},
    {'id': 'AMX M4 mle. 54', 'class_': 'ТТ', 'hp': 2800, 'damage': 450, 'reload': 10.02, 'breakout_prob': 0.80, 'fire_prob': 0.20},
    {'id': 'AMX 30 B', 'class_': 'СТ', 'hp': 1908, 'damage': 350, 'reload': 5.89, 'breakout_prob': 0.80, 'fire_prob': 0.10},
    {'id': '121B', 'class_': 'СТ', 'hp': 1908, 'damage': 350, 'reload': 6.06, 'breakout_prob': 0.78, 'fire_prob': 0.12}, #?
    {'id': 'FV217 Badger', 'class_': 'ПТ', 'hp': 2240, 'damage': 460, 'reload': 7.16, 'breakout_prob': 0.90, 'fire_prob': 0.20},
    {'id': 'Chieftain Mk. 6', 'class_': 'ТТ', 'hp': 2491, 'damage': 400, 'reload': 7.58, 'breakout_prob': 0.83, 'fire_prob': 0.10},
    {'id': 'Super Conqueror', 'class_': 'ТТ', 'hp': 2597, 'damage': 400, 'reload': 8.17, 'breakout_prob': 0.81, 'fire_prob': 0.20},
    {'id': 'Об. 260', 'class_': 'ТТ', 'hp': 2544, 'damage': 400, 'reload': 7.75, 'breakout_prob': 0.82, 'fire_prob': 0.15},
    {'id': 'Об. 777 Ⅱ', 'class_': 'ТТ', 'hp': 2544, 'damage': 430, 'reload': 8.25, 'breakout_prob': 0.83, 'fire_prob': 0.25},
    {'id': 'Об. 907', 'class_': 'СТ', 'hp': 1908, 'damage': 320, 'reload': 5.47, 'breakout_prob': 0.78, 'fire_prob': 0.12}, #?
    {'id': 'Т-22 ср.', 'class_': 'СТ', 'hp': 1961, 'damage': 310, 'reload': 5.47, 'breakout_prob': 0.77, 'fire_prob': 0.10},
    {'id': 'Kpz 50 t', 'class_': 'СТ', 'hp': 1908, 'damage': 320, 'reload': 5.22, 'breakout_prob': 0.82, 'fire_prob': 0.12},
    {'id': 'XM66F', 'class_': 'ПТ', 'hp': 2014, 'damage': 410, 'reload': 6.90, 'breakout_prob': 0.81, 'fire_prob': 0.12}, #?
    {'id': 'T95E6', 'class_': 'ТТ', 'hp': 2438, 'damage': 400, 'reload': 7.24, 'breakout_prob': 0.84, 'fire_prob': 0.15},
    {'id': 'Sheridan Ракетный', 'class_': 'ЛТ', 'hp': 1908, 'damage': 560, 'reload': 13.47, 'breakout_prob': 0.55, 'fire_prob': 0.12},
    {'id': 'VK 90.01 (P)', 'class_': 'ТТ', 'hp': 2597, 'damage': 460, 'reload': 10.53, 'breakout_prob': 0.75, 'fire_prob': 0.10},
    {'id': 'Concept 1B', 'class_': 'ТТ', 'hp': 2491, 'damage': 380, 'reload': 7.58, 'breakout_prob': 0.80, 'fire_prob': 0.12}, #?
    {'id': 'M48 Patton', 'class_': 'СТ', 'hp': 1961, 'damage': 340, 'reload': 5.73, 'breakout_prob': 0.80, 'fire_prob': 0.12},
    {'id': 'M60', 'class_': 'СТ', 'hp': 2014, 'damage': 350, 'reload': 5.98, 'breakout_prob': 0.80, 'fire_prob': 0.10},
    {'id': 'WZ-111 5A', 'class_': 'ТТ', 'hp': 2438, 'damage': 440, 'reload': 8.93, 'breakout_prob': 0.78, 'fire_prob': 0.12},
    {'id': 'Объект 268/4', 'class_': 'ПТ', 'hp': 1961, 'damage': 650, 'reload': 13.05, 'breakout_prob': 0.69, 'fire_prob': 0.12},
    {'id': 'Foch 155', 'class_': 'ПТ', 'hp': 1961, 'damage': 600, 'reload': 11.52, 'breakout_prob': 0.72, 'fire_prob': 0.15},
    {'id': 'Vickers Light', 'class_': 'ЛТ', 'hp': 1802, 'damage': 300, 'reload': 5.47, 'breakout_prob': 0.72, 'fire_prob': 0.20},
    {'id': 'FV4202', 'class_': 'СТ', 'hp': 1908, 'damage': 350, 'reload': 6.06, 'breakout_prob': 0.78, 'fire_prob': 0.20},
    {'id': 'FV215b 183', 'class_': 'ПТ', 'hp': 1908, 'damage': 930, 'reload': 18.52, 'breakout_prob': 0.68, 'fire_prob': 0.20},
    {'id': 'Ho-Ri', 'class_': 'ПТ', 'hp': 2014, 'damage': 560, 'reload': 10.10, 'breakout_prob': 0.77, 'fire_prob': 0.15},
    {'id': 'WZ-132-1', 'class_': 'ЛТ', 'hp': 1855, 'damage': 360, 'reload': 6.65, 'breakout_prob': 0.72, 'fire_prob': 0.12},
    {'id': '60TP Lewandowskiego', 'class_': 'ТТ', 'hp': 2756, 'damage': 630, 'reload': 14.74, 'breakout_prob': 0.77, 'fire_prob': 0.15},
    {'id': 'Vz. 55', 'class_': 'ТТ', 'hp': 2544, 'damage': 470, 'reload': 10.69, 'breakout_prob': 0.74, 'fire_prob': 0.10},
]

# np.random.shuffle(TANKS)
TANKS = TANKS[:36]
# Об. 777 Ⅱ, Concept 1B, Об. 907, XM66F
#     {'id': 'FV4202', 'hp': 1908, 'damage': 350, 'reload': 6.74, 'breakout_prob': 0.8, 'fire_prob': 0.20},

EFFECTS = [
    'Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2',
    'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r',
    'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r',
    'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu',
    'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral',
    'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot',
    'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r',
    'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'gist_earth',
    'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r',
    'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r',
    'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'nipy_spectral', 'nipy_spectral_r',
    'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'rocket', 'rocket_r',
    'seismic', 'seismic_r', 'spectral', 'spectral_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r',
    'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'viridis', 'viridis_r', 'vlag', 'vlag_r', 'winter', 'winter_r'
]

def read_json(file_name):
    try:
        with open(DATA_FOLDER_FILE_PATH + file_name, mode='r') as openfile:
            lst = json.load(openfile)
    except FileNotFoundError:
        lst = []
    return lst


def get_loser(users):
    np.random.seed(date.today().day)
    # random.shuffle(users)
#     random_user = f"Банка дня: @{users[0]}"
#     random_user_id = random.choice(list(users))
#     random_user = f'Банка дня: @{users[random_user_id][0]}'
    random_user_dic = np.random.choice(users)
    random_user_domain = random_user_dic['first_last_name']
    loser = f'Банка дня: {random_user_domain}'
    # random_user_domain = random_user_dic['domain']
    # loser = f'Банка дня: @{random_user_domain}'
    return loser


def get_winner(users):
    np.random.seed(abs(date.today().day - date.today().month))
    # random.shuffle(users)
#     random_user = f"Игрок дня: @{users[0]}"
#     random_user_id = random.choice(list(users))
#     random_user = f'Игрок дня: @{users[random_user_id][0]}'
    random_user_dic = np.random.choice(users)
    random_user_domain = random_user_dic['first_last_name']
    winner = f'Статист дня: {random_user_domain}'
    # random_user_domain = random_user_dic['domain']
    # winner = f'Статист дня: @{random_user_domain}'
    return winner


def get_best_teams(teams, num_best_teams=8):
    message = ''
    best_teams = []
    while len(best_teams) < num_best_teams:
        random_index = random.randint(0, len(teams)-1)
        team = teams[random_index]
        if team not in best_teams:
            best_teams.append(team)
    for num, team in enumerate(best_teams, start=1):
        message += f'{num}) {team}\n'
    return message.strip()


def get_leaderboard(users):
    response = ''
    for i in range(len(users) - 1, 0, -1):
        for j in range(i):
            try:
                winrate_1 = users[j]['wins'] / users[j]['battles']
                mean_damage_1 = sum(users[j]['damage']) / users[j]['battles']
            except ZeroDivisionError:
                winrate_1 = 0
                mean_damage_1 = 0
            try:
                winrate_2 = users[j + 1]['wins'] / users[j + 1]['battles']
                mean_damage_2 = sum(users[j + 1]['damage']) / users[j + 1]['battles']
            except ZeroDivisionError:
                winrate_2 = 0
                mean_damage_2 = 0
                    
            if winrate_1 == winrate_2:
                if mean_damage_1 < mean_damage_2:
                    users[j + 1], users[j] = users[j], users[j + 1]
                else:
                    pass
            elif winrate_1 < winrate_2:
                users[j + 1], users[j] = users[j], users[j + 1]
    
    for num, dic in enumerate(users, start=1):
        try:
            winrate = round(dic['wins'] / dic['battles'] * 100)
            mean_damage = round(sum(dic['damage']) / dic['battles'])
        except ZeroDivisionError:
            winrate = 0
            mean_damage = 0
        first_last_name = dic['first_last_name']
        emoji = dic['emoji']
        response += f'{num}) {first_last_name} {emoji}: {winrate}%, {mean_damage} су\n'
    return response.strip()


def get_demotivator(vk_session):
    message = None
    attachment = None
    photos = read_json('photos.json')
    messages = read_json('messages.json')
    # with open('photos.json', mode='r') as openfile:
    #     photos = json.load(openfile)

    # with open('messages.json', mode='r') as openfile:
    #     messages = json.load(openfile)

    if len(photos) > 0 and len(messages) > 0:
        random_num = random.randint(0, len(photos) - 1)
        url = photos[random_num]['url']
        expansion = photos[random_num]['expansion']
        p = requests.get(url)
        out = open(f'./Images/dem_image.{expansion}', 'wb')
        out.write(p.content)
        out.close()

        # random_num_1 = random.randint(0, len(messages) - 1)
        # random_num_2 = random.randint(0, len(messages) - 1)
        # text_1 = messages[random_num_1]
        # text_2 = messages[random_num_2]
        text_1 = np.random.choice(messages)
        text_2 = np.random.choice(messages)

        # dem = Demotivator('mv-jadheedh-regular.ttf')
        dem = Demotivator(DATA_FOLDER_FILE_PATH + 'ofont.ru_Geologica.ttf')
        dem.create_demotivator(
            f'./Images/dem_image.{expansion}',
            text_1,
            text_2
        )
        dem.save(f'./Images/demotivator.{expansion}')
        # message = 'Привет!'

        upload = vk_api.VkUpload(vk_session)
        photo = upload.photo_messages(f'./Images/demotivator.{expansion}')
        owner_id = photo[0]['owner_id']
        photo_id = photo[0]['id']
        access_key = photo[0]['access_key']
        attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    else:
        message = 'Опция недоступна!'

    return message, attachment


def apply_filter(img, kernel):
    h, w = np.array(img.shape)
    kh, kw = np.array(kernel.shape)
    out = np.zeros((h - kh + 1, w - kw + 1))
    for i in range(h - kh + 1):
        for j in range(w - kw + 1):
            patch = img[i : i + kh, j : j + kw]
            new_pixel = np.multiply(patch, kernel).sum()
            out[i, j] = new_pixel
    return out


def get_effect(vk_session):
    message = None
    attachment = None

    photos = read_json('photos.json')
    # with open('photos.json', mode='r') as openfile:
    #     photos = json.load(openfile)

    if len(photos) > 0:
        random_num = random.randint(0, len(photos) - 1)
        url = photos[random_num]['url']
        expansion = photos[random_num]['expansion']
        p = requests.get(url)
        out = open(f'./Images/effect_img.{expansion}', 'wb')
        out.write(p.content)
        out.close()

        random_num = random.randint(0, len(photos) - 1)
        url = photos[random_num]['url']
        random_num = random.randint(0, len(EFFECTS) - 1)
        effect = EFFECTS[random_num]

        image = Image.open(f'./Images/effect_img.{expansion}')
        img_tensor = tf.convert_to_tensor(image).numpy().mean(axis=2)
        fig, axes = plt.subplots(figsize=plt.figaspect(img_tensor))
        axes.imshow(img_tensor, cmap=effect)
        fig.subplots_adjust(0, 0, 1, 1)
        axes.axis('off')
        fig.savefig(f'./Images/effect.{expansion}')
        plt.close(fig)

        upload = vk_api.VkUpload(vk_session)
        photo = upload.photo_messages(f'./Images/effect.png')
        owner_id = photo[0]['owner_id']
        photo_id = photo[0]['id']
        access_key = photo[0]['access_key']
        attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    else:
        message = 'Опция недоступна!'

    return message, attachment


# def get_demotivator(vk_session):
#     message = None
#     attachment = None
#     photos = read_json('photos.json')
#     messages = read_json('messages.json')
#     # with open('photos.json', mode='r') as openfile:
#     #     photos = json.load(openfile)

#     # with open('messages.json', mode='r') as openfile:
#     #     messages = json.load(openfile)

#     if len(photos) > 0 and len(messages) > 0:
#         random_num = random.randint(0, len(photos) - 1)
#         url = photos[random_num]['url']
#         expansion = photos[random_num]['expansion']
#         p = requests.get(url)
#         out = open(f'Images\dem_image.{expansion}', 'wb')
#         # out = open(f'Images/dem_image.{expansion}', 'wb')
#         out.write(p.content)
#         out.close()

#         # random_num_1 = random.randint(0, len(messages) - 1)
#         # random_num_2 = random.randint(0, len(messages) - 1)
#         # text_1 = messages[random_num_1]
#         # text_2 = messages[random_num_2]
#         text_1 = np.random.choice(messages)
#         text_2 = np.random.choice(messages)

#         # dem = Demotivator('mv-jadheedh-regular.ttf')
#         dem = Demotivator(DATA_FOLDER_FILE_PATH + 'gtwalsheimpro_condensedmediumoblique.otf')
#         dem.create_demotivator(
#             f'Images/dem_image.{expansion}',
#             text_1,
#             text_2
#         )
#         dem.save(f'Images/demotivator.{expansion}')
#         # message = 'Привет!'

#         upload = vk_api.VkUpload(vk_session)
#         photo = upload.photo_messages(f'Images/demotivator.{expansion}')
#         owner_id = photo[0]['owner_id']
#         photo_id = photo[0]['id']
#         access_key = photo[0]['access_key']
#         attachment = f'photo{owner_id}_{photo_id}_{access_key}'
#     else:
#         message = 'Опция недоступна!'

#     return message, attachment


# def apply_filter(img, kernel):
#     h, w = np.array(img.shape)
#     kh, kw = np.array(kernel.shape)
#     out = np.zeros((h - kh + 1, w - kw + 1))
#     for i in range(h - kh + 1):
#         for j in range(w - kw + 1):
#             patch = img[i : i + kh, j : j + kw]
#             new_pixel = np.multiply(patch, kernel).sum()
#             out[i, j] = new_pixel
#     return out


# def get_effect(vk_session):
#     message = None
#     attachment = None

#     photos = read_json('photos.json')
#     # with open('photos.json', mode='r') as openfile:
#     #     photos = json.load(openfile)

#     if len(photos) > 0:
#         random_num = random.randint(0, len(photos) - 1)
#         url = photos[random_num]['url']
#         expansion = photos[random_num]['expansion']
#         p = requests.get(url)
#         out = open(f'Images/effect_img.{expansion}', 'wb')
#         out.write(p.content)
#         out.close()

#         random_num = random.randint(0, len(photos) - 1)
#         url = photos[random_num]['url']
#         random_num = random.randint(0, len(EFFECTS) - 1)
#         effect = EFFECTS[random_num]

#         image = Image.open(f'Images/effect_img.{expansion}')
#         img_tensor = tf.convert_to_tensor(image).numpy().mean(axis=2)
#         fig, axes = plt.subplots(figsize=plt.figaspect(img_tensor))
#         axes.imshow(img_tensor, cmap=effect)
#         fig.subplots_adjust(0, 0, 1, 1)
#         axes.axis('off')
#         fig.savefig(f'Images/effect.{expansion}')
#         plt.close(fig)

#         upload = vk_api.VkUpload(vk_session)
#         photo = upload.photo_messages(f'Images/effect.png')
#         owner_id = photo[0]['owner_id']
#         photo_id = photo[0]['id']
#         access_key = photo[0]['access_key']
#         attachment = f'photo{owner_id}_{photo_id}_{access_key}'
#     else:
#         message = 'Опция недоступна!'

#     return message, attachment


def get_keyboards(users):
    keyboard_1 = VkKeyboard(**KEYBOARD_SETTINGS)
    keyboard_1.add_callback_button(
        label='Статист дня ',
        color=VkKeyboardColor.POSITIVE,
        payload={'type': 'Статист дня'}
    )

    keyboard_1.add_callback_button(
        label='Банка дня',
        color=VkKeyboardColor.NEGATIVE,
        payload={'type': 'Банка дня'}
    )

    keyboard_1.add_line()

    keyboard_1.add_callback_button(
        label='Инсайдерская инфа по T8',
        color=VkKeyboardColor.PRIMARY,
        payload={'type': 'Инсайдерская инфа по T8'}
    )

    keyboard_1.add_line()

    keyboard_1.add_callback_button(
        label='Быстрый бой',
        color=VkKeyboardColor.SECONDARY,
        payload={'type': 'Быстрый бой'}
    )

    keyboard_1.add_callback_button(
        label='Долгий бой',
        color=VkKeyboardColor.SECONDARY,
        payload={'type': 'Долгий бой'}
    )

    keyboard_1.add_line()

    keyboard_1.add_callback_button(
        label='Демотиватор',
        color=VkKeyboardColor.SECONDARY,
        payload={'type': 'Демотиватор'}
    )

    keyboard_1.add_callback_button(
        label='Ядро свёртки',
        color=VkKeyboardColor.SECONDARY,
        payload={'type': 'Ядро свёртки'}
    )

    keyboard_1.add_line()

    keyboard_1.add_callback_button(
        label='Лидерборд',
        color=VkKeyboardColor.PRIMARY,
        payload={'type': 'Лидерборд'}
    )

    keyboard_1.add_callback_button(
        label='Помощь',
        color=VkKeyboardColor.PRIMARY,
        payload={'type': 'Помощь'}
    )

    
    # 1
    # 2
    # 3
    # --
    # 4
    # 5
    # 6
    # --
    # 7
    # 8
    # 9
    # --

    keyboard_2 = VkKeyboard(**KEYBOARD_SETTINGS)
            
    for i, dic in enumerate(users, start=1):
        keyboard_2.add_callback_button(
            label=dic['first_last_name'],
            color=VkKeyboardColor.POSITIVE,
            payload={'type': dic['id']}
        )
        if i % 3 == 0 and i != len(users):
            keyboard_2.add_line()

    keyboard_2.add_line()

    keyboard_2.add_callback_button(
        label='Отменя боя',
        color=VkKeyboardColor.SECONDARY,
        payload={'type': 'Отмена боя'}
    )

    keyboard_3 = VkKeyboard(**KEYBOARD_SETTINGS)

    for i, dic in enumerate(TANKS, start=1):
        keyboard_3.add_callback_button(
            label=dic['id'],
            color=VkKeyboardColor.POSITIVE,
            payload={'type': dic['id']}
        )
        if i % 4 == 0 and i != len(TANKS):
            keyboard_3.add_line()
            
    keyboard_3.add_line()

    keyboard_3.add_callback_button(
        label='Отменя боя',
        color=VkKeyboardColor.SECONDARY,
        payload={'type': 'Отмена боя'}
    )

    return keyboard_1, keyboard_2, keyboard_3