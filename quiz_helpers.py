import json
import random


def get_random_question():
    with open('quiz_bank.json', 'r', encoding='UTF-8') as file:
        quiz_bank = json.load(file)
    question, _ = random.choice(list(quiz_bank.items())) 
    return question
        