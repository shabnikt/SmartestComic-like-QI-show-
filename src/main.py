import os
from json import load
from playsound import playsound

from help_lib.helper import get_rely_list, get_categories
from help_lib.log_formatter import log
from help_lib.categories_animation import *


log.setLevel(getenv("LOGLEVEL"))
bg = getenv('BG')
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

cat_dir, categories, cat_dict = get_categories()

with open("media/question.json", "r", encoding='utf-8') as json:
    questions = load(json)

with open("config.json", "r", encoding='utf-8') as json_mapping:
    config = load(json_mapping)


def animate_text(text, widget):
    t = widget.cget('text')
    if t != text:
        t += text.replace(t, '')[0]
        widget.configure(text=t)
        widget.after(40, animate_text, text, widget)


def choose_set_lab(event):
    with open("theme.json", "r", encoding='utf-8') as theme_file:
        theme = load(theme_file)['theme']

    with open("media/question.json", "r", encoding='utf-8') as json:
        que = load(json)[theme]

    for widget in qhost_question_frame.winfo_children():
        widget.destroy()

    question_label = tkinter.Label(master=qhost_question_frame, text=que['text'], bg=transparent_color, **que['widget'])
    question_label.place(**que['place'], anchor=tkinter.CENTER)


def table_movement(players_list):
    temp_old_relys = [float(_.place_info()['rely']) for _ in players_list]

    new_relys = list()
    active_players = list()
    old_relys = list()

    for i in range(len(temp_old_relys)):
        if temp_old_relys[i] != rely_list[i]:
            active_players.append(players_list[i])
            old_relys.append(temp_old_relys[i])
            new_relys.append(rely_list[i])

    if active_players:
        active_dict = {}
        for j in range(len(active_players)):
            if old_relys[j] < new_relys[j]:
                active_dict[active_players[j]] = float("{:.2f}".format(old_relys[j] + 0.03))
            else:
                active_dict[active_players[j]] = float("{:.2f}".format(old_relys[j] - 0.03))

        for player in active_players:
            player.place(relx=0.5, rely=active_dict[player], anchor=customtkinter.CENTER)
        score_frame.after(25, table_movement, players_list)
    else:
        for b in buttons2 + buttons1 + buttons_1:
            b.configure(state='normal')


def play_music(event):
        playsound('media\smartest_comic.wav')


def change_score(player, value):
    global score_dict
    score_dict[player] += value
    score_labels[list(score_dict.keys()).index(player)].configure(text=score_dict[player])
    sorted_dict = dict(sorted(score_dict.items(), key=lambda item: item[1], reverse=True))
    players_list = list(sorted_dict.keys())
    log.debug(f'sorted one\n{sorted_dict}')

    for b in buttons2+buttons1+buttons_1:
        b.configure(state='disabled')

    table_movement(players_list)


def show_question(event):
    global categories, cat_dict, questions
    with open("theme.json", "r", encoding='utf-8') as theme_file:
        theme = load(theme_file)['theme']
    print(theme)

    for widget in qhost_question_frame.winfo_children():
        widget.destroy()

    question = questions[theme]
    question_label = tkinter.Label(master=qhost_question_frame, text='', bg=transparent_color, **question['widget'])
    question_label.place(**question['place'], anchor=tkinter.CENTER)
    text = question['text']
    animate_text(text, question_label)

    del cat_dict[theme]
    del questions[theme]
    del categories[categories.index(theme)]
    os.remove('theme.json')


# MAIN APP
app = customtkinter.CTk()
app.attributes("-fullscreen", True)

bg_img = get_img(getenv('BG_IMAGE'), 1920, 1080)
bg_image = tkinter.Label(master=app, image=bg_img)
bg_image.place(relx=0.5, rely=0.5, relheight=1, relwidth=1, anchor=customtkinter.CENTER)


# QUESTIONS FRAME
question_frame = customtkinter.CTkFrame(master=app, fg_color='#0c3653', bg_color='#000000', corner_radius=10)
question_frame.place(relx=0.5, rely=0.30, relwidth=0.58, relheight=0.546, anchor=customtkinter.CENTER)

que_img = get_img(getenv('QUESTION_BG'), 1114, 590)
question_bg = tkinter.Label(master=question_frame, image=que_img)
question_bg.place(relx=0.5, rely=0.5, relheight=1, relwidth=1, anchor=customtkinter.CENTER)

question_bg.bind('<Control-Button-1>', lambda event: start_cat_anim(app, score_frame, question_frame, cat_dict))
question_bg.bind('<Alt-Button-1>', show_question)
question_bg.bind('<Alt-Button-3>', choose_set_lab)
question_bg.bind('<Button-2>', lambda e: playsound(getenv('MUSIC')))

# =================================================================================================================
transparent_color = bg

score_window = customtkinter.CTkToplevel()
score_window.attributes("-fullscreen", True)
score_window.attributes('-alpha', 0.6)
score_window.wm_attributes("-transparentcolor", transparent_color)
score_window.configure(background=transparent_color)
score_window.attributes('-topmost', 'true')

qhost_question_frame = customtkinter.CTkFrame(master=score_window, fg_color=transparent_color, bg_color=transparent_color, corner_radius=10)
qhost_question_frame.place(relx=0.5, rely=0.30, relwidth=0.58, relheight=0.546, anchor=customtkinter.CENTER)

# TABLE FRAME
score_frame = customtkinter.CTkFrame(master=score_window, fg_color=bg, corner_radius=10)
score_frame.place(relx=0.5, rely=0.8, relwidth=0.58, relheight=0.4, anchor=customtkinter.CENTER)

frames_dict = {"master": score_frame}
frames_dict.update(config["frames_dict"])
player1 = customtkinter.CTkFrame(**frames_dict)
player2 = customtkinter.CTkFrame(**frames_dict)
player3 = customtkinter.CTkFrame(**frames_dict)
player4 = customtkinter.CTkFrame(**frames_dict)

score_dict = {player1: 0, player2: 0, player3: 0, player4: 0}
frames_list = list(score_dict.keys())
anchor_dict = {"anchor": customtkinter.CENTER}

place_dict = config["place_dict"]
rely_list = get_rely_list(place_dict["relheight"])

for i in range(len(frames_list)):
    frames_list[i].place(**place_dict, **anchor_dict, rely=rely_list[i])

# BUTTONS
butt2_dict = config["butt2_dict"]
butt1_dict = config["butt1_dict"]
butt_1_dict = config["butt_1_dict"]

b2place_dict = config["b2place_dict"]
b1place_dict = config["b1place_dict"]
b_1place_dict = config["b_1place_dict"]

buttons2 = [customtkinter.CTkButton(master=frames_list[i], **butt2_dict,
                                    command=lambda i=i: change_score(frames_list[i], 2)) for i in range(4)]
for button in buttons2:
    button.place(**b2place_dict, **anchor_dict)

buttons1 = [customtkinter.CTkButton(master=frames_list[i], **butt1_dict,
                                    command=lambda i=i: change_score(frames_list[i], 1)) for i in range(4)]
for button in buttons1:
    button.place(**b1place_dict, **anchor_dict)

buttons_1 = [customtkinter.CTkButton(master=frames_list[i], **butt_1_dict,
                                     command=lambda i=i: change_score(frames_list[i], -1)) for i in range(4)]
for button in buttons_1:
    button.place(**b_1place_dict, **anchor_dict)



# LABELS
names = config["names"]
names_dict = config["names_dict"]
lplace_dict = config["lplace_dict"]
splace_dict = config["splace_dict"]

labels = [customtkinter.CTkLabel(master=frames_list[i], text=names[i], **names_dict) for i in range(4)]
for label in labels:
    label.place(**lplace_dict, **anchor_dict)

score_labels = [customtkinter.CTkLabel(master=frames_list[i], text=score_dict[frames_list[i]], **names_dict)
                for i in range(4)]
for score in score_labels:
    score.place(**splace_dict, **anchor_dict)


app.mainloop()
