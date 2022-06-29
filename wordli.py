#!/usr/bin/env python
# coding: utf-8
from time import sleep, time
import random
import sys
import os
import colorama
from colorama import Fore, Back, Style
python = sys.executable
colorama.init(autoreset=True)



def read_random_word():
    with open(r"C:\Users\Evgeni\Desktop\js\words.txt", "r") as f:
        word_array = f.read().splitlines()
        return random.choice(word_array)

def match(text, alphabet=set('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ')):
    return not alphabet.isdisjoint(text)

def arf(str):
    with open(r"C:\Users\Evgeni\Desktop\js\words.txt", "r") as file:
        text=file.read().splitlines()
        if str in text:
            return True
        else:
            return False

def new_game():
    os.system('CLS')
    print(Fore.GREEN + 'Новая игра!')
    sleep(3)
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')
    print('Ведите слово')
    game()



word = read_random_word().upper()
global attempt
attempt = 0
arr = []

def game():
    global attempt
    while attempt < 6:
        player_word = input().upper()
        if len(player_word) == 5 and player_word.isalpha() == True and match(player_word) == True:
            if arf(player_word.lower()) == True:
                sys.stdout.write('\x1b[1A')
                sys.stdout.write('\x1b[2K')
            
                for i in range(min(len(player_word), 5)):
                    if player_word[i] == word[i]:
                        arr.append(Fore.GREEN + player_word[i])
                    elif player_word[i] in word:
                        arr.append(Fore.YELLOW + player_word[i])
                    else:
                        print(player_word[i], end="")
                    print()
                    sleep(0.2)

                print()
                attempt += 1
        
                if player_word == word:
                    print(f'Поздравляем! Вы угадали слово {Fore.GREEN + word.upper()} за {attempt} попытки.')
                    sleep(3)
                    new_game()
                    
                elif attempt == 5:
                    print(f'Вы не угадали слово с 5 попыток, это было {Fore.GREEN + word.upper()}.')
                    sleep(3)
                    new_game()
                    
                    
            else:
                print('В словаре игры нет такого слова, попробуйте другое!')
                sleep(3)
                sys.stdout.write('\x1b[1A')
                sys.stdout.write('\x1b[2K')
                sys.stdout.write('\x1b[1A')
                sys.stdout.write('\x1b[2K')
                
                game()

        else:
            print('слово должно состоять из пяти букв')
            sleep(3)
            sys.stdout.write('\x1b[1A')
            sys.stdout.write('\x1b[2K')
            sys.stdout.write('\x1b[1A')
            sys.stdout.write('\x1b[2K')
            game()

new_game()