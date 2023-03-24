import customtkinter
import tkinter

from json import load
from os import getenv
from os.path import exists
from help_lib.animation import frame_animation
from help_lib.helper import get_img, save_choose, get_frames


def animate_categories(app, args):
    anim_frame = customtkinter.CTkFrame(master=app, fg_color='#212325')
    anim_frame.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=customtkinter.CENTER)
    args["anim_frame"] = anim_frame

    img = get_img(getenv('BG_IMAGE'))
    anim_bg = tkinter.Label(master=anim_frame, image=img)
    anim_bg.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=customtkinter.CENTER)
    anim_bg.image = img

    frame_animation(getenv("CIRCLE"), anim_bg, app, (1920, 1080))

    create_top_level(args)


def create_top_level(args):
    transparent_color = '#b5b3b3'
    top = customtkinter.CTkToplevel(args["anim_frame"], fg_color=transparent_color)
    top.attributes("-fullscreen", True)
    top.wm_attributes("-transparentcolor", transparent_color)
    top.attributes('-topmost', 'true')
    args["top"] = top

    font_size = 2

    label = customtkinter.CTkLabel(master=top, text=f'Выбирает категорию\n{args["chooser"]}', text_font=('Calibri', font_size),
                                   text_color='#ffffff', fg_color=transparent_color, bg_color=transparent_color)
    label.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

    resize_label(label, font_size, args)


def resize_label(label, font_size, args):
    if font_size < 50:
        font_size += 4
        label.configure(text_font=('Helvetica', font_size))

        label.after(50, resize_label, label, font_size, args)
    else:
        move_label_up(label, font_size, args)


def move_label_up(label, font_size, args):
    tempy = float(label.place_info()["rely"])

    if font_size > 30 or tempy != 0.1:
        font_size -= 5
        rely = tempy - 0.1 if tempy != 0.1 else tempy

        label.configure(text_font=('Helvetica', font_size))
        label.place(relx=0.5, rely=rely, anchor=customtkinter.CENTER)

        label.after(50, move_label_up, label, font_size, args)

    else:
        n = 0
        themes_loop(n, args)


def themes_loop(n, args):
    n = n if n < len(args["categories"]) else 0

    curr_width = 0.3

    sizex = int(1920 * curr_width)
    sizey = int(1080 * curr_width)

    img = get_img(args["cat_dict"][args["categories"][n]][0], sizex, sizey)

    theme = tkinter.Label(master=args["anim_frame"], background='black', image=img)
    theme.image = img
    theme.place(relx=0.5, rely=0.5, relwidth=curr_width, relheight=curr_width, anchor=customtkinter.CENTER)

    # theme.bind("<Button-1>", lambda x: save_choose(args, args["used"], args["categories"][n]))

    resize_theme(n, theme, args)


def resize_theme(n, theme, args):
    while theme.place_info()['relwidth'] < '1.1':
        prev_width = float(theme.place_info()['relwidth'])
        if prev_width >= 1:
            step = 0.05
            height = 0.08
        elif prev_width >= 0.9:
            step = 0.1
            height = 0.06
        elif prev_width >= 0.8:
            step = 0.1
            height = 0.04
        elif prev_width >= 0.6:
            step = 0.1
            height = 0.02
        else:
            step = 0.2
            height = 0

        curr_width = prev_width + step

        sizex = int(1920 * curr_width)
        sizey = int(1080 * (curr_width + height))

        img = get_img(args["cat_dict"][args["categories"][n]][0], sizex, sizey)

        theme.place(relx=0.5, rely=0.5, relwidth=curr_width, relheight=curr_width, anchor=customtkinter.CENTER)
        theme.configure(image=img)
        theme.image = img

        args["anim_frame"].update()

    else:
        if exists('theme.json'):
            with open('theme.json', "r", encoding='utf-8') as json:
                choose_cat = load(json)['theme']
            save_choose(args, args["used"], choose_cat)
            theme_last_turn(n, args, choose_cat)
        else:
            n += 1
            themes_loop(n, args)


def theme_last_turn(n, args, choose_cat):
    curr_width = 0.4
    sizex = int(1920 * curr_width)
    sizey = int(1080 * curr_width)

    path = args["cat_dict"][choose_cat][1]
    img = get_img(path, sizex, sizey)

    theme = tkinter.Label(master=args["anim_frame"], background='#212325', image=img)
    theme.image = img
    theme.place(relx=0.5, rely=0.5, relwidth=curr_width, relheight=curr_width, anchor=customtkinter.CENTER)

    last_resize(n, theme, path, args)


def last_resize(n, theme, path, args):
    while theme.place_info()['relwidth'] < '1.1':
        prev_width = float(theme.place_info()['relwidth'])
        if prev_width >= 1:
            step = 0.05
            height = 0.08
        elif prev_width >= 0.9:
            step = 0.05
            height = 0.06
        elif prev_width >= 0.8:
            step = 0.05
            height = 0.04
        elif prev_width >= 0.6:
            step = 0.1
            height = 0.02
        else:
            step = 0.2
            height = 0

        curr_width = prev_width + step

        sizex = int(1920 * curr_width)
        sizey = int(1080 * (curr_width + height))

        img = get_img(path, sizex, sizey)

        theme.place(relx=0.5, rely=0.5, relwidth=curr_width, relheight=curr_width, anchor=customtkinter.CENTER)
        theme.configure(image=img)
        theme.image = img

        args["anim_frame"].update()
    else:
        end_animation(args)


def end_animation(args):
    args["anim_frame"].destroy()
    args["top"].destroy()
    args["score_frame"].place(relx=0.5, rely=0.8, relwidth=0.58, relheight=0.4, anchor=customtkinter.CENTER)

