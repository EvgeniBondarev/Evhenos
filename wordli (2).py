#!/usr/bin/env python
# coding: utf-8
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

print("Введите слово:")
word = read_random_word().upper()

for attempt in range(1,7):
    guess = input().upper()
    
 
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')
   

   
    for i in range(min(len(guess), 5)):
        if guess[i] == word[i]:
            print((Fore.GREEN + guess[i]), end="")
        elif guess[i] in word:
            print((Fore.YELLOWпа + guess[i]), end="")
        else:
            print(guess[i], end="")
    print()
    
    if guess == word:
        print('Поздравляем! Вы угадали слово за %i попытки.' %attempt)
    elif attempt == 6:
        print('Вы не угадали слово с 6 попыток, это было %s' %word.upper())





