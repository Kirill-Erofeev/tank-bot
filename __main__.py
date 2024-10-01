import re
import json
import vk_api
import random
import requests
import numpy as np
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from datetime import datetime, timedelta, date
from functools import reduce
from tank import Tank
from vkusers import VKUsers
from demotivator import Demotivator
from functions import *

users = VKUsers(GROUP_ID, GROUP_TOKEN)
users = read_json('users.json')
photos = read_json('photos.json')
messages = read_json('messages.json')

# with open('photos.json', mode='r') as openfile:
#     photos = json.load(openfile)

# with open('messages.json', mode='r') as openfile:
#     messages = json.load(openfile)


vk_session = VkApi(token=GROUP_TOKEN)
longpoll = VkBotLongPoll(vk_session, group_id=GROUP_ID)
vk = vk_session.get_api()
long_battle = False
lock = False


keyboard_1, keyboard_2, keyboard_3 = get_keyboards(users)


for event in longpoll.listen():

    random_id = random.randint(1, 10 ** 9)
    keyboard = keyboard_1
    message = None
    attachment = None

    if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
        # print('12')
        chat_id = int(event.chat_id)
        message_text = event.object.message['text'].lower()
        user_id = event.object.message['from_id']
        # print(event.object.message['attachments'][0]['doc']['url'])
        # print(event.object.message['attachments'][0]['doc']['ext'])
        try:
            url = event.object.message['attachments'][0]['doc']['url']
            # print(url)
            expansion = event.object.message['attachments'][0]['doc']['ext']
            if expansion in ['png', 'jpg', 'jpeg']:
                photos.append({'url': url, 'expansion': expansion})
                # print(photos)
                with open(DATA_FOLDER_FILE_PATH + 'photos.json', mode='w') as outfile:
                    json.dump(photos, outfile)

        except:
        # except IndexError:
            pass

        finally:
            if len(message_text) <= 15 and message_text not in ['выстрел', 'вылечить', 'потушить', 'завершить бой', '', '&', None]:
                messages.append(message_text)
                with open(DATA_FOLDER_FILE_PATH + 'messages.json', mode='w') as outfile:
                    json.dump(messages, outfile)
        
        try:
            reply_message_text = event.object.message['reply_message']['text']
            reply_message_from_id = event.object.message['reply_message']['from_id']

            if reply_message_from_id == -GROUP_ID:
                if re.match('^[\[\]\|a-z0-9@_]+[а-яА-ЯёЁa-zA-Z,"\?\.\n ]+$', reply_message_text):
                    # invited_user = [dic for dic in users if dic['id'] == list(player_tanks.keys())[0]][0]
                    # fln = invited_user['first_last_name']
                    if user_id == list(player_tanks.keys())[1]:
                        if (datetime.now() - invite_time).total_seconds() < 180:
                            if message_text in ['да', 'д', 'согласен', 'согл', 'yes', 'y', 'lf']:
                                if battle_type == 'долгий':
                                    long_battle = True
                                message = 'Выберите танк:'
                                keyboard = keyboard_3
                            else:
                                message = 'Получен отказ, бой отменён'
                                battle_type = None
                                player_tanks.clear()
                        else:
                            message = 'Время приглашения истекло, бой отменён'
                            battle_type = None
                            player_tanks.clear()
        
        except Exception as e:
            pass
            # print(f'EXCEPT: {e}')
            # message = f'ОШИБКА: {e}'
        
        # if battle_type == 'быстрый' and None not in player_tanks.values():
        #     message = 'Бой начинается!'
            
        if message_text.startswith('&'):
            message = 'Привет!'
        
        elif battle_type == 'долгий' and message_text == 'выстрел':
            user_id_1 = list(player_tanks.keys())[0]
            user_id_2 = list(player_tanks.keys())[1]

            if user_id == user_id_1:
                # print('1 user')
                if datetime.now() > shot_time_1:
                    if tank_2.fire and user_id == user_id_1:
                        message = tank_2.compute_fire(
                            tank_1,
                            player_tanks,
                            user_id_1,
                            user_id_2,
                            num_shot_1,
                            mode='2'
                        )
                    num_shot_1 += 1
                    if message == None:
                        message = f"{player_tanks[user_id_1]['id']} стреляет по {player_tanks[user_id_2]['id']}:\n"
                    message += f"{num_shot_1}) {tank_2.hp} "
                    damage = tank_1.give_damage(tank_2, battle_type, start_time)
                    if tank_2.hp <= 0:
                        if tank_1.fire:
                            message = tank_1.compute_fire(
                                tank_2,
                                player_tanks,
                                user_id_1,
                                user_id_2,
                                # num_shot_2,
                                mode='0'
                            )
                        tank_2.hp = 0
                        tank_1.update_dict(tank_2, user_id_1, user_id_2, users)
                        message = tank_1.get_message(tank_2)
                        users = tank_1.update_json(tank_2, user_id_1, user_id_2, users)
                        with open(DATA_FOLDER_FILE_PATH + 'users.json', mode='w') as outfile:
                            json.dump(users, outfile)
                        long_battle = False
                        battle_type = None
                        player_tanks.clear()
                    else:
                        shot_time_1 = datetime.now() + timedelta(seconds=tank_1.reload)
                        if isinstance(damage, int):
                            message += f'- {damage} = {tank_2.hp}'
                        elif isinstance(damage, str):
                            message = f'{num_shot_1}) {damage}'
                        elif isinstance(damage, list):
                            if isinstance(damage[1], int) or damage[1] == None:
                                message += f'- {damage[0]} = {tank_2.hp}\nПротивник в огне!'
                            elif isinstance(damage[1], str):
                                message += f'- {damage[0]} = {tank_2.hp}\n{damage[1]}'
#                         message += f'- {damage} = {tank_2.hp}'
                        
                else:
                    message = f'Орудие {tank_1.id} перезаряжается!'
                
            elif user_id == user_id_2:
                # print('2 user')
                if datetime.now() > shot_time_2:
                    if tank_1.fire and user_id == user_id_2:
                        message = tank_1.compute_fire(
                            tank_2,
                            player_tanks,
                            user_id_2,
                            user_id_1,
                            num_shot_2,
                            mode='2'
                        )
                    num_shot_2 += 1
                    if message == None:
                        message = f"{player_tanks[user_id_2]['id']} стреляет по {player_tanks[user_id_1]['id']}:\n"
                    message += f"{num_shot_2}) {tank_1.hp} "
                    damage = tank_2.give_damage(tank_1, battle_type, start_time)
                    if tank_1.hp <= 0:
                        if tank_2.fire:
                            message = tank_2.compute_fire(
                                tank_1,
                                player_tanks,
                                user_id_2,
                                user_id_1,
                                # num_shot_2,
                                mode='0'
                            )
                        tank_1.hp = 0
                        tank_1.update_dict(tank_2, user_id_1, user_id_2, users)
                        message = tank_1.get_message(tank_2)
                        users = tank_1.update_json(tank_2, user_id_1, user_id_2, users)
                        with open(DATA_FOLDER_FILE_PATH + 'users.json', mode='w') as outfile:
                            json.dump(users, outfile)
                        long_battle = False
                        battle_type = None
                        player_tanks.clear()
                    else:
                        shot_time_2 = datetime.now() + timedelta(seconds=tank_2.reload)
                        if isinstance(damage, int):
                            message += f'- {damage} = {tank_1.hp}'
                        elif isinstance(damage, str):
                            message = f'{num_shot_2}) {damage}'
                        # elif isinstance(damage, list):
                        #     message += f'- {damage[0]} = {tank_1.hp}. ВРАГ ГОРИТ!'
                        elif isinstance(damage, list):
                            if isinstance(damage[1], int) or damage[1] == None:
                                message += f'- {damage[0]} = {tank_1.hp}\nПротивник в огне!'
                            elif isinstance(damage[1], str):
                                message += f'- {damage[0]} = {tank_1.hp}\n{damage[1]}'
                else:
                    message = f'Орудие {tank_2.id} перезаряжается!'

        elif battle_type == 'долгий' and message_text == 'потушить':
            user_id_1 = list(player_tanks.keys())[0]
            user_id_2 = list(player_tanks.keys())[1]
            if user_id == user_id_1 and tank_1.fire:
                message = tank_1.compute_fire(
                    tank_2,
                    player_tanks,
                    user_id_1,
                    user_id_2,
                    # num_shot_2,
                    mode='1'
                )
            elif user_id == user_id_2 and tank_2.fire:
                message = tank_2.compute_fire(
                    tank_1,
                    player_tanks,
                    user_id_2,
                    user_id_1,
                    # num_shot_2,
                    mode='1'
                )



        elif battle_type == 'долгий' and message_text == 'вылечить':
            user_id_1 = list(player_tanks.keys())[0]
            user_id_2 = list(player_tanks.keys())[1]
            if user_id == user_id_1 and tank_1.charger_krit:
                tank_1.reload /= 1.9
                tank_1.charger_krit = False
                message = f"Заряжающий {player_tanks[user_id]['id']} вылечен"
            elif user_id == user_id_2 and tank_2.charger_krit:
                tank_2.reload /= 1.9
                tank_2.charger_krit = False
                message = f"Заряжающий {player_tanks[user_id]['id']} вылечен"
        


        try:
            if battle_type != None and message_text == 'отменить приглашение' and long_battle == False and lock:
                if (datetime.now() - invite_time).total_seconds() > 180:
                    user = [dic for dic in users if dic['id'] == user_id][0]
                    battle_type = None
                    player_tanks.clear()
                    message = f"{user['first_last_name']} отменяет приглашение, поскольку прошло больше трёх минут"
        except NameError:
            pass

        try:
            if battle_type == 'долгий' and message_text == 'завершить бой' and lock:
                if (datetime.now() - start_time).total_seconds() > 180 and user_id not in player_tanks.keys():
                    user = [dic for dic in users if dic['id'] == user_id][0]
                    battle_type = None
                    player_tanks.clear()
                    message = f"{user['first_last_name']} завершает бой, поскольку он шёл больше трёх минут"
        except NameError:
            pass                    


        if message != None:
            vk.messages.send(
                random_id=random_id,
                chat_id=chat_id,
                keyboard=keyboard.get_keyboard(),
                message=message
            )

        
    elif event.type == VkBotEventType.MESSAGE_EVENT:
        user_id = event.object.user_id
        button_value = event.object.payload['type']
        chat_id = event.object.peer_id
        user = [dic for dic in users if dic['id'] == user_id][0]
        tank_ids = list(map(lambda dic: dic['id'], TANKS))
        
        if button_value == 'Статист дня':
            message = get_winner(users)
            
        elif button_value == 'Банка дня':
            message = get_loser(users)
            
        elif button_value == 'Инсайдерская инфа по T8':
            message = get_best_teams(T12_TEAMS)
            
        elif button_value == 'Лидерборд':
            message = get_leaderboard(users)
            
        elif button_value in ['Быстрый бой', 'Долгий бой']:
            if len(player_tanks) == 0:
                battle_type = 'быстрый' if button_value == 'Быстрый бой' else 'долгий'
                message = 'Выбор соперника'
                keyboard = keyboard_2
            else:
                message = 'Приглашение уже отправлено или бой уже идёт!'
            
        elif button_value == 'Отмена боя':
            user = [dic for dic in users if dic['id'] == user_id][0]
            battle_type = None
            player_tanks.clear()
            message = f"{user['first_last_name']} отменяет бой"
        
        elif button_value == 'Демотиватор':
            message, attachment = get_demotivator(vk_session)

        elif button_value == 'Ядро свёртки':
            message, attachment = get_effect(vk_session)

        elif button_value == 'Помощь':
            message = BOT_INFO
            
        elif isinstance(button_value, int):
            user = [dic for dic in users if dic['id'] == user_id][0]
            fln = user['first_last_name']
            target_user = [dic for dic in users if dic['id'] == button_value][0]
            target_domain = target_user['domain']
            if button_value != user_id:
                invite_time = datetime.now()
                player_tanks[user_id] = None
                player_tanks[button_value] = None
                message = f'@{target_domain}, {fln} вызывает тебя на {battle_type} бой.'
                message += '\nДля подтверждения согласия необходимо написать "да", ответив на это сообщение.'
            else:
                message = f'@{target_domain}, считаешь себя самым умным?'
        
          
        elif button_value in tank_ids:
            user_domain = user['domain']
            user_fln = user['first_last_name']
            if user_id in player_tanks.keys():
                tank_info = [dic for dic in TANKS if dic['id'] == button_value][0]
                player_tanks[user_id] = tank_info
                # message = f'Выбор @{user_domain}: {button_value}'
                # message = f'{user_fln} выбирает {button_value}'
                message = f'{user_fln} сделал свой выбор'
                if None in player_tanks.values():
                    keyboard = keyboard_3
                else:
                    keyboard = keyboard_1
            else:
                keyboard = keyboard_3
                message = 'Не тот игрок выбрал танк!'
            
            if battle_type == 'быстрый' and None not in player_tanks.values():
                user_id_1 = list(player_tanks.keys())[0]
                user_id_2 = list(player_tanks.keys())[1]
                tank_1 = Tank(**player_tanks[user_id_1])
                tank_2 = Tank(**player_tanks[user_id_2])
                
                while tank_2.hp > 0:
                    damage = tank_1.give_damage(tank_2, battle_type)
                        
                while tank_1.hp > 0:
                    damage = tank_2.give_damage(tank_1, battle_type)
                
#                 42 < 46
#                 46 > 42

                tank_1.update_hp_and_shots(tank_2)
#                 winner = tank_1.get_winner(tank_2, id_1, id_2)
                tank_1.update_dict(tank_2, user_id_1, user_id_2, users)
                message = tank_1.get_message(tank_2)
                users = tank_1.update_json(tank_2, user_id_1, user_id_2, users)
                with open(DATA_FOLDER_FILE_PATH + 'users.json', mode='w') as outfile:
                    json.dump(users, outfile)
                player_tanks.clear()
                battle_type = None
                
            elif battle_type == 'долгий' and None not in player_tanks.values():
                user_id_1 = list(player_tanks.keys())[0]
                user_id_2 = list(player_tanks.keys())[1]
                tank_1 = Tank(**player_tanks[user_id_1])
                tank_2 = Tank(**player_tanks[user_id_2])
                start_time = datetime.now()
                shot_time_1 = datetime.now()
                shot_time_2 = datetime.now()
                num_shot_1 = 0
                num_shot_2 = 0
                message = 'Бой начинается!'
                
        
        vk.messages.send(
            peer_id=event.object.peer_id,
            random_id=random_id,
            keyboard=keyboard.get_keyboard(),
            message=message,
            attachment=attachment
        )
    
    if keyboard in [keyboard_2, keyboard_3]:
        lock = False
    elif keyboard == keyboard_1:
        lock = True

            # if tank_1.fire and user_id == user_id_2:
            #     for k, v in reversed(tank_2.shots.items()):
            #         if isinstance(v, list) and tank_2.shots[k][1] == None:
            #             tank_2.shots[k][1] = fire_damage
            #             break
            #         elif isinstance(v, list) and tank_2.shots[k][1] != None:
            #             fire_damage = tank_2.shots[k][1]
            #             break
            #     message = f"{player_tanks[user_id_1]['id']} стреляет по {player_tanks[user_id_2]['id']}:\n"
            #     message += f"{num_shot_2}) {tank_1.hp} - {fire_damage} = {tank_1.hp - fire_damage} - урон от пожара\n"
            #     tank_1.hp -= fire_damage
            #     tank_1.fire = False
            #     tank_1.start_fire_time = None

            # if tank_1.fire and user_id == user_id_1:
            #     fire_time = (datetime.now() - tank_1.start_fire_time).total_seconds()
            #     fire_damage = int(fire_time * 100)
            #     if fire_damage > 500:
            #         fire_damage = 500
            #     for k, v in reversed(tank_2.shots.items()):
            #         if isinstance(v, list) and tank_2.shots[k][1] == None:
            #             tank_2.shots[k][1] = fire_damage
            #             break
            #     tank_1.hp -= fire_damage
            #     tank_1.fire = False
            #     tank_1.start_fire_time = None

            # if user_id == user_id_1 and tank_1.fire:
            #     fire_time = (datetime.now() - tank_1.start_fire_time).total_seconds()
            #     print(user_id, fire_time)
            #     fire_damage = int(fire_time * 100)
            #     for k, v in reversed(tank_2.shots.items()):
            #         if isinstance(v, list):
            #             tank_2.shots[k][1] = fire_damage
            #             break
            #     message = f"Пожар {player_tanks[user_id]['id']} потушен"
            #     tank_1.hp -= fire_damage
            #     tank_1.fire = False
            #     tank_1.start_fire_time = None

