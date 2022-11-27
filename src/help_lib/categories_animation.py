import customtkinter
import tkinter

from os import getenv
from os.path import exists
from help_lib.animation import frame_animation
from help_lib.helper import get_img, save_choose, get_frames


def animate_categories(app, score_frame, frame, cat_dict):
    anim_frame = customtkinter.CTkFrame(master=app, fg_color='#212325')
    anim_frame.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=customtkinter.CENTER)

    img = get_img(getenv('BG_IMAGE'))
    anim_bg = tkinter.Label(master=anim_frame, image=img)
    anim_bg.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=customtkinter.CENTER)
    anim_bg.image = img

    frame_animation(getenv("CIRCLE"), anim_bg, app, (1920, 1080))

    create_top_level(anim_frame, cat_dict)


def create_top_level(anim_frame, cat_dict):
    transparent_color = '#fcfcfc'
    top = customtkinter.CTkToplevel(anim_frame, fg_color=transparent_color)
    top.attributes("-fullscreen", True)
    top.wm_attributes("-transparentcolor", transparent_color)
    top.attributes('-topmost', 'true')

    font_size = 2

    label = customtkinter.CTkLabel(master=top, text='Выбирает категорию\nНИКИТА', text_font=('Helvetica', font_size),
                                   text_color='#ffffff', fg_color=transparent_color, bg_color=transparent_color)
    label.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

    resize_label(label, font_size, anim_frame, cat_dict, top)


def resize_label(label, font_size, anim_frame, cat_dict, top):
    if font_size < 50:
        font_size += 4
        label.configure(text_font=('Helvetica', font_size))

        label.after(50, resize_label, label, font_size, anim_frame, cat_dict, top)
    else:
        move_label_up(label, font_size, anim_frame, cat_dict, top)


def move_label_up(label, font_size, anim_frame, cat_dict, top):
    tempy = float(label.place_info()["rely"])

    if font_size > 30 or tempy != 0.1:
        font_size -= 5
        rely = tempy - 0.1 if tempy != 0.1 else tempy

        label.configure(text_font=('Helvetica', font_size))
        label.place(relx=0.5, rely=rely, anchor=customtkinter.CENTER)

        label.after(50, move_label_up, label, font_size, anim_frame, cat_dict, top)

    else:
        n = 0
        categories = list(cat_dict.keys())
        themes_loop(n, anim_frame, categories, cat_dict, top)


def themes_loop(n, anim_frame, categories, cat_dict, top):
    n = n if n < len(categories) else 0

    curr_width = 0.3

    sizex = int(1920 * curr_width)
    sizey = int(1080 * curr_width)
    print(f'{sizex}x{sizey}')

    img = get_img(cat_dict[categories[n]][0], sizex, sizey)

    theme = tkinter.Label(master=anim_frame, background='black', image=img)
    theme.image = img
    theme.place(relx=0.5, rely=0.5, relwidth=curr_width, relheight=curr_width, anchor=customtkinter.CENTER)

    theme.bind("<Button-1>", lambda x: save_choose(categories[n]))

    resize_theme(n, anim_frame, theme, categories, cat_dict, top)


def resize_theme(n, anim_frame, theme, categories, cat_dict, top):
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
            height = 0
        else:
            step = 0.2
            height = 0

        curr_width = prev_width + step

        sizex = int(1920 * curr_width)
        sizey = int(1080 * (curr_width + height))
        print(f'{sizex}x{sizey}')

        img = get_img(cat_dict[categories[n]][0], sizex, sizey)

        theme.place(relx=0.5, rely=0.5, relwidth=curr_width, relheight=curr_width, anchor=customtkinter.CENTER)
        theme.configure(image=img)
        theme.image = img

        anim_frame.update()

    else:
        if exists('theme.json'):
            theme_last_turn(n, anim_frame, categories, cat_dict, top)
        else:
            n += 1
            print()
            themes_loop(n, anim_frame, categories, cat_dict, top)


def theme_last_turn(n, anim_frame, categories, cat_dict, top):
    curr_width = 0.4

    sizex = int(1920 * curr_width)
    sizey = int(1080 * curr_width)

    path = cat_dict[categories[n]][1]
    img = get_img(path, sizex, sizey)

    theme = tkinter.Label(master=anim_frame, background='#212325', image=img)
    theme.image = img
    theme.place(relx=0.5, rely=0.5, relwidth=curr_width, relheight=curr_width, anchor=customtkinter.CENTER)

    last_resize(n, anim_frame, theme, path, top)


def last_resize(n, anim_frame, theme, path, top):
    while theme.place_info()['relwidth'] < '1':
        prev_width = float(theme.place_info()['relwidth'])
        if prev_width in (0.6, 0.7, 0.8):
            step = 0.1
        elif prev_width >= 0.9:
            step = 0.025
        else:
            step = 0.2

        curr_width = prev_width + step

        sizex = int(1920 * curr_width)
        sizey = int(1080 * curr_width)

        img = get_img(path, sizex, sizey)

        theme.place(relx=0.5, rely=0.5, relwidth=curr_width, relheight=curr_width, anchor=customtkinter.CENTER)
        theme.configure(image=img)
        theme.image = img

        anim_frame.update()

    else:
        end_animation(anim_frame, top)


def end_animation(anim_frame, top):
    anim_frame.destroy()
    top.destroy()

