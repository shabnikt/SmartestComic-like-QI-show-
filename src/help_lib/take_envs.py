from os import getenv, listdir
from json import load


def get_categories():
    cat_dir = getenv("categories")
    categories = [i.split('1')[0] for i in listdir(cat_dir) if '1' in i]
    temp_stuff = [(c, (f"{cat_dir}/{c}1.png", f"{cat_dir}/{c}2.png")) for c in categories]
    cat_dict = {key: value for key, value in temp_stuff}
    return cat_dir, categories, cat_dict


def get_questions(categories, line):
    que_list = line.split('|')
    temp_stuff = [(categories[i], que_list[i].strip()) for i in range(len(categories))]
    questions_dict = {key: value for key, value in temp_stuff}
    return questions_dict