import customtkinter
import tkinter
from PIL import Image, ImageTk
from os import getenv
from os.path import exists
from json import dump


def save_choose(theme):
    print(theme)
    with open('theme.json', 'w') as json_file:
        dump({"theme": theme}, json_file)


def get_img(path, sizex, sizey):
    circle_img = Image.open(path)
    circle_img = circle_img.resize((sizex, sizey), Image.Resampling.LANCZOS)
    img = ImageTk.PhotoImage(circle_img)
    return img


def start_cat_anim(app, score_frame, frame, cat_dict):
    anim_frame = customtkinter.CTkFrame(master=app, fg_color='#212325')
    anim_frame.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=customtkinter.CENTER)

    curr_width = 0.04
    size = int(1080 * curr_width)

    img = get_img(getenv('CIRCLE'), size, size)

    bglab = tkinter.Label(master=anim_frame, background='#212325', image=img)
    bglab.image = img
    bglab.place(relx=0.5, rely=0.5, relwidth=curr_width, relheight=curr_width, anchor=customtkinter.CENTER)

    resize_circle(anim_frame, bglab, score_frame, frame, cat_dict)


def resize_circle(anim_frame, bglab, score_frame, frame, cat_dict):
    if bglab.place_info()['relwidth'] < '3':
        curr_width = float(bglab.place_info()['relwidth']) + 0.38
        size = int(1080 * curr_width)

        img = get_img(getenv('CIRCLE'), size, size)

        bglab.place(relx=0.5, rely=0.5, relwidth=curr_width, relheight=curr_width, anchor=customtkinter.CENTER)
        bglab.configure(image=img)
        bglab.image = img

        bglab.after(16, resize_circle, anim_frame, bglab, score_frame, frame, cat_dict)
    else:
        pass
        create_top_label(anim_frame, cat_dict)


def create_top_label(anim_frame, cat_dict):
    transparent_color = '#b71111'
    top = customtkinter.CTkToplevel(anim_frame, fg_color=transparent_color)
    top.attributes("-fullscreen", True)
    top.wm_attributes("-transparentcolor", transparent_color)
    top.attributes('-topmost', 'true')

    font_size = 2

    choose_button = customtkinter.CTkButton(master=top, bg_color=transparent_color, fg_color=transparent_color,
                                            hover_color=transparent_color, text_font=('Helvetica', 180),
                                            text_color='red', text='push push push\npush push push\npush push push')
    label = customtkinter.CTkLabel(master=top, text='Выбирает категорию\nНИКИТА', text_font=('Helvetica', font_size),
                                   text_color='#c90f0f', fg_color=transparent_color, bg_color=transparent_color)
    label.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

    resize_label(label, font_size, anim_frame, cat_dict, top, choose_button)


def resize_label(label, font_size, anim_frame, cat_dict, top, choose_button):
    if font_size < 50:
        font_size += 4
        label.configure(text_font=('Helvetica', font_size))

        label.after(50, resize_label, label, font_size, anim_frame, cat_dict, top, choose_button)
    else:
        move_label_up(label, font_size, anim_frame, cat_dict, top, choose_button)


def move_label_up(label, font_size, anim_frame, cat_dict, top, choose_button):
    tempy = float(label.place_info()["rely"])

    if font_size > 30 or tempy != 0.1:
        font_size -= 5
        rely = tempy - 0.1 if tempy != 0.1 else tempy

        label.configure(text_font=('Helvetica', font_size))
        label.place(relx=0.5, rely=rely, anchor=customtkinter.CENTER)

        label.after(50, move_label_up, label, font_size, anim_frame, cat_dict, top, choose_button)

    else:
        choose_button.place(relx=0.5, rely=0.6, relwidth=1, relheight=0.8, anchor=customtkinter.CENTER)

        n = 0
        categories = list(cat_dict.keys())
        themes_loop(n, anim_frame, categories, cat_dict, top, choose_button)


def themes_loop(n, anim_frame, categories, cat_dict, top, choose_button):
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

    choose_button.configure(command=lambda: save_choose(categories[n]))

    resize_theme(n, anim_frame, theme, border, categories, cat_dict, top, choose_button)


def resize_theme(n, anim_frame, theme, border, categories, cat_dict, top, choose_button):
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

        theme.after(1000, resize_theme, n, anim_frame, theme, border, categories, cat_dict, top, choose_button)
    else:
        if exists('theme.json'):
            theme_last_turn(n, anim_frame, categories, cat_dict, top, choose_button)
        else:
            n += 1
            themes_loop(n, anim_frame, categories, cat_dict, top, choose_button)


def theme_last_turn(n, anim_frame, categories, cat_dict, top, choose_button):
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

    choose_button.configure(command=lambda: save_choose(categories[n]))

    last_resize(n, anim_frame, theme, border, path, top, choose_button)


def last_resize(n, anim_frame, theme, border, path, top, choose_button):
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

        theme.after(1000, last_resize, n, anim_frame, theme, border, path, top, choose_button)
    else:
        end_animation(anim_frame, top)


def end_animation(anim_frame, top):
    anim_frame.destroy()
    top.destroy()
