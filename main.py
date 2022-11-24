import telebot

import sys
import os
import datetime
import re

bot = telebot.TeleBot('5971543255:AAGL-SSJzozQuZdzlOHUI8-yOHlRc2iKGIY');
hello = "Я могу вычислить наибольший общий делитель двух чисел и сыграть в крестики-нолики. " \
        "Чтобы посчитать, напиши \'НОД\', а чтобы сыграть отправь \'игра\'"

state = 0
match_number = re.compile(r'^[1-9][0-9]*\.?[0-9]*')
match_only_number = re.compile(r'^[1-9]')
cashe = {}
arg_a = 0
arg_b = 0

def show_board(message):
    res = ""

    for i in range(0, 3):
        for j in range(0, 3):
            if game[3 * i + j] == 0:
                res += "- "
            elif first:
                if game[3 * i + j] == 1:
                    res += "X "
                else:
                    res += "O "
            else:
                if game[3 * i + j] == 1:
                    res += "O "
                else:
                    res += "X "
        res += "\n"

    bot.send_message(message.from_user.id, res)

def win_check():
    for i in range(0, 3):
        if game[i * 3] == game[i * 3 + 1] == game[i * 3 + 2] and game[i * 3] != 0:
            return 1
    for i in range(0, 3):
        if game[i] == game[3 + i] == game[6 + i] and game[i] != 0:
            return 1
    if game[0] == game[4] == game[8] and game[0] != 0:
        return 1
    elif game[2] == game[4] == game[6] and game[2] != 0:
        return 1


    for i in range(0, 3):
        for j in range(0, 3):
            if game[3 * i + j] == 0:
                return 0

    return -1

def bots_turn(message):
    done = False
    turn = -1

    if game[4] == 0:
        game[4] = 2
    else:
        for i in range(0, 3):
            if game[i * 3] == game[i * 3 + 1] and game[i * 3 + 2] == 0 and game[i * 3] != 0:
                if game[i * 3] == 2 and turn != -1:
                    done = False
                    game[turn] = 0

                if not done:
                    turn = i * 3 + 2
                    game[i * 3 + 2] = 2
                    done = True
                if game[i * 3] == 2:
                    return True
            elif game[i * 3] == game[i * 3 + 2] and game[i * 3 + 1] == 0 and game[i * 3] != 0:
                if game[i * 3] == 2 and turn != -1:
                    done = False
                    game[turn] = 0

                if not done:
                    turn = i * 3 + 1
                    game[i * 3 + 1] = 2
                    done = True
                if game[i * 3] == 2:
                    return True
            elif game[i * 3 + 1] == game[i * 3 + 2] and game[i * 3] == 0 and game[i * 3 + 1] != 0:
                if game[i * 3 + 1] == 2 and turn != -1:
                    done = False
                    game[turn] = 0

                if not done:
                    turn = i * 3
                    game[i * 3] = 2
                    done = True
                if game[i * 3 + 1] == 2:
                    return True
        if not done:
            for i in range(0, 3):
                if game[i] == game[3 + i] and game[6 + i] == 0 and game[i] != 0:
                    if game[i] == 2 and turn != -1:
                        done = False
                        game[turn] = 0

                    if not done:
                        turn = 6 + i
                        game[6 + i] = 2
                        done = True
                    if game[i] == 2:
                        return True
                elif game[i] == game[6 + i] and game[3 + i] == 0 and game[i] != 0:
                    if game[i] == 2 and turn != -1:
                        done = False
                        game[turn] = 0

                    if not done:
                        turn = 3 + i
                        game[3 + i] = 2
                        done = True
                    if game[i] == 2:
                        return True
                elif game[3 + i] == game[6 + i] and game[i] == 0 and game[3 + i] != 0:
                    if game[3 + i] == 2 and turn != -1:
                        done = False
                        game[turn] = 0

                    if not done:
                        turn = i
                        game[i] = 2
                        done = True
                    if game[3 + i] == 2:
                        return True
        if not done:
            if game[4] == 2:
                if game[0] == 2 and game[8] == 0:
                    game[8] = 2
                    done = True
                elif game[2] == 2 and game[6] == 0:
                    game[6] = 2
                    done = True
                elif game[6] == 2 and game[2] == 0:
                    game[2] = 2
                    done = True
                elif game[8] == 2 and game[0] == 0:
                    game[0] = 2
                    done = True
            elif game[4] == 1:
                if game[0] == 1 and game[8] == 0:
                    game[8] = 2
                    done = True
                elif game[2] == 1 and game[6] == 0:
                    game[6] = 2
                    done = True
                elif game[6] == 1 and game[2] == 0:
                    game[2] = 2
                    done = True
                elif game[8] == 1 and game[0] == 0:
                    game[0] = 2
                    done = True
        if not done:
                if game[0] == 0 and game[8] == 0:
                    game[0] = 2
                elif game[2] == 0 and game[6] == 0:
                    game[2] = 2
                else: #уже на ничью
                    for i in range(0, 9):
                        if game[i] == 0:
                            game[i] = 2
                            break
                #elif game[6] == 0:
                #    game[6] = 2
                #elif game[8] == 0:
                #    game[8] = 2

    #bot.send_message(message.from_user.id, "Мой ход")
    #show_board(message)
    return win_check()

# Функции
def num_gcd(x, y):
    if x % y == 0:
        return y
    if y % x == 0:
        return x

    if (x > y):
        return num_gcd(x % y, y)
    else:
        return num_gcd(x, y % x)

def GCD(message, arg_a, arg_b, cashe, match_number):

    res = 0

    if re.match(match_number, arg_a) and re.match(match_number, arg_b):
        a = float(arg_a)
        b = float(arg_b)

        a = a // 1
        b = b // 1

        for key in cashe.keys():

            if key == (a, b):
                res = cashe[(a, b)]
                bot.send_message(message.from_user.id, "Результат: " + str(res) + " (получен из кэша)")
            elif key == (b, a):
                res = cashe[(b, a)]
                bot.send_message(message.from_user.id, "Результат: " + str(res) + " (получен из кэша)")

        if res == 0:
            res = num_gcd(int(a), int(b))
            bot.send_message(message.from_user.id, "Результат: " + str(res))
            cashe[(a, b)] = res

    else:
        bot.send_message(message.from_user.id, "Кажется, введены не положительные числа, поэтому получить результат не удалось(")

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global state
    global arg_a, arg_b, cashe, match_number
    global game, first

    if state == 0:
        if message.text == "/start":
            bot.send_message(message.from_user.id, "Привет!");
        elif "привет" in message.text.lower():
            bot.send_message(message.from_user.id, "Еще раз привет! " + hello)
        elif message.text == "/help":
            bot.send_message(message.from_user.id, hello)
        elif message.text.lower() == "нод":
            bot.send_message(message.from_user.id, "Ищу наибольший общий делитель двух чисел, для выхода отправь \'все\'")
            state = 1
            bot.send_message(message.from_user.id, "Первое число:")
        elif message.text.lower() == "игра":
            bot.send_message(message.from_user.id, "Игра в крестики-нолики, для выхода отправь \'все\'")
            state = 10
            game = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            bot.send_message(message.from_user.id, "Выбери Х или О (начинает игрок, выбравший Х!)")
        else:
            bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши \'/help\'")
    elif state == 1:
            if message.text.lower() == "все" or message.text.lower() == "всё":
                bot.send_message(message.from_user.id, hello)
                state = 0
            else:
                arg_a = message.text
                state = 2
                bot.send_message(message.from_user.id, "Второе число:")
    elif state == 2:
        if message.text.lower() == "все" or message.text.lower() == "всё":
            bot.send_message(message.from_user.id, hello)
            state = 0
        else:
            arg_b = message.text
            GCD(message, arg_a, arg_b, cashe, match_number)
            state = 1
            bot.send_message(message.from_user.id, "Еще раз? Для выхода отправь \'все\'!")
            bot.send_message(message.from_user.id, "Первое число:")
    elif state == 10:
        if message.text.lower() == "все" or message.text.lower() == "всё":
            bot.send_message(message.from_user.id, hello)
            state = 0
        elif message.text.lower() == "x" or message.text.lower() == "х" or message.text == "1":
            first = True
            state = 11
            bot.send_message(message.from_user.id, "Чтобы сделать ход, напиши число от 1 до 9:\n1 2 3\n4 5 6\n7 8 9")
        elif message.text.lower() == "o" or message.text.lower() == "о" or message.text == "2":
            first = False
            state = 11
            bot.send_message(message.from_user.id, "Чтобы сделать ход, напиши число от 1 до 9:\n1 2 3\n4 5 6\n7 8 9\nНо сначала мой ход")
            bots_turn(message)
            bot.send_message(message.from_user.id, "Мой ход")
            show_board(message)
        else:
            bot.send_message(message.from_user.id, "Выбери Х или О (начинает игрок, выбравший Х!)")
    elif state == 11:
        if message.text.lower() == "все" or message.text.lower() == "всё":
            bot.send_message(message.from_user.id, hello)
            state = 0
        elif re.match(match_only_number, message.text):
            if game[int(message.text) - 1] != 0:
                bot.send_message(message.from_user.id, "Этот ход уже был сделан, выбери другой")
            else:
                game[int(message.text) - 1] = 1
                show_board(message)

                win = win_check()
                if win == 1:
                    bot.send_message(message.from_user.id, "Поздравляю, ты победил! Если хочешь сыграть еще раз, напиши \'игра\'")
                    state = 0
                elif win == -1:
                    bot.send_message(message.from_user.id, "Ничья! Если хочешь сыграть еще раз, напиши \'игра\'")
                    state = 0
                else:
                    win = bots_turn(message)
                    bot.send_message(message.from_user.id, "Мой ход")
                    show_board(message)
                    if win == 1:
                        bot.send_message(message.from_user.id, "Победа за мной! Если хочешь сыграть еще раз, напиши \'игра\'")
                        state = 0
                    elif win == -1:
                        bot.send_message(message.from_user.id, "Ничья! Если хочешь сыграть еще раз, напиши \'игра\'")
                        state = 0
        else:
            bot.send_message(message.from_user.id, "Чтобы выйти отправь \'все\' или напиши число от 1 до 9 чтобы сделать ход:\n1 2 3\n4 5 6\n7 8 9")


bot.polling(none_stop=True, interval=0)
