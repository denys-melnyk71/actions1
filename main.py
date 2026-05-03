import pyttsx3
import tts.sapi
import threading
import speech_recognition as s

engine = pyttsx3.init()
voice = tts.sapi.Sapi()
voice.set_voice('Anatol')
CURRENT_VOICE = 'Anatol'
sr = s.Recognizer()

VOICE_INPUT = False
OUTPUT_FORMAT = "текст"

def listen():
    global audio
    with s.Microphone() as source:
        audio = sr.listen(source)

def msg_in():
    global VOICE_INPUT
    if VOICE_INPUT:
        # слухання
        t = threading.Thread(target=listen)
        t.start()
        input('@ *слухає* (Enter щоб зупинити)')
        t.join()
        VOICE_INPUT = False
        # STT
        try:
            msg = sr.recognize_google(audio, language="uk-UA")
            return msg
        except sr.UnknownValueError:
            return "Я не зрозумів. Можеш повторити?"
    else:
        return input("> ")
    

def msg_out(msg):
    global OUTPUT_FORMAT
    if OUTPUT_FORMAT == "текст":
        print('@ ' + msg)
    elif OUTPUT_FORMAT == "голос":
        print('@ *говорить*')
        voice.say(msg)
    elif OUTPUT_FORMAT == "змішаний":
        print('@ ' + msg)
        voice.say(msg)
    else:
        print("ПОМИЛКА: невідомий формат виводу")


def arg_check(user_argl, argm):
    # argm - матриця, де кожен вкладений список 
    # це список доступних аргументів на відповідну позицію
    argc = len(argm)
    if len(user_argl) < argc:
        print('Недостатньо аргументів. Синтаксис команд можна переглянути ввівши "/команди"')
        return False
    i = 0
    for i in range(argc):
        if user_argl[i] not in argm[i]:
            print('ПОМИЛКА: неочікуваний аргумент "' + str(user_argl[i]) + '"')
            print('Очікується один з ' + str(argm[i]))
            return False
        i += 1
    return True


def command(msg):
    global VOICE_INPUT, OUTPUT_FORMAT, CURRENT_VOICE

    # виділяємо з повідомлення назву команди, список та кількість аргументів
    temp = msg.split()
    cmd = temp[0]
    arg_count = len(temp) - 1
    arg_list = []
    if arg_count > 0:
        arg_list = temp[1:]

    if cmd == "команди":
        print("============================ Список команд ============================")
        print("/команди                       - подивитись список команд")
        print("/вихід                         - завершити виконання програми")
        print("/г                             - записати голосове повідомлення")
        print("/формат <знак> <назва формату> - змінити формат виводу")
        print("/формати                       - подивитись список форматів виводу")
        print("/голос <знак> <назва голосу>   - змінити голос")
        print("/голоси                        - подивитись список голосів")
        print("/гучність <знак> <значення>    - змінити гучність")
        print("/швидкість <знак> <значення>   - змінити швидкість")
        print("==================== Можливі значення поля <знак> ====================")
        print("/<команда> + <значення> - збільшити поточне значення на задане")
        print("/<команда> - <значення> - зменшити поточне значення на задане")
        print("/<команда> = <значення> - замінити поточне значення на задане")
        print("/<команда> ?            - подивитись поточне значення")
        print("=======================================================================")
    elif cmd == "г":
        VOICE_INPUT = True
    elif cmd == "формат":
        if arg_count == 0:
            print('Недостатньо аргументів. Синтаксис команд можна переглянути ввівши "/команди"')
            return False
        elif arg_count == 1:
            if not arg_check(arg_list, [['?']]):
                return
            print('Поточний формат виводу - ' + OUTPUT_FORMAT)
        else:
            if not arg_check(arg_list, [['='], ['текст', 'голос', 'змішаний']]):
                return
            OUTPUT_FORMAT = arg_list[1]
            print('Формат виводу змінено на ' + OUTPUT_FORMAT)
    elif cmd == "формати":
        print('================== Список форматів ==================')
        print('текст    - вивід в консоль')
        print('голос    - вивід на динамікіи/навушники')
        print('змішаний - вивід в консоль та на динамікіи/навушники')
        print('=====================================================')
    elif cmd == "голос":
        if arg_count == 0:
            print('Недостатньо аргументів. Синтаксис команд можна переглянути ввівши "/команди"')
            return False
        elif arg_count == 1:
            if arg_check(arg_list, [['?']]):
                print('Поточний голос - ' + CURRENT_VOICE)
        else:
            # формуємо список голосів
            v_names = []
            voices = engine.getProperty('voices')
            for v in voices:
                v_names.append(v.name)
            # перевірка аргументів 
            if arg_check(arg_list, [['='], v_names]):
                # зміна голосу
                CURRENT_VOICE = arg_list[1]
                voice.set_voice(CURRENT_VOICE)
                print('Поточний голос - ' + CURRENT_VOICE)
    elif cmd == "голоси":
        voices = engine.getProperty('voices')
        for v in voices:
            print(v.name)
    elif cmd == "гучність":
        volume = voice.voice.Volume # фіксуємо поточну гучність
        if arg_count == 0:
            print('Недостатньо аргументів. Синтаксис команд можна переглянути ввівши "/команди"')
            return False
        elif arg_count == 1:
            if arg_check(arg_list, [['?']]):
                print("Поточна гучність - " + str(voice.voice.Volume))
        else:
            if arg_check(arg_list, [['+', '-', '=']]):
                try:
                    value = int(arg_list[1])
                    if arg_list[0] == '+':
                        voice.voice.Volume = min(voice.voice.Volume + value, 100)
                        print("Гучність змінена " + str(volume) + '->' + str(voice.voice.Volume))
                    elif arg_list[0] == '-':
                        voice.voice.Volume = max(voice.voice.Volume - value, 0)
                        print("Гучність змінена " + str(volume) + '->' + str(voice.voice.Volume))
                    else: # arg_list[0] == '='
                        voice.voice.Volume = min(max(value, 0), 100)
                        print("Гучність змінена " + str(volume) + '->' + str(voice.voice.Volume))
                except ValueError:
                    print("ПОМИЛКА: очікується ціле число")
                    return
    elif cmd == "швидкість":
        rate = voice.voice.Rate # фіксуємо поточну швидкість
        if arg_count == 0:
            print('Недостатньо аргументів. Синтаксис команд можна переглянути ввівши "/команди"')
            return False
        elif arg_count == 1:
            if arg_check(arg_list, [['?']]):
                print("Поточна швидкість - " + str(voice.voice.Rate))
        else:
            if arg_check(arg_list, [['+', '-', '=']]):
                try:
                    value = int(arg_list[1])
                    if arg_list[0] == '+':
                        voice.voice.Rate = min(voice.voice.Rate + value, 10)
                        print("Швидкість змінена " + str(rate) + '->' + str(voice.voice.Rate))
                    elif arg_list[0] == '-':
                        voice.voice.Rate = max(voice.voice.Rate - value, -10)
                        print("Швидкість змінена " + str(rate) + '->' + str(voice.voice.Rate))
                    else: # arg_list[0] == '='
                        voice.voice.Rate = min(max(value, -10), 10)
                        print("Швидкість змінена " + str(rate) + '->' + str(voice.voice.Rate))
                except ValueError:
                    print("ПОМИЛКА: очікується ціле число")
                    return
    else:
        print("ПОМИЛКА: невідома команда")


if __name__ == "__main__":
    print('========= Введіть "/команди" щоб подивитись список команд =========')
    while True:
        msg = msg_in()
        if msg == "/вихід":
            break
        elif len(msg) > 0 and msg[0] == "/":
            command(msg[1:])
        else:
            msg_out(msg)
