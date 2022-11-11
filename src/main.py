from functions.func_math import get_rely_list
from functions.take_envs import *
from functions.smartlog import log
from animation.choose_categories import *


log.setLevel("DEBUG")
cat_dir, categories, cat_dict = get_categories()


def table_movement(players_list):
    # TODO DISABLE BUTTONS
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

    for b in buttons2+buttons1+buttons_1:
        b.configure(state='disabled')

    table_movement(players_list)


with open("config.json", "r", encoding='utf-8') as json_mapping:
    config = load(json_mapping)

# MAIN APP
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
# app.geometry('800x400')
app.attributes("-fullscreen", True)


frame = customtkinter.CTkFrame(master=app, fg_color="#212325", corner_radius=10)
frame.place(relwidth=1, relheight=0.4)

button = customtkinter.CTkButton(master=frame, text="CTkButton",
                                 command=lambda: start_cat_anim(app, score_frame, frame, cat_dict))
button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)


# TABLE FRAMES
score_frame = customtkinter.CTkFrame(master=app, fg_color="#212325", corner_radius=10)
score_frame.place(rely=0.6, relwidth=1, relheight=0.4)

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
