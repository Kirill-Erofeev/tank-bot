# from collections import Counter

# import torch
# import torch.nn as nn
# import torch.nn.functional as F
# import numpy as np

# TRAINS_FOLDER_FILE_PATH = 'data/'
# MODELS_FOLDER_FILE_PATH = 'data/'
# TRAIN_TEXT_FILE_DEFAULT_NAME = 'poetic_data'

# SEQ_LEN = 256
# BATCH_SIZE = 16


# def text_to_seq(text_sample):
#     char_counts = Counter(text_sample)
#     char_counts = sorted(char_counts.items(), key=lambda x: x[1], reverse=True)

#     sorted_chars = [char for char, _ in char_counts]
#     # Nprint(sorted_chars)
#     char_to_idx = {char: index for index, char in enumerate(sorted_chars)}
#     idx_to_char = {v: k for k, v in char_to_idx.items()}
#     sequence = np.array([char_to_idx[char] for char in text_sample])

#     return sequence, char_to_idx, idx_to_char


# def get_batch(sequence):
#     trains = []
#     targets = []
#     for _ in range(BATCH_SIZE):
#         batch_start = np.random.randint(0, len(sequence) - SEQ_LEN)
#         chunk = sequence[batch_start: batch_start + SEQ_LEN]
#         train = torch.LongTensor(chunk[:-1]).view(-1, 1)
#         target = torch.LongTensor(chunk[1:]).view(-1, 1)
#         trains.append(train)
#         targets.append(target)
#     return torch.stack(trains, dim=0), torch.stack(targets, dim=0)

# def evaluate(model, char_to_idx, idx_to_char, start_text=' ', prediction_len=200, temp=0.3):
#     hidden = model.init_hidden()
#     idx_input = [char_to_idx[char] for char in start_text]
#     train = torch.LongTensor(idx_input).view(-1, 1, 1).to(device)
#     predicted_text = start_text

#     _, hidden = model(train, hidden)

#     inp = train[-1].view(-1, 1, 1)

#     for i in range(prediction_len):
#         output, hidden = model(inp.to(device), hidden)
#         output_logits = output.cpu().data.view(-1)
#         p_next = F.softmax(output_logits / temp, dim=-1).detach().cpu().data.numpy()
#         top_index = np.random.choice(len(char_to_idx), p=p_next)
#         inp = torch.LongTensor([top_index]).view(-1, 1, 1).to(device)
#         predicted_char = idx_to_char[top_index]
#         predicted_text += predicted_char

#     return predicted_text


# class TextRNN(nn.Module):

#     def __init__(self, input_size, hidden_size, embedding_size, n_layers=1):
#         super(TextRNN, self).__init__()

#         self.input_size = input_size
#         self.hidden_size = hidden_size
#         self.embedding_size = embedding_size
#         self.n_layers = n_layers

#         self.encoder = nn.Embedding(self.input_size, self.embedding_size)
#         self.lstm = nn.LSTM(self.embedding_size, self.hidden_size, self.n_layers)
#         self.dropout = nn.Dropout(0.2)
#         self.fc = nn.Linear(self.hidden_size, self.input_size)

#     def forward(self, x, hidden):
#         x = self.encoder(x).squeeze(2)
#         out, (ht1, ct1) = self.lstm(x, hidden)
#         out = self.dropout(out)
#         x = self.fc(out)
#         return x, (ht1, ct1)

#     def init_hidden(self, batch_size=1):
#         return (torch.zeros(self.n_layers, batch_size, self.hidden_size, requires_grad=True).to(device),
#                 torch.zeros(self.n_layers, batch_size, self.hidden_size, requires_grad=True).to(device))


# device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

# def module_name(epochs):
#     return MODELS_FOLDER_FILE_PATH + train_name + '_epoch_' + str(epochs) + '.pth'

# # def learn(epochs):
# #     model = TextRNN(input_size=len(idx_to_char), hidden_size=128, embedding_size=128, n_layers=2)
# #     model.to(device)

# #     criterion = nn.CrossEntropyLoss()
# #     optimizer = torch.optim.Adam(model.parameters(), lr=1e-2, amsgrad=True)
# #     scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
# #         optimizer,
# #         patience=5,
# #         verbose=True,
# #         factor=0.5
# #     )

# #     n_epochs = epochs  # 50000
# #     loss_avg = []

# #     for epoch in range(n_epochs):
# #         model.train()
# #         train, target = get_batch(sequence)
# #         train = train.permute(1, 0, 2).to(device)
# #         target = target.permute(1, 0, 2).to(device)
# #         hidden = model.init_hidden(BATCH_SIZE)

# #         output, hidden = model(train, hidden)
# #         loss = criterion(output.permute(1, 2, 0), target.squeeze(-1).permute(1, 0))

# #         loss.backward()
# #         optimizer.step()
# #         optimizer.zero_grad()

# #         loss_avg.append(loss.item())
# #         if len(loss_avg) >= 50:
# #             mean_loss = np.mean(loss_avg)
# #             print(f'Loss: {mean_loss} Epoch: {epoch}')
# #             scheduler.step(mean_loss)
# #             loss_avg = []
# #             model.eval()
# #             predicted_text = evaluate(model, char_to_idx, idx_to_char)
# #             # print(predicted_text)

# #     torch.save(model,  module_name(epochs))

# # quer = input('Учить нейросеть? (Y/N): ')

# train_name = TRAIN_TEXT_FILE_DEFAULT_NAME

# with open('data/poetic_data.txt', encoding='utf-8') as text_file:
#     text_sample = text_file.readlines()
# text_sample = ' '.join(text_sample)
# sequence, char_to_idx, idx_to_char = text_to_seq(text_sample)

# # if (quer == 'Y'):
# #     epochs = int(input('Введите колличество эпох обучения (>1000): '))
# #     learn(epochs)
# model = torch.load(module_name(50000))
# print(evaluate(
#     model,
#     char_to_idx,
#     idx_to_char,
#     temp=1,
#     prediction_len=90,
#     start_text=' '
#     )
# )
# # elif (quer == 'N'):
# #     epochs = int(input('Введите эпоху входной модели: '))
# #     model = torch.load(module_name(epochs))
# #     model.eval()
# #     while True:
# #         count = int(input('Введите колличество символов текста: '))
# #         N = int(input('Введите колличество генераций текста: '))
# #         for i in range(N):
# #             print('-----------------------------')
# #             print(evaluate(
# #                 model,
# #                 char_to_idx,
# #                 idx_to_char,
# #                 temp=1,
# #                 prediction_len=count,
# #                 start_text=' '
# #                )
# #             )
# #             print('-----------------------------\n\n')
# #         qrep = input('Еще разок? (Y/N): ')
# #         if (qrep != 'Y'): break
# # else:
# #     print('Ошибка ввода.')

# with open('text.txt') as file:
#     a = file.read()
# import json

# DATA_FOLDER_FILE_PATH = './'
# def read_file(file_name):
#     try:
#         with open(DATA_FOLDER_FILE_PATH + file_name, mode='r') as openfile:
#             lst = json.load(openfile)
#     except FileNotFoundError:
#         lst = []
#     return lst

# print(read_file('photos.json'))

# T110E4 3206 + 2000 = 5206 1.06
# T110E3 2851 + 2067 = 4918 1.12      
# T110E5 2878 + 2576 = 5454 1.01      
# Grille 15 3497 + 1802 = 5299 1.04   
# Jz.Pz. E 100 3065 + 2279 = 5344 1.03
# VK 72.01 K 2673 + 2744 = 5417 1.02  
# Maus 2733 + 3192 = 5925 0.93        
# E 100 2448 + 2915 = 5363 1.03       
# E 50 M 3366 + 2014 = 5380 1.02      
# Leopard 1 3949 + 1908 = 5857 0.94   
# Об. 268 3073 + 1908 = 4981 1.1      
# Об. 263 4000 + 1961 = 5961 0.92     
# ИС-7 2584 + 2703 = 5287 1.04        
# Об. 140 3814 + 1908 = 5722 0.96     
# Т-62А 3455 + 2014 = 5469 1.01       
# Т-100 ЛТ 3298 + 1855 = 5153 1.07    
# FV215b 3274 + 2576 = 5850 0.94
# STB-1 3511 + 1961 = 5472 1.01
# Type 71 2625 + 2703 = 5328 1.03
# WZ-113G FT 3040 + 2240 = 5280 1.04
# WZ-113 3274 + 2438 = 5712 0.96
# WZ-121 3438 + 1908 = 5346 1.03
# CS-63 3366 + 1908 = 5274 1.04
# ЛВ-1300 Уран 2621 + 2544 = 5165 1.06
# Strv K 3465 + 2576 = 6041 0.91
# AMX M4 mle. 54 2695 + 2800 = 5495 1.0
# AMX 30 B 3565 + 1908 = 5473 1.0
# 121B 3465 + 1908 = 5373 1.02
# FV217 Badger 3855 + 2240 = 6095 0.9
# Chieftain Mk. 6 3166 + 2491 = 5657 0.97
# Super Conqueror 2938 + 2597 = 5535 0.99
# Об. 260 3097 + 2544 = 5641 0.98
# Об. 777 Ⅱ 3127 + 2544 = 5671 0.97
# Об. 907 3510 + 1908 = 5418 1.02
# Т-22 ср. 3400 + 1961 = 5361 1.03
# Kpz 50 t 3678 + 1908 = 5586 0.98
# XM66F 3565 + 2014 = 5579 0.99
# T95E6 3315 + 2438 = 5753 0.96
# Sheridan Ракетный 2494 + 1908 = 4402 1.25
# VK 90.01 (P) 2621 + 2597 = 5218 1.05
# Concept 1B 3008 + 2491 = 5499 1.0
# M48 Patton 3560 + 1961 = 5521 1.0
# M60 3512 + 2014 = 5526 1.0
# WZ-111 5A 2956 + 2438 = 5394 1.02
# Объект 268/4 2989 + 1961 = 4950 1.11
# Foch 155 3125 + 1961 = 5086 1.08
# Vickers Light 3291 + 1802 = 5093 1.08
# FV4202 3465 + 1908 = 5373 1.02
# FV215b 183 3013 + 1908 = 4921 1.12
# Ho-Ri 3327 + 2014 = 5341 1.03
# WZ-132-1 3248 + 1855 = 5103 1.08
# 60TP Lewandowskiego 2564 + 2756 = 5320 1.03
# Vz. 55 2638 + 2544 = 5182 1.06
TANKS = [
    {'id': 'T110E4', 'class': 'ПТ', 'hp': 2000, 'damage': 630, 'reload': 11.79, 'breakout_prob': 0.74, 'fire_prob': 0.20},
    {'id': 'T110E3', 'class': 'ПТ', 'hp': 2067, 'damage': 680, 'reload': 14.31, 'breakout_prob': 0.68, 'fire_prob': 0.20},
    {'id': 'T110E5', 'class': 'ТТ', 'hp': 2576, 'damage': 400, 'reload': 8.34, 'breakout_prob': 0.79, 'fire_prob': 0.20},
    {'id': 'Grille 15', 'class': 'ПТ', 'hp': 1802, 'damage': 580, 'reload': 9.95, 'breakout_prob': 0.76, 'fire_prob': 0.15}, #0.15
    {'id': 'Jz.Pz. E 100', 'class': 'ПТ', 'hp': 2279, 'damage': 800, 'reload': 15.66, 'breakout_prob': 0.77, 'fire_prob': 0.15},
    # {'id': 'Jz.Pz. E 100', 'class': 'ПТ', 'hp': 2279, 'damage': 800, 'reload': 0.50, 'breakout_prob': 1, 'fire_prob': 0.15},
    {'id': 'VK 72.01 K', 'class': 'ТТ', 'hp': 2744, 'damage': 600, 'reload': 13.47, 'breakout_prob': 0.78, 'fire_prob': 0.12},
    {'id': 'Maus', 'class': 'ТТ', 'hp': 3192, 'damage': 460, 'reload': 10.10, 'breakout_prob': 0.87, 'fire_prob': 0.12},
    {'id': 'E 100', 'class': 'ТТ', 'hp': 2915, 'damage': 680, 'reload': 16.67, 'breakout_prob': 0.77, 'fire_prob': 0.15}, #0.15
    {'id': 'E 50 M', 'class': 'СТ', 'hp': 2014, 'damage': 340, 'reload': 6.06, 'breakout_prob': 0.78, 'fire_prob': 0.12}, #0.12
    {'id': 'Leopard 1', 'class': 'СТ', 'hp': 1908, 'damage': 360, 'reload': 5.47, 'breakout_prob': 0.86, 'fire_prob': 0.10},
    {'id': 'Об. 268', 'class': 'ПТ', 'hp': 1908, 'damage': 690, 'reload': 13.47, 'breakout_prob': 0.70, 'fire_prob': 0.12},
    {'id': 'Об. 263', 'class': 'ПТ', 'hp': 1961, 'damage': 460, 'reload': 6.90, 'breakout_prob': 0.88, 'fire_prob': 0.15},
    {'id': 'ИС-7', 'class': 'ТТ', 'hp': 2703, 'damage': 460, 'reload': 10.68, 'breakout_prob': 0.76, 'fire_prob': 0.15},
    {'id': 'Об. 140', 'class': 'СТ', 'hp': 1908, 'damage': 300, 'reload': 4.72, 'breakout_prob': 0.84, 'fire_prob': 0.12},
    {'id': 'Т-62А', 'class': 'СТ', 'hp': 2014, 'damage': 330, 'reload': 5.73, 'breakout_prob': 0.79, 'fire_prob': 0.10},
    {'id': 'Т-100 ЛТ', 'class': 'ЛТ', 'hp': 1855, 'damage': 310, 'reload': 5.64, 'breakout_prob': 0.73, 'fire_prob': 0.10},
    {'id': 'FV215b', 'class': 'ТТ', 'hp': 2576, 'damage': 400, 'reload': 7.33, 'breakout_prob': 0.86, 'fire_prob': 0.20},
    {'id': 'STB-1', 'class': 'СТ', 'hp': 1961, 'damage': 330, 'reload': 5.64, 'breakout_prob': 0.79, 'fire_prob': 0.12},
    {'id': 'Type 71', 'class': 'ТТ', 'hp': 2703, 'damage': 420, 'reload': 9.60, 'breakout_prob': 0.77, 'fire_prob': 0.12},
    {'id': 'WZ-113G FT', 'class': 'ПТ', 'hp': 2240, 'damage': 640, 'reload': 12.63, 'breakout_prob': 0.76, 'fire_prob': 0.12},
    {'id': 'WZ-113', 'class': 'ТТ', 'hp': 2438, 'damage': 400, 'reload': 7.33, 'breakout_prob': 0.84, 'fire_prob': 0.12},
    {'id': 'WZ-121', 'class': 'СТ', 'hp': 1908, 'damage': 420, 'reload': 7.33, 'breakout_prob': 0.77, 'fire_prob': 0.12},
    {'id': 'CS-63', 'class': 'СТ', 'hp': 1908, 'damage': 340, 'reload': 6.06, 'breakout_prob': 0.76, 'fire_prob': 0.10},
    {'id': 'ЛВ-1300 Уран', 'class': 'ТТ', 'hp': 2544, 'damage': 460, 'reload': 10.53, 'breakout_prob': 0.74, 'fire_prob': 0.15},
    {'id': 'Strv K', 'class': 'ТТ', 'hp': 2576, 'damage': 350, 'reload': 6.06, 'breakout_prob': 0.89, 'fire_prob': 0.15},
    {'id': 'AMX M4 mle. 54', 'class': 'ТТ', 'hp': 2800, 'damage': 450, 'reload': 10.02, 'breakout_prob': 0.80, 'fire_prob': 0.20},
    {'id': 'AMX 30 B', 'class': 'СТ', 'hp': 1908, 'damage': 350, 'reload': 5.89, 'breakout_prob': 0.80, 'fire_prob': 0.10},
    {'id': '121B', 'class': 'СТ', 'hp': 1908, 'damage': 350, 'reload': 6.06, 'breakout_prob': 0.78, 'fire_prob': 0.12}, #?
    {'id': 'FV217 Badger', 'class': 'ПТ', 'hp': 2240, 'damage': 460, 'reload': 7.16, 'breakout_prob': 0.90, 'fire_prob': 0.20},
    {'id': 'Chieftain Mk. 6', 'class': 'ТТ', 'hp': 2491, 'damage': 400, 'reload': 7.58, 'breakout_prob': 0.83, 'fire_prob': 0.10},
    {'id': 'Super Conqueror', 'class': 'ТТ', 'hp': 2597, 'damage': 400, 'reload': 8.17, 'breakout_prob': 0.81, 'fire_prob': 0.20},
    {'id': 'Об. 260', 'class': 'ТТ', 'hp': 2544, 'damage': 400, 'reload': 7.75, 'breakout_prob': 0.82, 'fire_prob': 0.15},
    {'id': 'Об. 777 Ⅱ', 'class': 'ТТ', 'hp': 2544, 'damage': 430, 'reload': 8.25, 'breakout_prob': 0.83, 'fire_prob': 0.25},
    {'id': 'Об. 907', 'class': 'СТ', 'hp': 1908, 'damage': 320, 'reload': 5.47, 'breakout_prob': 0.78, 'fire_prob': 0.12}, #?
    {'id': 'Т-22 ср.', 'class': 'СТ', 'hp': 1961, 'damage': 310, 'reload': 5.47, 'breakout_prob': 0.77, 'fire_prob': 0.10},
    {'id': 'Kpz 50 t', 'class': 'СТ', 'hp': 1908, 'damage': 320, 'reload': 5.22, 'breakout_prob': 0.82, 'fire_prob': 0.12},
    {'id': 'XM66F', 'class': 'ПТ', 'hp': 2014, 'damage': 410, 'reload': 6.90, 'breakout_prob': 0.81, 'fire_prob': 0.12}, #?
    {'id': 'T95E6', 'class': 'ТТ', 'hp': 2438, 'damage': 400, 'reload': 7.24, 'breakout_prob': 0.84, 'fire_prob': 0.15},
    {'id': 'Sheridan Ракетный', 'class': 'ЛТ', 'hp': 1908, 'damage': 560, 'reload': 13.47, 'breakout_prob': 0.55, 'fire_prob': 0.12},
    {'id': 'VK 90.01 (P)', 'class': 'ТТ', 'hp': 2597, 'damage': 460, 'reload': 10.53, 'breakout_prob': 0.75, 'fire_prob': 0.10},
    {'id': 'Concept 1B', 'class': 'ТТ', 'hp': 2491, 'damage': 380, 'reload': 7.58, 'breakout_prob': 0.80, 'fire_prob': 0.12}, #?
    {'id': 'M48 Patton', 'class': 'СТ', 'hp': 1961, 'damage': 340, 'reload': 5.73, 'breakout_prob': 0.80, 'fire_prob': 0.12},
    {'id': 'M60', 'class': 'СТ', 'hp': 2014, 'damage': 350, 'reload': 5.98, 'breakout_prob': 0.80, 'fire_prob': 0.10},
    {'id': 'WZ-111 5A', 'class': 'ТТ', 'hp': 2438, 'damage': 440, 'reload': 8.93, 'breakout_prob': 0.78, 'fire_prob': 0.12},
    {'id': 'Объект 268/4', 'class': 'ПТ', 'hp': 1961, 'damage': 650, 'reload': 13.05, 'breakout_prob': 0.69, 'fire_prob': 0.12},
    {'id': 'Foch 155', 'class': 'ПТ', 'hp': 1961, 'damage': 600, 'reload': 11.52, 'breakout_prob': 0.72, 'fire_prob': 0.15},
    {'id': 'Vickers Light', 'class': 'ЛТ', 'hp': 1802, 'damage': 300, 'reload': 5.47, 'breakout_prob': 0.72, 'fire_prob': 0.20},
    {'id': 'FV4202', 'class': 'СТ', 'hp': 1908, 'damage': 350, 'reload': 6.06, 'breakout_prob': 0.78, 'fire_prob': 0.20},
    {'id': 'FV215b 183', 'class': 'ПТ', 'hp': 1908, 'damage': 930, 'reload': 18.52, 'breakout_prob': 0.68, 'fire_prob': 0.20},
    {'id': 'Ho-Ri', 'class': 'ПТ', 'hp': 2014, 'damage': 560, 'reload': 10.10, 'breakout_prob': 0.77, 'fire_prob': 0.15},
    {'id': 'WZ-132-1', 'class': 'ЛТ', 'hp': 1855, 'damage': 360, 'reload': 6.65, 'breakout_prob': 0.72, 'fire_prob': 0.12},
    {'id': '60TP Lewandowskiego', 'class': 'ТТ', 'hp': 2756, 'damage': 630, 'reload': 14.74, 'breakout_prob': 0.77, 'fire_prob': 0.15},
    {'id': 'Vz. 55', 'class': 'ТТ', 'hp': 2544, 'damage': 470, 'reload': 10.69, 'breakout_prob': 0.74, 'fire_prob': 0.10},
]

lt = []
st = []
tt = []
pt = []
e = []
# for dic in TANKS:
#     if dic['class'] == 'ЛТ':
#         # lt.append(round(dic['damage'] * 60 / dic['reload']))
#         lt.append(dic['hp'])
#     elif dic['class'] == 'СТ':
#         # st.append(round(dic['damage'] * 60 / dic['reload']))
#         st.append(dic['hp'])
#     elif dic['class'] == 'ТТ':
#         # tt.append(round(dic['damage'] * 60 / dic['reload']))
#         tt.append(dic['hp'])
#     elif dic['class'] == 'ПТ':
#         # pt.append(round(dic['damage'] * 60 / dic['reload']))
#         pt.append(dic['hp'])
#     f = round(dic['damage'] * 60 / dic['reload'])
#     s = round(dic['damage'] * 60 / dic['reload']) + dic['hp']
#     print(dic['id'], f, '+', dic['hp'], '=', s, round(5500 / s, 2))
#     e.append(s)

# print(round(sum(lt) / len(lt)))
# print(round(sum(st) / len(st)))
# print(round(sum(tt) / len(tt)))
# print(round(sum(pt) / len(pt)))
# print(round(sum(e) / len(e)))
# user_info = [[1, 2]]
# print(list(map(lambda x: x[0], user_info)))
print(k)