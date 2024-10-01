import json
from vk_api import VkApi


class VKUsers:
    DATA_FOLDER_FILE_PATH = './data/'

    def __init__(self, group_id, group_token):
        self.group_id = group_id
        self.group_token = group_token
        
    def get_users_list(self, user_ids, fields):
        vk_session = VkApi(token=self.group_token)
        vk = vk_session.get_api()
        users_list = vk.users.get(user_ids=user_ids, fields=fields)
        return users_list
        
    
    def get_users_dict(self, users_list):
        users_dict = {}
        for dic in users_list:
            user_id = dic['id']
            domain = dic['domain']
            first_name = dic['first_name']
            last_name = dic['last_name']
            users_dict[user_id] = [domain, f'{first_name} {last_name}']
#         users_dict = {str(dic['id']): [dic['domain'], f"{dic['first_name']} {dic['last_name']}"] for dic in users_list}
        return users_dict
    
    def get_users_list_1(self, user_info):
        user_ids = list(map(lambda x: x[0], user_info))
        emoji = list(map(lambda x: x[1], user_info))
        vk_session = VkApi(token=self.group_token)
        vk = vk_session.get_api()
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
#             dic['first_last_name'] = f'{} {}'.format(dic['first_name'], dic['last_name'])
            dic['battles'] = 0
            dic['wins'] = 0
            dic['damage'] = []
            dic['emoji'] = emoji[i]
            del dic['first_name']
            del dic['last_name']
        return users_list
        
    def to_json(self, file_name, users_dict):
        json_users_dict = json.dumps(users_dict)
        with open(self.DATA_FOLDER_FILE_PATH + file_name, mode='w') as outfile:
#             json.dump(json_users_dict, outfile)
            outfile.write(json_users_dict)
    
    def read_json(self, file_name):
        with open(self.DATA_FOLDER_FILE_PATH + file_name, mode='r') as openfile:
            json_object = json.load(openfile)
        # print(json_object)
        return json_object
    


if __name__ == '__main__':
    # DATA_FOLDER_FILE_PATH = './data/'
    group_id = 226106896
    group_token = '''vk1.a.HNKbzJjt987sI6qa1TwXBlpYpxb4RO-c-y5KF9nnDLsTkc1Mouu7X_DPGWJVmsweEJkIXUFcQR
    oTOf8YdhIn6sFtzK8h4MIFecAiwF_fSovgl7Bq1O5bJFVljxp-hf6qthNrX3GvaMi7JU4cr_Ac_LkKgf3q4y5OMbg5XOalt7F
    Og9Me5qepbqfvjoQTlxvI8Mjol24sn_ixEO5X6yPz1g'''
    user_ids = [
        [322120408, '🧠'], #Андрей
        [280864946, '👜'], #Артём Х
        [567572779, '👶'], #Егор К
        [434340601, '🌚'], #Кирилл К
        [160348331, '😍'], #Артур
        [249200120, '🤡'], #Я
        [571456262, '🍌'], #Влад
        [452036630, '😈'], #Артём Б
        [479688907, '🤬'], #Алексей
        [546754921, '🤑'], #Фёдор
        [704189756, '⛄️'], #Салман
        [650573187, '🥐'], #Богдан
        [284569404, '🍆'], #Владимир
        [360581583, '🥝'], #Андрей
        [388908512, '🍭'], #Егор
        [264360502, '🍻'], #Артём Г
        [865092166, '👨‍👧‍👦'], #
    ]
    user_ids = [
        [337896324, '🍌'], #Вадим
        [356360907, '👠'], #Александр
        [249200120, '🦾'], #Я
        [601925367, '🍊'], #Руслан
        [219330689, '👨‍🍳'], #Слава
        [241247237, '💸'], #Родион
        [296179282, '✝️'], #Максим
        [322120408, '🧠'], #Андрей
        [482464167, '♿️'], #Данил
        [241650811, '😈'], #Микола
        [517196287, '🚵'], #Влад '🇧🇾'
    ]
    user_ids = [
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
        # [865092166, '🚑']
    ]

    users = VKUsers(group_id, group_token)
    users_list = users.get_users_list_1(user_ids)
    # print(users_list)
    users.to_json('users.json', users_list)
    # users_list = users.get_users_list([160348331, 571456262], ['domain'])