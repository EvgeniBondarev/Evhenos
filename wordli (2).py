#!/usr/bin/env python
# coding: utf-8
from time import sleep, time
import random
import sys
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

def read_random_word():
    with open("words.txt", encoding='utf-8') as f:
        word_array = f.read().splitlines()
        return random.choice(word_array)

def match(text, alphabet=set('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ')):
    return not alphabet.isdisjoint(text)

def arf(str):
    with open("words.txt", encoding='utf-8') as file:
        text=file.read().splitlines()
        if str in text:
            return True
        else:
            return False


word = read_random_word().upper()
global attempt
attempt = 0

def game():
    global attempt
    print("Введите слово:")
    while attempt < 7:
        player_word = input().upper()
        if len(player_word) == 5 and player_word.isalpha() == True and match(player_word) == True:
            if arf(player_word.lower()) == True:
                sys.stdout.write('\x1b[1A')
                sys.stdout.write('\x1b[2K')
            
                for i in range(min(len(player_word), 5)):
                    if player_word[i] == word[i]:
                        print((Fore.GREEN + player_word[i]), end="")
                    elif player_word[i] in word:
                        print((Fore.YELLOW + player_word[i]), end="")
                    else:
                        print(player_word[i], end="")
                    sleep(0.2)
                print()
                attempt += 1
                
                if player_word == word:
                    print(f'Поздравляем! Вы угадали слово за {attempt} попытки.')
                elif attempt == 6:
                    print(f'Вы не угадали слово с 5 попыток, это было {Fore.GREEN + word.upper()}.')
            else:
                print('В словаре игры нет такого слова, попробуйте другое!')
                game()

        else:
            print('слово должно состоять из пяти букв')
            game()
game()

