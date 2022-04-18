#!/usr/bin/env python
# coding: utf-8
from turtle import st
from termcolor import colored
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
    while attempt < 6:
        guess = input().upper()
        if len(guess) == 5 and guess.isalpha() and match(guess) == True:
            if arf(guess.lower()) == True:
                sys.stdout.write('\x1b[1A')
                sys.stdout.write('\x1b[2K')
            
                for i in range(min(len(guess), 5)):
                    if guess[i] == word[i]:
                        print((Fore.GREEN + guess[i]), end="")
                    elif guess[i] in word:
                        print((Fore.YELLOW + guess[i]), end="")
                    else:
                        print(guess[i], end="")
                print()
                attempt += 1
                
                if guess == word:
                    print('Поздравляем! Вы угадали слово за %i попытки.' %attempt)
                elif attempt == 6:
                    print('Вы не угадали слово с 6 попыток, это было %s' %word.upper())
            else:
                print('В словаре игры нет такого слова, попробуйте другое!')
                game()

        else:
            print('слово должно состоять из пяти букв')
            game()
game()



