import time
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

from json import load

from help_lib.helper import *
from help_lib.log_formatter import log
from help_lib.categories_animation import *
from help_lib.animation import animate_text, frame_animation

thread_sounds = dict()


def create_sound(player, filename):
    thread_sounds[int(player)] = threading.Thread(target=playsound, args=(f"{getenv('WHISTLE')}/{filename}.wav",), daemon=True)
    thread_sounds[int(player)].start()


def receive():
    while True:
        try:
            data = receive_socket.recv(1024).decode("utf8")
            player, filename = data.split("|")
            if int(player) not in thread_sounds.keys() or not thread_sounds[int(player)].is_alive():
                create_sound(player, filename)
        except OSError:
            break


def send(event=None):
    msg = '417306088|Проверка. Random.'
    send_socket.send(bytes(msg, "utf8"))


def start_animation(gif):
    global flag
    if flag:
        flag = False
        frame_animation(gif, bg_image, app)
        bg_image.configure(image=bg_img)
        bg_image.image = bg_img

        question_frame.place(relx=0.5, rely=0.30, relwidth=0.58, relheight=0.546, anchor=customtkinter.CENTER)
        qhost_question_frame.place(relx=0.5, rely=0.30, relwidth=0.58, relheight=0.546, anchor=customtkinter.CENTER)
        score_frame.place(relx=0.5, rely=0.8, relwidth=0.58, relheight=0.4, anchor=customtkinter.CENTER)


def choose_category(event):
    global choosers
    score_frame.place_forget()
    question_bg.configure(image=que_img)
    question_bg.image = que_img
    for widget in qhost_question_frame.winfo_children():
        widget.destroy()

    if len(used_categories) < 6:
        args = {"score_frame": score_frame, "categories": sample(set(categories) - set(used_categories), 5),
                "cat_dict": cat_dict, "chooser": choosers[0], "used": used_categories, 'finish': False}
        play_sound(getenv('THEME'))
        animate_categories(app, args)
        choosers = choosers[1:] + [choosers[0]]
    else:
        play_sound(getenv('FINALE'))

        end_bg = tkinter.Label(master=app)
        end_bg.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=customtkinter.CENTER)

        frame_animation(getenv("BIDEN"), end_bg, app)


def choose_set_lab(event):
    with open('theme.json', "r", encoding='utf-8') as json:
        theme = load(json)['theme']
    question_bg.configure(image=que_img)
    question_bg.image = que_img

    with open(getenv('QUESTIONS'), "r", encoding='utf-8') as json:
        que = load(json)[theme]

    for widget in qhost_question_frame.winfo_children():
        widget.destroy()

    question_label = tkinter.Label(master=qhost_question_frame, text=que['text'], bg=transparent_color, **que['widget'])
    question_label.place(**que['place'], anchor=tkinter.CENTER)


def show_image(event):
    try:
        theme = used_categories[-1]
        log.debug(theme)
        img = get_img(f'media/question/images/{theme}.png', 1114, 590)

        for widget in qhost_question_frame.winfo_children():
            widget.destroy()

        question_bg.configure(image=img)
        question_bg.image = img
    except Exception as e:
        log.warning(f'Show image error: {e}')


def show_question(event):
    global categories, cat_dict, questions

    question_bg.configure(image=que_img)
    question_bg.image = que_img

    try:
        theme = used_categories[-1]
        log.debug(theme)

        for widget in qhost_question_frame.winfo_children():
            widget.destroy()

        question = questions[theme]
        question_label = tkinter.Label(master=qhost_question_frame, text='', bg=transparent_color, **question['widget'])
        question_label.place(**question['place'], anchor=tkinter.CENTER)
        text = question['text']
        animate_text(text, question_label, print)
    except Exception as e:
        log.warning(f'Show question error: {e}')


# TABLE SCORE MOVEMENT
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


def change_score(player, value):
    global score_dict
    score_dict[player] += value
    score_labels[list(score_dict.keys()).index(player)].configure(text=score_dict[player])
    sorted_dict = dict(sorted(score_dict.items(), key=lambda item: item[1], reverse=True))
    players_list = list(sorted_dict.keys())
    log.debug(f'sorted one\n{sorted_dict}')

    for b in buttons2 + buttons1 + buttons_1:
        b.configure(state='disabled')

    table_movement(players_list)


# VARIABLES
log.setLevel(getenv("LOGLEVEL"))
bg = getenv('BG')
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

cat_dir, categories, cat_dict = get_categories()
used_categories = list()

with open(getenv('QUESTIONS'), "r", encoding='utf-8') as json:
    questions = load(json)

with open("config.json", "r", encoding='utf-8') as json_mapping:
    config = load(json_mapping)

# MAIN APP
app = customtkinter.CTk()
app.attributes("-fullscreen", True)

bg_img = get_img(getenv('BG_IMAGE'), 1920, 1080)
start_img = get_img("media/start.png", 1920, 1080)
bg_image = tkinter.Label(master=app, image=start_img)
bg_image.place(relx=0.5, rely=0.5, relheight=1, relwidth=1, anchor=customtkinter.CENTER)
flag = True
bg_image.bind('<Button-2>', lambda e: start_animation(getenv('START')))

# QUESTIONS FRAME
question_frame = customtkinter.CTkFrame(master=app, fg_color='#0c3653', bg_color='#000000', corner_radius=10)

que_img = get_img(getenv('QUESTION_BG'), 1114, 590)
question_bg = tkinter.Label(master=question_frame, image=que_img)
question_bg.place(relx=0.5, rely=0.5, relheight=1, relwidth=1, anchor=customtkinter.CENTER)

question_bg.bind('<Control-Button-1>', choose_category)
question_bg.bind('<Alt-Button-1>', show_question)
question_bg.bind('<Alt-Button-3>', show_image)
question_bg.bind('<Alt-Button-2>', choose_set_lab)
question_bg.bind('<Control-Button-3>', lambda e: play_sound(getenv('THEME')))
question_bg.bind('<Control-Button-2>', send)

# =================================================================================================================
transparent_color = bg

score_window = customtkinter.CTkToplevel()
score_window.attributes("-fullscreen", True)
score_window.attributes('-alpha', 0.6)
score_window.wm_attributes("-transparentcolor", transparent_color)
score_window.configure(background=transparent_color)
score_window.attributes('-topmost', 'true')

qhost_question_frame = customtkinter.CTkFrame(master=score_window, fg_color=transparent_color,
                                              bg_color=transparent_color, corner_radius=10)

# TABLE FRAME
score_frame = customtkinter.CTkFrame(master=score_window, fg_color=bg, corner_radius=10)

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
choosers = names
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

# Connect to sockets
receive_socket = socket(AF_INET, SOCK_STREAM)
receive_socket.connect(("localhost", 8080))

time.sleep(1)

send_socket = socket(AF_INET, SOCK_STREAM)
send_socket.connect(("localhost", 8000))

receive_thread = Thread(target=receive)
receive_thread.start()

app.mainloop()
