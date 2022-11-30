from PIL import Image, ImageTk, ImageSequence
from os import getenv, listdir, remove
from json import dump
from playsound import playsound
import threading
from random import sample


def play_sound(song):
    threading.Thread(target=playsound, args=(song,), daemon=True).start()


def get_rely_list(relheight, players=4):
    realy_y = (100 - (int(relheight * 100) * players)) / ((players + 1) * 100)
    rely_list = [realy_y + relheight / 2,
                 (realy_y + relheight / 2) + (realy_y + relheight) * 1,
                 (realy_y + relheight / 2) + (realy_y + relheight) + (realy_y + relheight),
                 (realy_y + relheight / 2) + (realy_y + relheight) + (realy_y + relheight) + (realy_y + relheight)]
    return rely_list


def get_img(path, sizex=1920, sizey=1080):
    circle_img = Image.open(path)
    circle_img = circle_img.resize((sizex, sizey), Image.Resampling.LANCZOS)
    img = ImageTk.PhotoImage(circle_img)
    return img


def save_choose(args, used_categories, theme):
    print(theme)
    used_categories.append(theme)
    args["finish"] = True



def get_categories():
    cat_dir = getenv("categories")
    categories = [i.split('1')[0] for i in listdir(cat_dir) if '1' in i]
    temp_stuff = [(c, (f"{cat_dir}/{c}1.png", f"{cat_dir}/{c}2.png")) for c in categories]
    cat_dict = {key: value for key, value in temp_stuff}
    return cat_dir, categories, cat_dict


def get_frames(folder):
    frames = [f"{folder}/{frame}" for frame in listdir(folder)]
    return sorted(frames)


def get_questions(categories, line):
    que_list = line.split('|')
    temp_stuff = [(categories[i], que_list[i].strip()) for i in range(len(categories))]
    questions_dict = {key: value for key, value in temp_stuff}
    return questions_dict


def delete_categories(cat_dict, questions, categories, theme):
    del cat_dict[theme]
    del questions[theme]
    del categories[categories.index(theme)]
    remove('theme.json')
