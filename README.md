# Гайд по танковому боту для ВК
### Установка приложения
> **Warning**<br>
Предполагается, что пользователь выдал все необходимые права боту в облачной версии приложения
> 
Клонирование репозитория
```cmd
git clone https://github.com/Kirill-Erofeev/vk_bot.git
```
Переход в корневую папку проекта
```cmd
cd ./vk_bot
```
Создание виртуального окружения
```cmd
python -m venv venv
```
Активация виртуального окружения
```cmd
venv\Scripts\activate.bat
```
Установка зависимостей
```cmd
pip install -r requirements.txt
```
Активация программы
```cmd
python ./tank_bot/__main__.py
```
### Обзор файловой структуры
* В файле `__main__.py` содержится точка входа в программу
* В файле `config.py` содержfncz глобальные переменные
* В файле `demotivator.py` содержится класс, позволяющий создавать демотиваторы
* В файле `functions.py` содержатся функции, необходимые для обработки информации
* В файле `tank.py` содержится класс, отвечающий за танковые бои
### Интерфейс для взаимодействия с ботом
![Без имени 667](https://github.com/user-attachments/assets/1a3fc005-1f7e-42c9-b4c2-417345978fab)
### Пример "статиста дня"
![Статист дня](https://github.com/user-attachments/assets/239d49aa-fcc0-4d8a-bc07-56a3a790aa52)
### Пример "банки дня"
![Банка дня](https://github.com/user-attachments/assets/057fd809-6fc8-436d-a448-2e0ed6657199)
### Пример "инсайдерской инфы по Т8"
![Т8](https://github.com/user-attachments/assets/75f15988-930f-4f33-9dc5-cc71f7b7056d)
### Пример "быстрого боя"
![Быстрый бой](https://github.com/user-attachments/assets/21055858-dd1c-4238-9893-ea49c024ce77)
![Быстрый бой](https://github.com/user-attachments/assets/87cb947a-11c4-46db-a81a-f2a31decf93b)
### Пример "долгого" боя
![Долгий бой](https://github.com/user-attachments/assets/b3acb387-6549-4f35-bd2a-ac1751eba5f8)
![Долгий бой](https://github.com/user-attachments/assets/e2501f68-3426-4e40-8260-0eb1e4c88886)
### Пример "демотиватора"
![demotivator](https://github.com/user-attachments/assets/00267ec8-e39d-4907-8c3c-adb4f1c5f13c)
### Пример "ядра свёртки"
![effect](https://github.com/user-attachments/assets/16c1b5dc-fea6-43bc-b9f0-3b42f233c264)
### Пример "лидерборда"
![Лидерборд](https://github.com/user-attachments/assets/4c72595e-9c87-40dc-b96e-b140e3b510e1)
### Пример "помощи"
![Помощь](https://github.com/user-attachments/assets/1b9601c8-3767-4c55-995a-18f2f23d0dd6)