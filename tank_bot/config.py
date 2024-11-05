import numpy as np

GROUP_ID = 226416696

GROUP_TOKEN = '''vk1.a.dBgqASfEk_UEHceRLCGZtxQhSc-FM6U39rfWbKR9mVzdbWO0D2trKAoC_vr26Ke9hr5ylMbwKc
veGCY_l1F01nB0hVH7EnCVsFhaB4oT1iIN79O8nwdkG-1MgaKSs6tugkAbdxp_KIX7D_5TJSWyjLRpY5JIn29U178dIrakqiP
OK_fTIbfFPE0gIDbzUIxeqmWIr4csmRkdornG17O6LQ''' #LU-XE

USER_IDS = [
    [271414666, '☢️'], #Даня М
    [352572288, '👶'], #Боря
    [342942391, '🤬'], #Вадя
    [495188885, '🔞'], #Даня С
    [171292172, '👴🏻'], #Евгений
    [249200120, '🦾'], #Я
    [328330195, '♿️'], #Лёша
    [253737037, '🦁'], #Мага
    [279614752, '🧠'], #Чопель
    [218260735, '🚑'], #Тимофей
    [865092166, '🚑']
]

JSON_FILE_PATH = './data/json/'
IMAGES_FILE_PATH = './data/images/'
FONTS_FILE_PATH = './data/fonts/'

KEYBOARD_SETTINGS = dict(inline=False, one_time=False)

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

np.random.shuffle(TANKS)
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
# GROUP_TOKEN = '''vk1.a.GqXNacaJEtuM_Ew62A_BHvKMOvqGYlO5rUdPg1CGnDmid1fzeECZtqWwXXK_I8Zdrs-WCAz3ia
# KY1azls8VI-mmrIXtVmpbKnNReWoqp3xOAwcW_bHTCDIpSQSgUeEVhqXzshoC4SxO0XWoECt3kvi7UKCB6wp71her01fGlHfh
# Ws4VX69Wv5Z0DIf-hdSTYD64DaiUUjnHu4Al0DrAesA''' #ENEMY
# GROUP_ID = 226106896 #Японская жаба