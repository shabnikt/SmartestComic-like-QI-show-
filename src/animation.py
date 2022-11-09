import customtkinter
import tkinter
from PIL import Image, ImageTk
import os
import json

with open("config.json", "r", encoding='utf-8') as json_mapping:
    categories = json.load(json_mapping)["categories"]


def animation(app, score_frame, frame):
    score_frame.place_forget()
    frame.place_forget()
    circle_img = Image.open(os.getenv('CIRCLE'))
    w = 0.04
    size = int(1080 * w)
    circle_img = circle_img.resize((size, size), Image.Resampling.LANCZOS)
    img = ImageTk.PhotoImage(circle_img)
    bglab = tkinter.Label(master=app, background='#212325', image=img)
    bglab.image = img
    bglab.place(relx=0.5, rely=0.5, relwidth=w, relheight=w, anchor=customtkinter.CENTER)
    print(bglab.place_info()['relwidth'])

    circle(app, bglab, score_frame, frame)


def circle(app, bglab, score_frame, frame):
    if bglab.place_info()['relwidth'] < '3':
        w = float(bglab.place_info()['relwidth']) + 0.38
        circle_img = Image.open(os.getenv('CIRCLE'))
        size = int(1080 * w)
        circle_img = circle_img.resize((size, size), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(circle_img)
        bglab.place(relx=0.5, rely=0.5, relwidth=w, relheight=w, anchor=customtkinter.CENTER)
        bglab.configure(image=img)
        bglab.image = img
        print(bglab.place_info()['relwidth'])
        bglab.after(16, circle, app, bglab, score_frame, frame)
    else:
        print(f"now: {bglab.place_info()['relwidth']}")
        choose_cat(app)


def choose_cat(app):
    top = customtkinter.CTkToplevel(app, fg_color='#b71111')
    top.attributes("-fullscreen", True)
    top.wm_attributes("-transparentcolor", "#b71111")
    size = 2
    lab = customtkinter.CTkLabel(master=top, text='Выбирает категорию\nНИКИТА', text_font=('Helvetica', size),
                                 text_color='#c90f0f', fg_color='#b71111', bg_color='#b71111')
    lab.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

    move_lab(lab, size, app)


def move_lab(lab, size, app):
    if size < 50:
        print(size)
        size += 4
        print(size)
        print()
        lab.configure(text_font=('Helvetica', size))
        lab.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
        lab.after(50, move_lab, lab, size, app)
    else:
        move_up(lab, size, app)


def move_up(lab, size, app):
    if size > 30 or float(lab.place_info()["rely"]) != 0.1:
        size -= 5
        if float(lab.place_info()["rely"])  != 0.1:
            rely = float(lab.place_info()["rely"]) - 0.1
        else:
            rely = float(lab.place_info()["rely"])
        print(rely)
        lab.configure(text_font=('Helvetica', size))
        lab.place(relx=0.5, rely=rely, anchor=customtkinter.CENTER)
        lab.after(50, move_up, lab, size, app)

    else:
        n = 0
        move_theme(n, app)


def move_theme(n, app):
    n = n if n < len(categories) else 0
    circle_img = Image.open(categories[n])
    w = 0.3
    blackx = 0.4
    blacky = (1920 * (blackx - w) / 1080) + w
    sizex = int(1920 * w)
    sizey = int(1080 * w)
    circle_img = circle_img.resize((sizex, sizey), Image.Resampling.LANCZOS)
    img = ImageTk.PhotoImage(circle_img)

    border = tkinter.Label(master=app, background='red')
    border.place(relx=0.5, rely=0.5, relwidth=blackx, relheight=blacky, anchor=customtkinter.CENTER)

    cat1 = tkinter.Label(master=app, background='#212325', image=img)
    cat1.place(relx=0.5, rely=0.5, relwidth=w, relheight=w, anchor=customtkinter.CENTER)
    cat1.configure(image=img)
    cat1.image = img

    theme_loop(n, app, cat1, border)


def theme_loop(n, app, cat1, border):
    if cat1.place_info()['relwidth'] < '1':
        w = float(cat1.place_info()['relwidth']) + 0.1
        t_v = float(border.place_info()['relwidth'])
        blackx = t_v + 0.1 if t_v < 1 else 1
        blacky = (1920 * (blackx - w) / 1080) + w
        circle_img = Image.open(categories[n])
        sizex = int(1920 * w)
        sizey = int(1080 * w)
        circle_img = circle_img.resize((sizex, sizey), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(circle_img)

        border.place(relx=0.5, rely=0.5, relwidth=blackx, relheight=blacky, anchor=customtkinter.CENTER)

        cat1.place(relx=0.5, rely=0.5, relwidth=w, relheight=w, anchor=customtkinter.CENTER)
        cat1.configure(image=img)
        cat1.image = img
        print(cat1.place_info()['relwidth'])
        cat1.after(1000, theme_loop, n, app, cat1, border)
    else:
        n += 1

        move_theme(n, app)








#app.after(1000, animend, bglab, score_frame, frame)
def animend(lab, score_frame, frame):
    score_frame.place(rely=0.6, relwidth=1, relheight=0.4)
    frame.place(relwidth=1, relheight=0.4)
    lab.destroy()

