import random
import numpy as np
from datetime import datetime


class Tank:
    # def __init__(self, **kwargs):
    #     self.shots = {}
    #     self.__dict__.update(kwargs)

    def __init__(self, id, class_, hp, damage, reload, breakout_prob, fire_prob):
        self.id = id
        self.class_ = class_
        self.hp = hp
        self.max_hp = hp
        self.damage = damage
        self.reload = reload
        self.breakout_prob = breakout_prob
        self.fire_prob = fire_prob
        self.shots = {}
        self.fire = False
        self.enemy_death = 0
        self.start_fire_time = 0
        self.charger_prob = 0.08
        self.charger_krit = False

    
    def give_damage(self, tank, battle_type, start_time=datetime.now()):
        if random.random() < tank.breakout_prob:
            random_num = np.random.normal(0.0, 0.1, 1)[0]
            random_num = (
                0.25 if random_num > 0.25 else
                -0.25 if random_num < -0.25 else
                random_num
            )
            real_damage = round((1 + random_num) * self.damage)
            tank.hp -= real_damage
            if (battle_type == 'долгий') and (tank.hp > 500) and (random.random() < tank.fire_prob):
                tank.fire = True
                tank.start_fire_time = datetime.now()
                real_damage = [real_damage, None]
            elif (battle_type == 'долгий') and (tank.hp > self.damage * 1.25) and (random.random() < tank.charger_prob):
                tank.charger_krit = True
                tank.reload *= 1.9
                real_damage = [real_damage, 'Вражеский заряжающий контужен']
            if battle_type == 'быстрый':
                self.enemy_death += self.reload
            elif battle_type == 'долгий':
                self.enemy_death = round((datetime.now() - start_time).total_seconds(), 2)
            self.shots[self.enemy_death] = real_damage
        else:
            real_damage = 'Броня не пробита!'
            self.enemy_death += self.reload
            self.shots[self.enemy_death] = real_damage
        return real_damage
    

    def compute_fire(self, tank, player_tanks, user_id_1, user_id_2, num_shot=0, mode='0'):
        message = None
        fire_time = (datetime.now() - self.start_fire_time).total_seconds()
        fire_damage = int(fire_time * 100)
        fire_damage = min(500, fire_damage)
        for k, v in reversed(tank.shots.items()):
            if isinstance(v, list) and tank.shots[k][1] == None:
                tank.shots[k][1] = fire_damage
                break
            elif isinstance(v, list) and tank.shots[k][1] != None:
                fire_damage = tank.shots[k][1]
                break
        if mode == '1':
            message = f"Пожар {player_tanks[user_id_1]['id']} потушен"
        elif mode == '2':
            message = f"{player_tanks[user_id_1]['id']} стреляет по {player_tanks[user_id_2]['id']}:\n"
            message += f"{num_shot}) {self.hp} - {fire_damage} = {self.hp - fire_damage} - урон от пожара\n"
        if mode in ['0', '2']:
            self.hp -= fire_damage
            self.fire = False
            self.start_fire_time = None
        return message
                
    
    def update_hp_and_shots(self, tank):
        if self.enemy_death < tank.enemy_death:
            tank.shots = {
                k: v for k, v in tank.shots.items()
                if k <= self.enemy_death
            }
            self.hp = self.max_hp - sum(
                [v for v in tank.shots.values() if isinstance(v, int)]
            )
            tank.hp = 0
            
        elif self.enemy_death > tank.enemy_death:
            self.hp = 0
            self.shots = {
                k: v for k, v in self.shots.items()
                if k <= tank.enemy_death
            }
            tank.hp = tank.max_hp - sum(
                [v for v in self.shots.values() if isinstance(v, int)]
            )
            
        else:
            self.hp = 0
            tank.hp = 0
            
            
    def update_dict(self, tank, user_id_1, user_id_2, users):
        user_fln_1 = [dic for dic in users if dic['id'] == user_id_1][0]['first_last_name']
        user_fln_2 = [dic for dic in users if dic['id'] == user_id_2][0]['first_last_name']
        
        if self.hp == 0 and tank.hp == 0:
            winner = f'{user_fln_1} и {user_fln_2}'
        elif self.hp == 0:
            winner = user_fln_2
        elif tank.hp == 0:
            winner = user_fln_1
            
        if self.hp > 0:
            self.shots[1000] = 'Вы уничтожили танк противника!\n'
        else:
            self.shots[1000] = 'Ваш танк уничтожен!\n'
        
        if tank.hp > 0:
            tank.shots[1000] = 'Вы уничтожили танк противника!'
            tank.shots[2000] = f'\nВремя боя: {round(tank.enemy_death, 2)}'
        else:
            tank.shots[1000] = 'Ваш танк уничтожен!'
            tank.shots[2000] = f'\nВремя боя: {round(self.enemy_death, 2)}'

        if ' и ' in winner:
            tank.shots[3000] = f'\nВ этот раз у нас два победителя (проигравших?): {winner}'
        else:
            tank.shots[3000] = f'\nЧествуем победителя: {winner}'            
        
        
    def get_message(self, tank):
        message = f'{self.id} стреляет по {tank.id}:\n'
        hp = tank.max_hp
        
        for shot_num, damage in enumerate(self.shots.values(), start=1):
            if isinstance(damage, int):
                if hp - damage >= 0:
                    message += f'{shot_num}) {hp} - {damage} = {hp - damage}\n'
                    hp -= damage
                else:
                    message += f'{shot_num}) {hp} - {damage} < 0\n'
            elif damage == 'Броня не пробита!':
                message += f'{shot_num}) {damage}\n'
            elif isinstance(damage, list):
                if isinstance(damage[1], int):
                    message += f'{shot_num}) {hp} - {damage[0]} = {hp - damage[0]}\n'
                    hp -= damage[0]
                    message += f'{shot_num}) {hp} - {damage[1]} = {hp - damage[1]} - урон от пожара\n'
                    hp -= damage[1]
                elif isinstance(damage[1], str):
                    message += f'{shot_num}) {hp} - {damage[0]} = {hp - damage[0]}\n'
                    hp -= damage[0]
                    message += f'{shot_num}) {damage[1]}\n'
            else:
                message += f'{damage}\n'
                
        message += f'{tank.id} стреляет по {self.id}:\n'
        hp = self.max_hp
        
        for shot_num, damage in enumerate(tank.shots.values(), start=1):
            if isinstance(damage, int):
                if hp - damage >= 0:
                    message += f'{shot_num}) {hp} - {damage} = {hp - damage}\n'
                    hp -= damage
                else:
                    message += f'{shot_num}) {hp} - {damage} < 0\n'
            elif damage == 'Броня не пробита!':
                message += f'{shot_num}) {damage}\n'
            elif isinstance(damage, list):
                if isinstance(damage[1], int):
                    message += f'{shot_num}) {hp} - {damage[0]} = {hp - damage[0]}\n'
                    hp -= damage[0]
                    message += f'{shot_num}) {hp} - {damage[1]} = {hp - damage[1]} - урон от пожара\n'
                    hp -= damage[1]
                elif isinstance(damage[1], str):
                    message += f'{shot_num}) {hp} - {damage[0]} = {hp - damage[0]}\n'
                    hp -= damage[0]
                    message += f'{shot_num}) {damage[1]}\n'
            else:
                message += f'{damage}\n'

        return message
    
    
    def update_json(self, tank, user_id_1, user_id_2, users):
        for dic in users:
            if dic['id'] == user_id_1:
                dic['battles'] += 1
                if self.hp == 0 and tank.hp == 0:
                    damage = tank.max_hp
                elif self.hp != 0: # !=
                    dic['wins'] += 1
                    damage = tank.max_hp
                else:
                    damage = sum([v for v in self.shots.values() if isinstance(v, int)])
                dic['damage'].append(damage)
                
            elif dic['id'] == user_id_2:
                dic['battles'] += 1
                if self.hp == 0 and tank.hp == 0:
                    damage = self.max_hp
                elif tank.hp != 0: # !=
                    dic['wins'] += 1
                    damage = self.max_hp
                else:
                    damage = sum([v for v in tank.shots.values() if isinstance(v, int)])
                dic['damage'].append(damage)
                
        return users