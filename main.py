import customtkinter
from func_math import *
from smartlog import log

log.setLevel('DEBUG')

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
# app.geometry('800x400')
app.attributes("-fullscreen", True)


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
                active_dict[active_players[j]] = float("{:.2f}".format(old_relys[j] - 0.03))  #old_relys[j] - 0.03

        for player in active_players:
            player.place(relx=0.5, rely=active_dict[player], anchor=customtkinter.CENTER)
        score_frame.after(25, table_movement, players_list)


def upp_score(player):
    global score_dict
    # log.debug(f'old one\n{score_dict}')
    score_dict[player] += 2
    # log.debug(f'new one\n{score_dict}')
    sorted_dict = dict(sorted(score_dict.items(), key=lambda item: item[1], reverse=True))
    players_list = list(sorted_dict.keys())
    log.debug(f'sorted one\n{sorted_dict}')

    table_movement(players_list)


# TABLE FRAMES
score_frame = customtkinter.CTkFrame(master=app, fg_color='#212325', corner_radius=10)
score_frame.place(rely=0.5, relwidth=1, relheight=0.5)

frames_dict = {'master': score_frame, 'corner_radius': 10}
player1 = customtkinter.CTkFrame(**frames_dict)
player2 = customtkinter.CTkFrame(**frames_dict)
player3 = customtkinter.CTkFrame(**frames_dict)
player4 = customtkinter.CTkFrame(**frames_dict)

place_dict = {'relx': 0.5, "relwidth": 0.8, "relheight": 0.2, "anchor": customtkinter.CENTER}
rely_list = get_rely_list(place_dict["relheight"])

score_dict = {player1: 0, player2: 0, player3: 0, player4: 0}
s = dict(sorted(score_dict.items(), key=lambda item: item[1], reverse=True))
l = list(s.keys()).index(player1)


player1.place(**place_dict, rely=rely_list[0])
player2.place(**place_dict, rely=rely_list[1])
player3.place(**place_dict, rely=rely_list[2])
player4.place(**place_dict, rely=rely_list[3])

# log.debug(player1.place_info()['rely'])
# log.debug(player2.place_info()['rely'])
# log.debug(player3.place_info()['rely'])
# log.debug(player4.place_info()['rely'])


# Buttons
butt_dict = {"text": "CTkButton"}  # , "command": lambda: player_movement(0.14)
b1 = customtkinter.CTkButton(master=player1, **butt_dict, command=lambda: upp_score(player1))
b2 = customtkinter.CTkButton(master=player2, **butt_dict, command=lambda: upp_score(player2))
b3 = customtkinter.CTkButton(master=player3, **butt_dict, command=lambda: upp_score(player3))
b4 = customtkinter.CTkButton(master=player4, **butt_dict, command=lambda: upp_score(player4))

bplace_dict = {"relx": 0.5, "rely": 0.5, "anchor": customtkinter.CENTER}
b1.place(**bplace_dict)
b2.place(**bplace_dict)
b3.place(**bplace_dict)
b4.place(**bplace_dict)

app.mainloop()

# if __name__ == '__main__':
#     pass
# https://www.youtube.com/watch?v=6NSjTE--hjw&ab_channel=DJDaveHarris-Topic
# player1.winfo_rooty()

# def player_movement(finish):
#     rely = float(player1.place_info()['rely'])
#     log.debug(rely)
#     if rely != finish:
#         new_rely = rely + 0.03 if rely < finish else rely - 0.03
#         player1.place(relx=0.5, rely=new_rely, anchor=customtkinter.CENTER)
#
#         player1.after(25, player_movement, finish)