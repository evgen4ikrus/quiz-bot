import os


def get_question_and_answer(quiz_question):
    quiz_question = quiz_question.split('\n\n')
    question, answer = '', ''
    for question_section in quiz_question:
        if question_section.startswith('Вопрос'):
            question = question_section.partition('\n')[2]
        if question_section.startswith('Ответ:'):
            answer = question_section.partition('\n')[2]
    return question, answer


def get_quiz_bank(folder='quiz_questions'):
    files = os.listdir(folder)
    quiz_bank = {}
    for file in files:
        with open(os.path.join(folder, file), 'r', encoding='KOI8-R') as file:
            file_contents = file.read()
            quiz_questions = file_contents.split('\n\n\n')
            for quiz_question in quiz_questions:
                question, answer = get_question_and_answer(quiz_question)
                quiz_bank[question] = answer
    return(quiz_bank)
