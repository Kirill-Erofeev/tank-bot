import json
import vk_api
import random
import requests
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt


from .config import *
from PIL import Image
from datetime import date
from demotivator import Demotivator
from datetime import datetime, timedelta
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


player_tanks = {}
battle_type = None

def create_users_json(vk):
    user_ids = list(map(lambda x: x[0], USER_IDS))
    emoji = list(map(lambda x: x[1], USER_IDS))
    users_list = vk.users.get(user_ids=user_ids, fields=['domain'])
    user_info = ['id', 'domain', 'first_name', 'last_name']
    users_list = [
        {key: value for key, value in dic.items() if key in user_info}
        for dic in users_list
    ]
    for i, dic in enumerate(users_list):
        first_name = dic['first_name']
        last_name = dic['last_name']
        dic['first_last_name'] = f'{first_name} {last_name}'
        # dic['first_last_name'] = f'{} {}'.format(dic['first_name'], dic['last_name'])
        dic['battles'] = 0
        dic['wins'] = 0
        dic['damage'] = []
        dic['emoji'] = emoji[i]
        del dic['first_name']
        del dic['last_name']
    
    with open(JSON_FILE_PATH + 'users.json', mode='w') as outfile:
        json.dump(users_list, outfile)


def read_json(file_name):
    try:
        with open(JSON_FILE_PATH + file_name, mode='r') as openfile:
            lst = json.load(openfile)
    except FileNotFoundError:
        lst = []
    return lst


def get_loser(users):
    np.random.seed(date.today().day)
    random_user_dic = np.random.choice(users)
    random_user_domain = random_user_dic['first_last_name']
    loser = f'Банка дня: {random_user_domain}'
    return loser


def get_winner(users):
    np.random.seed(abs(date.today().day - date.today().month))
    random_user_dic = np.random.choice(users)
    random_user_domain = random_user_dic['first_last_name']
    winner = f'Статист дня: {random_user_domain}'
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

    if len(photos) > 0 and len(messages) > 0:
        random_num = random.randint(0, len(photos) - 1)
        url = photos[random_num]['url']
        expansion = photos[random_num]['expansion']
        p = requests.get(url)
        out = open(f'./data/images/dem_image.{expansion}', 'wb')
        out.write(p.content)
        out.close()
        text_1 = np.random.choice(messages)
        text_2 = np.random.choice(messages)

        dem = Demotivator(FONTS_FILE_PATH + 'ofont.ru_Geologica.ttf')
        dem.create_demotivator(
            f'./data/images/dem_image.{expansion}',
            text_1,
            text_2
        )
        dem.save(f'./data/images//demotivator.{expansion}')

        upload = vk_api.VkUpload(vk_session)
        photo = upload.photo_messages(f'./data/images/demotivator.{expansion}')
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

    if len(photos) > 0:
        random_num = random.randint(0, len(photos) - 1)
        url = photos[random_num]['url']
        expansion = photos[random_num]['expansion']
        p = requests.get(url)
        out = open(f'./data/images/effect_img.{expansion}', 'wb')
        out.write(p.content)
        out.close()

        random_num = random.randint(0, len(photos) - 1)
        url = photos[random_num]['url']
        random_num = random.randint(0, len(EFFECTS) - 1)
        effect = EFFECTS[random_num]

        image = Image.open(f'./data/images/effect_img.{expansion}')
        img_tensor = tf.convert_to_tensor(image).numpy().mean(axis=2)
        fig, axes = plt.subplots(figsize=plt.figaspect(img_tensor))
        axes.imshow(img_tensor, cmap=effect)
        fig.subplots_adjust(0, 0, 1, 1)
        axes.axis('off')
        fig.savefig(f'./data/images/effect.{expansion}')
        plt.close(fig)

        upload = vk_api.VkUpload(vk_session)
        photo = upload.photo_messages(f'./data/images/effect.png')
        owner_id = photo[0]['owner_id']
        photo_id = photo[0]['id']
        access_key = photo[0]['access_key']
        attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    else:
        message = 'Опция недоступна!'

    return message, attachment



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

    np.random.shuffle(TANKS)
    TANKS = TANKS[:36]

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