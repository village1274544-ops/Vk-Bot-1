import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import os
import time

print("🔄 Запуск бота для майнкрафт сервера...")

# Ваши данные
GROUP_ID = os.environ.get('GROUP_ID', '234268176')
TOKEN = os.environ.get('TOKEN', 'vk1.a.PG52Lss5mcUsbIg4bhSpSx4Ce-ibEsD2MRVW_LBJuO4GgC6laRrQANNexgsrDB_GLOFJK33WgxtfzInlb5SpbJ6dv9eJf2xj6WejGTOPbtByjV-8HEX5Awg0E5SzJmNC3oAubSjJ0uIs9_4Cg6Cq-t0NHzSzAUwRllr5XHak8fOJ8XOshYBFJHhJltoL8h-yCmx-z7MW2n9daQmK-SHj5w')

print(f"🔧 ID группы: {GROUP_ID}")

try:
    vk_session = vk_api.VkApi(token=TOKEN)
    longpoll = VkBotLongPoll(vk_session, GROUP_ID)
    vk = vk_session.get_api()
    print("✅ Успешная авторизация в ВКонтакте!")
except Exception as e:
    print(f"❌ Ошибка авторизации: {e}")
    exit(1)

def send_message(user_id, message, keyboard=None):
    try:
        vk.messages.send(
            user_id=user_id,
            message=message,
            random_id=random.randint(0, 2**64),
            keyboard=keyboard
        )
        return True
    except Exception as e:
        print(f"❌ Ошибка отправки: {e}")
        return False

# Клавиатура
keyboard = {
    "one_time": False,
    "buttons": [
        [{"action": {"type": "text", "label": "📢 Оповещения"}, "color": "positive"}],
        [{"action": {"type": "text", "label": "🔄 График вайпов"}, "color": "primary"}],
        [{"action": {"type": "text", "label": "📖 Информация"}, "color": "primary"}],
        [{"action": {"type": "text", "label": "🌐 IP серверов"}, "color": "secondary"}]
    ]
}
keyboard_json = str(keyboard).replace("'", '"')

print("🎉 Бот работает! Ожидаем сообщения...")

while True:
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                msg = event.object.message['text'].lower()
                user_id = event.object.message['from_id']
                
                if msg in ['начать', 'привет', 'start']:
                    welcome_text = "🎮 Добро пожаловать!\n\nЗдравствуйте! Используйте кнопки ниже для получения информации:"
                    send_message(user_id, welcome_text, keyboard_json)
                elif msg in ['оповещения', '📢 оповещения']:
                    send_message(user_id, "📢 Оповещения:\n• Новый ивент 'Зимняя сказка'\n• Исправлены баги PvP\n• Добавлены квесты", keyboard_json)
                elif msg in ['график вайпов', '🔄 график вайпов', 'вайп']:
                    send_message(user_id, "🔄 График вайпов:\n• Статистический: 1 декабря\n• Полный вайп: 1 января", keyboard_json)
                elif msg in ['информация', '📖 информация']:
                    send_message(user_id, "📖 Информация:\n• Версия: 1.20.1\n• Онлайн: 45/100\n• Режим: Выживание", keyboard_json)
                elif msg in ['ip серверов', '🌐 ip серверов', 'ip']:
                    send_message(user_id, "🌐 IP серверов:\n• Основной: mc.rustcraft.ru\n• Резервный: backup.rustcraft.ru", keyboard_json)
                else:
                    send_message(user_id, "Используйте кнопки для навигации 👆", keyboard_json)
    
    except Exception as e:
        print(f"⚠️ Ошибка: {e}")
        time.sleep(10)
