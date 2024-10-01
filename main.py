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
users = users.read_json('users.json')

with open('photos.json', mode='r') as openfile:
    photos = json.load(openfile)

with open('messages.json', mode='r') as openfile:
    messages = json.load(openfile)


vk_session = VkApi(token=GROUP_TOKEN)
longpoll = VkBotLongPoll(vk_session, group_id=GROUP_ID)
vk = vk_session.get_api()


keyboard_1, keyboard_2, keyboard_3 = get_keyboards(users)


for event in longpoll.listen():

    random_id = random.randint(1, 10 ** 9)
    keyboard = keyboard_1
    message = None
    attachment = None

    if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
        chat_id = int(event.chat_id)
        message_text = event.object.message['text'].lower()
        user_id = event.object.message['from_id']

        try:
            url = event.object.message['attachments'][0]['doc']['url']
            expansion = event.object.message['attachments'][0]['doc']['ext']
            if expansion in ['png', 'jpg', 'jpeg']:
                photos.append({'url': url, 'expansion': expansion})
                with open('photos.json', mode='w') as outfile:
                    json.dump(photos, outfile)

        except IndexError:
            pass

        finally:
            if len(message_text) <= 10 and message_text not in ['выстрел', 'вылечить', 'потушить']:
                messages.append(message_text)
                with open('messages.json', mode='w') as outfile:
                    json.dump(messages, outfile)
        
        try:
            reply_message_text = event.object.message['reply_message']['text']
            reply_message_from_id = event.object.message['reply_message']['from_id']

            if reply_message_from_id == -GROUP_ID:
                if re.match('^[\[\]\|a-z0-9@_]+[а-яА-Я,"\?\.\n ]+$', reply_message_text):
                    if user_id == list(player_tanks.keys())[1]:
                        if message_text in ['да', 'д', 'согласен', 'согл', 'yes', 'y', 'lf']:
                            message = 'Выберите танк:'
                            keyboard = keyboard_3
                        else:
                            message = 'Отказано. Вы можете пригласить игрока заново'
                            player_tanks.clear()
        
        except Exception as e:
            print(f'EXCEPT: {e}')
            # message = f'ОШИБКА: {e}'
        
        # if battle_type == 'быстрый' and None not in player_tanks.values():
        #     message = 'Бой начинается!'
            
        if message_text.startswith('&'):
            message = 'Привет!'
        
        elif battle_type == 'долгий' and message_text == 'в':
            user_id_1 = list(player_tanks.keys())[0]
            user_id_2 = list(player_tanks.keys())[1]
            fire_damage = 500

            if tank_1.fire and user_id == user_id_2:
                # for k, v in reversed(tank_2.shots.items()):
                #     if isinstance(v, list) and tank_2.shots[k][1] == None:
                #         tank_2.shots[k][1] = fire_damage
                #         break
                #     elif isinstance(v, list) and tank_2.shots[k][1] != None:
                #         fire_damage = tank_2.shots[k][1]
                #         break
                # message = f"{player_tanks[user_id_1]['id']} стреляет по {player_tanks[user_id_2]['id']}:\n"
                # message += f"{num_shot_2}) {tank_1.hp} - {fire_damage} = {tank_1.hp - fire_damage} - урон от пожара\n"
                # tank_1.hp -= fire_damage
                # tank_1.fire = False
                # tank_1.start_fire_time = None
                message = tank_1.compute_fire(tank_2, player_tanks, user_id, num_shot_2, mode='2')
            
            elif tank_2.fire and user_id == user_id_1:
                # for k, v in reversed(tank_1.shots.items()):
                #     if isinstance(v, list) and tank_1.shots[k][1] == None:
                #         tank_1.shots[k][1] = fire_damage
                #         break
                #     elif isinstance(v, list) and tank_1.shots[k][1] != None:
                #         fire_damage = tank_1.shots[k][1]
                #         break
            
                # message = f"{player_tanks[user_id_2]['id']} стреляет по {player_tanks[user_id_1]['id']}:\n"
                # message += f"{num_shot_1}) {tank_2.hp} - {fire_damage} = {tank_2.hp - fire_damage} - урон от пожара\n"
                # tank_2.hp -= fire_damage
                # tank_2.fire = False
                # tank_2.start_fire_time = None
                message = tank_2.compute_fire(tank_1, player_tanks, user_id, num_shot_2, mode='2')


            # print('message =', message)
            # print(tank_1.id, tank_1.shots)
            # print(tank_2.id, tank_2.shots, '\n')
            # print('1 if', user_id, player_tanks[user_id]['id'], tank_1.fire, tank_2.fire, tank_1.start_fire_time, tank_2.start_fire_time)
            # print('2 if', user_id, player_tanks[user_id]['id'], tank_2.fire)



            if user_id == user_id_1:
                print('1 user')
                if datetime.now() > shot_time_1:
                    num_shot_1 += 1
                    if message == None:
                        message = f"{player_tanks[user_id_1]['id']} стреляет по {player_tanks[user_id_2]['id']}:\n"
                    message += f"{num_shot_1}) {tank_2.hp} "
                    damage = tank_1.give_damage(tank_2, battle_type, start_time)
                    if tank_2.hp <= 0:
                        if tank_1.fire:
                            # fire_time = (datetime.now() - tank_1.start_fire_time).total_seconds()
                            # fire_damage = int(fire_time * 100)
                            # if fire_damage > 500:
                            #     fire_damage = 500
                            # for k, v in reversed(tank_2.shots.items()):
                            #     if isinstance(v, list) and tank_2.shots[k][1] == None:
                            #         tank_2.shots[k][1] = fire_damage
                            #         break
                            # tank_1.hp -= fire_damage
                            # tank_1.fire = False
                            # tank_1.start_fire_time = None
                            message = tank_1.compute_fire(tank_2, player_tanks, user_id, num_shot_2, mode='0')

                            # print('1 if\n1T SHOTS', tank_1.shots, '\n')
                            # print('2T SHOTS', tank_2.shots, '\n')
                        tank_2.hp = 0
                        tank_1.update_dict(tank_2, user_id_1, user_id_2, users)
                        message = tank_1.get_message(tank_2)
                        users = tank_1.update_json(tank_2, user_id_1, user_id_2, users)
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
                # try:
                #     print('1 if', user_id, player_tanks[user_id]['id'], tank_1.fire, tank_2.fire, tank_1.start_fire_time, tank_2.start_fire_time, '\n\n\n')
                #     # print('2 if', user_id, player_tanks[user_id]['id'], tank_2.fire, '\n\n\n')
                # except:
                #     print('E', '\n\n\n')
                
            elif user_id == user_id_2:
                print('2 user')
                if datetime.now() > shot_time_2:
                    num_shot_2 += 1
                    if message == None:
                        message = f"{player_tanks[user_id_2]['id']} стреляет по {player_tanks[user_id_1]['id']}:\n"
                    message += f"{num_shot_2}) {tank_1.hp} "
                    damage = tank_2.give_damage(tank_1, battle_type, start_time)
                    if tank_1.hp <= 0:
                        if tank_2.fire:
                            # fire_time = (datetime.now() - tank_2.start_fire_time).total_seconds()
                            # print(user_id, fire_time)
                            # fire_damage = int(fire_time * 100)
                            # if fire_damage > 500:
                            #     fire_damage = 500
                            # for k, v in reversed(tank_1.shots.items()):
                            #     if isinstance(v, list) and tank_1.shots[k][1] == None:
                            #         tank_1.shots[k][1] = fire_damage
                            #         break
                            # tank_2.hp -= fire_damage
                            # tank_2.fire = False
                            # tank_2.start_fire_time = None
                            # print('1 if\n1T SHOTS', tank_1.shots, '\n')
                            # print('2T SHOTS', tank_2.shots, '\n')
                            message = tank_2.compute_fire(tank_1, player_tanks, user_id, num_shot_2, mode='0')

                        tank_1.hp = 0
                        tank_1.update_dict(tank_2, user_id_1, user_id_2, users)
                        message = tank_1.get_message(tank_2)
                        users = tank_1.update_json(tank_2, user_id_1, user_id_2, users)
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

        elif battle_type == 'долгий' and message_text == 'п':
            user_id_1 = list(player_tanks.keys())[0]
            user_id_2 = list(player_tanks.keys())[1]
            if user_id == user_id_1 and tank_1.fire:
                # fire_time = (datetime.now() - tank_1.start_fire_time).total_seconds()
                # print(user_id, fire_time)
                # fire_damage = int(fire_time * 100)
                # for k, v in reversed(tank_2.shots.items()):
                #     if isinstance(v, list):
                #         tank_2.shots[k][1] = fire_damage
                #         break
                # message = f"Пожар {player_tanks[user_id]['id']} потушен"
                # tank_1.hp -= fire_damage
                # tank_1.fire = False
                # tank_1.start_fire_time = None
                message = tank_1.compute_fire(tank_2, player_tanks, user_id, num_shot_2, mode='1')


            elif user_id == user_id_2 and tank_2.fire:
                # fire_time = (datetime.now() - tank_2.start_fire_time).total_seconds()
                # fire_damage = int(fire_time * 100)
                # for k, v in reversed(tank_1.shots.items()):
                #     if isinstance(v, list):
                #         tank_1.shots[k][1] = fire_damage
                #         break
                # message = f"Пожар {player_tanks[user_id]['id']} потушен"
                # tank_2.hp -= fire_damage
                # tank_2.fire = False
                # tank_2.start_fire_time = None
                message = tank_2.compute_fire(tank_1, player_tanks, user_id, num_shot_2, mode='1')



        elif battle_type == 'долгий' and message_text == 'выл':
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
        
        if button_value == 'Игрок дня':
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
                message = 'Бой уже идёт!'
            
        elif button_value == 'Отмена боя':
            user = [dic for dic in users if dic['id'] == user_id][0]
            player_tanks.clear()
            battle_type = None
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

