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

    frame_animation(anim_bg,
                    lambda: create_top_level(anim_frame, cat_dict),
                    get_frames(getenv("CIRCLE")))


def create_top_level(anim_frame, cat_dict):
    transparent_color = '#b71111'
    top = customtkinter.CTkToplevel(anim_frame, fg_color=transparent_color)
    top.attributes("-fullscreen", True)
    top.wm_attributes("-transparentcolor", transparent_color)
    top.attributes('-topmost', 'true')

    font_size = 2

    label = customtkinter.CTkLabel(master=top, text='Выбирает категорию\nНИКИТА', text_font=('Helvetica', font_size),
                                   text_color='#c90f0f', fg_color=transparent_color, bg_color=transparent_color)
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
    blackx = 0.4
    blacky = (1920 * (blackx - curr_width) / 1080) + curr_width

    sizex = int(1920 * curr_width)
    sizey = int(1080 * curr_width)

    img = get_img(cat_dict[categories[n]][0], sizex, sizey)

    border = tkinter.Label(master=anim_frame, background='red')
    border.place(relx=0.5, rely=0.5, relwidth=blackx, relheight=blacky, anchor=customtkinter.CENTER)

    theme = tkinter.Label(master=anim_frame, background='#212325', image=img)
    theme.image = img
    theme.place(relx=0.5, rely=0.5, relwidth=curr_width, relheight=curr_width, anchor=customtkinter.CENTER)

    theme.bind("<Button-1>", lambda x: save_choose(categories[n]))

    resize_theme(n, anim_frame, theme, border, categories, cat_dict, top)


def resize_theme(n, anim_frame, theme, border, categories, cat_dict, top):
    if theme.place_info()['relwidth'] < '1':
        curr_width = float(theme.place_info()['relwidth']) + 0.1
        border_width = float(border.place_info()['relwidth'])

        blackx = border_width + 0.1 if border_width < 1 else 1
        blacky = (1920 * (blackx - curr_width) / 1080) + curr_width

        sizex = int(1920 * curr_width)
        sizey = int(1080 * curr_width)

        img = get_img(cat_dict[categories[n]][0], sizex, sizey)

        border.place(relx=0.5, rely=0.5, relwidth=blackx, relheight=blacky, anchor=customtkinter.CENTER)

        theme.place(relx=0.5, rely=0.5, relwidth=curr_width, relheight=curr_width, anchor=customtkinter.CENTER)
        theme.configure(image=img)
        theme.image = img

        theme.after(1000, resize_theme, n, anim_frame, theme, border, categories, cat_dict, top)
    else:
        if exists('theme.json'):
            theme_last_turn(n, anim_frame, categories, cat_dict, top)
        else:
            n += 1
            themes_loop(n, anim_frame, categories, cat_dict, top)


def theme_last_turn(n, anim_frame, categories, cat_dict, top):
    curr_width = 0.3
    blackx = 0.4
    blacky = (1920 * (blackx - curr_width) / 1080) + curr_width

    sizex = int(1920 * curr_width)
    sizey = int(1080 * curr_width)

    path = cat_dict[categories[n]][1]
    img = get_img(path, sizex, sizey)

    border = tkinter.Label(master=anim_frame, background='red')
    border.place(relx=0.5, rely=0.5, relwidth=blackx, relheight=blacky, anchor=customtkinter.CENTER)

    theme = tkinter.Label(master=anim_frame, background='#212325', image=img)
    theme.image = img
    theme.place(relx=0.5, rely=0.5, relwidth=curr_width, relheight=curr_width, anchor=customtkinter.CENTER)

    last_resize(n, anim_frame, theme, border, path, top)


def last_resize(n, anim_frame, theme, border, path, top):
    if theme.place_info()['relwidth'] < '1':
        curr_width = float(theme.place_info()['relwidth']) + 0.1
        border_width = float(border.place_info()['relwidth'])

        blackx = border_width + 0.1 if border_width < 1 else 1
        blacky = (1920 * (blackx - curr_width) / 1080) + curr_width

        sizex = int(1920 * curr_width)
        sizey = int(1080 * curr_width)

        img = get_img(path, sizex, sizey)

        border.place(relx=0.5, rely=0.5, relwidth=blackx, relheight=blacky, anchor=customtkinter.CENTER)

        theme.place(relx=0.5, rely=0.5, relwidth=curr_width, relheight=curr_width, anchor=customtkinter.CENTER)
        theme.configure(image=img)
        theme.image = img

        theme.after(1000, last_resize, n, anim_frame, theme, border, path, top)
    else:
        end_animation(anim_frame, top)


def end_animation(anim_frame, top):
    anim_frame.destroy()
    top.destroy()

