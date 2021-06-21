import tkinter as tk
from tkinter import messagebox as mb
from tkinter import simpledialog
import sqlite3
import operator
from datetime import datetime


window = tk.Tk()
window.title("UnWatch")
window.iconphoto(False, tk.PhotoImage(file="unwatch.png"))

new_chars = list()  # зашифрованный список
clear_chars = list()  # незашифрованный список

# флажок переключения зашифрованного
# вида текста на незашифрованный
KEY_SYMBOL_SHOW = True

# создание списка с кодами нужных символов, туда включается русский и
# английский алфавит, цифры и основные спец символы
# ! " # $ % & ' ( ) * + , - . / 0 1 2 3 4 5 6 7 8 9 : ; < = > ? @
# A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
correct_symbols = [c for c in range(32, 91)]
# a b c d e f g h i j k l m n o p q r s t u v w x y z { | } ~
correct_symbols.extend(list(range(97, 127)))
# а б в г д е ж з и й к л м н о п р с т у ф х ц ч ш щ ъ ы ь э ю я
correct_symbols.extend(list(range(1072, 1104)))
# А Б В Г Д Е Ж З И Й К Л М Н О П Р С Т У Ф Х Ц Ч Ш Щ Ъ Ы Ь Э Ю Я
correct_symbols.extend(list(range(1040, 1072)))

NOTE_NOT_SAVED = 0
NOTE_SAVED = 1

db = sqlite3.connect("unwatch.db")
cursor = db.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS article(
    title VARCHAR(255),
    body TEXT,
    create_date VARCHAR(255)
)""")


# показать зашифрованный текст
def show_symbols(event=None):
    global KEY_SYMBOL_SHOW
    # Если отображается зашифрованный текст, тогда мы всё удаляем в виджете
    # и добавляем в виджет незашифрованный текст
    # и меняем цвет индикатора Е на красный
    if KEY_SYMBOL_SHOW:
        txt_text.delete("1.0", tk.END)
        txt_text.insert("1.0", "".join(clear_chars))
        lbl_color["bg"] = "red"
        KEY_SYMBOL_SHOW = False
    # Если отображается незашифрованный текст, тогда мы всё удаляем в виджете
    # и добавляем в виджет зашифрованный текст
    # и меняем цвет индикатора Е на зеленый
    else:
        txt_text.delete("1.0", tk.END)
        txt_text.insert("1.0", "".join(new_chars))
        lbl_color["bg"] = "green"
        KEY_SYMBOL_SHOW = True


# обработка удаления последнего симова с обоих списков
# как зашифрованного так и списка в незашифрованном виде
def delete_last_char(event=None):
    global select_all
    lbl_word_count["text"] = f"Слов: {get_count_word(clear_chars)}"
    if select_all:
        txt_text.delete("1.0", tk.END)
        clear_chars.clear()
        new_chars.clear()
        select_all = False
    if clear_chars:
        del clear_chars[-1]
    elif not clear_chars:
        print("Clear chars: None")
    if new_chars:
        del new_chars[-1]
    elif not new_chars:
        print("New chars: None")


# обработка нажатия клавиши <Enter>, мы симовл перехода на новую строку
# в незашифрованный список а в зашифрованный список
# мы добавляем символ шифрования
def enter_key(event=None):
    global select_all
    select_all = False
    # new line
    clear_chars.append("\n")
    # char '#'
    new_chars.append(chr(35))


# Получение количества напечатаных слов
def get_count_word(text_list_symbols):
    count = 0
    for line in "".join(text_list_symbols).splitlines():
        count += len(line.split())
    return count


# Обработка нажатий клавиш <Ctrl + x>, <Ctrl + c>, <Ctrl + v>
# чтобы они работали в нашем виджете
def handle_keypress(event):
    global KEY_SYMBOL_SHOW
    global select_all
    select_all = False
    lbl_word_count["text"] = f"Слов: {get_count_word(clear_chars)}"

    try:
        char_code = ord(event.char)
        # print(event.char)  # отбражает какую клавишу мы нажимали,
        # может быть полезна при тестировании кода
        clear_chars.append(event.char)
        txt_text.state = NOTE_NOT_SAVED
        if lbl_color["bg"] == "red":
            lbl_color["bg"] = "green"
        if char_code in correct_symbols:
            KEY_SYMBOL_SHOW = True
            txt_text.delete("1.0", tk.END)
            new_chars.append(chr(35))
            txt_text.insert("1.0", "".join(new_chars))
            # print(new_chars)  # отображает зашифрованный список
            # print(clear_chars)  # отображает незашифрованный список
    except TypeError:
        ...


def ctrlo(event):
    # print(event.keycode)  # отображает код комбинации с использование Ctrl
    # global select_all
    # select_all = False
    print(txt_text.state)

    if event.keycode == 79:
        show_symbols(event)


select_all = False


def select_all_text(event):
    global select_all
    select_all = True
    txt_text.tag_add(tk.SEL, "1.0", tk.END)

    txt_text.mark_set(tk.INSERT, "1.0")
    txt_text.see(tk.INSERT)
    return 'break'


def set_word_count(event):
    print(get_count_word(clear_chars))


def save_note():
    title = "Сохранить заметку"
    prompt = "Введите название заметки:" + (" " * 42)
    if txt_text.state is NOTE_NOT_SAVED:
        note_name = simpledialog.askstring(title, prompt, parent=window)
        all_text = "".join(clear_chars)
        current_date = datetime.today().strftime("%d.%m.%Y %H:%M")
        print(all_text)
        if note_name:
            print(note_name)
            cursor.execute("INSERT INTO article VALUES(?, ?, ?);",
                           (note_name.strip(), all_text, current_date))
            db.commit()
            txt_text.state = NOTE_SAVED
            txt_text.focus_set()
            print("Заметка сохранена!")
    else:
        print("Запись уже сохранена!")
        txt_text.focus_set()


def show_note():
    print("Открыть файл")
    if txt_text.state == NOTE_NOT_SAVED:
        print("Файл не сохранен")
        answer = mb.askyesno(
            title="Сохранить файл",
            message="Сохранить файл?")
        if answer:
            save_note()
    show_all_notes = tk.Tk()
    cursor.execute("SELECT title, create_date FROM article;")

    listbox_border = tk.Frame(show_all_notes, bd=10,
                              relief="sunken", background="white")
    listbox_border.pack(padx=10, pady=10, fill=None, expand=False)
    # scrollbar = tk.Scrollbar(listbox_border)
    # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    note_list = tk.Listbox(listbox_border, width=100, height=10,
                           borderwidth=0, highlightthickness=0,
                           background=listbox_border.cget("background"))
    vsb = tk.Scrollbar(listbox_border, orient="vertical",
                       command=note_list.yview)
    note_list.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")


    titles = list(map(operator.itemgetter(0, 1), cursor.fetchall()))
    print(titles)
    for i in titles:
        note = i[0] + " #дата: " + i[1]
        note_list.insert(tk.END, note)

    # for i in range(30):
    #     i = ["title", "23.10.1993"]
    #     note = i[0] + " #дата: " + i[1]
    #     note_list.insert(tk.END, note)

    def open_note(event):
        cur_item = note_list.curselection()
        cur_note_title = note_list.get(cur_item).split("#")[0].strip()
        print(cur_note_title)
        cursor.execute("SELECT body FROM article WHERE title='{title}';"
                       .format(title=cur_note_title))
        body_text = cursor.fetchone()[0]
        # print(body_text)
        global new_chars
        global clear_chars
        clear_chars = list(body_text)
        new_chars = list("#" * len(body_text))
        # print(new_chars)
        txt_text.delete("1.0", tk.END)
        txt_text.insert("1.0", "".join(new_chars))
        txt_text.state = NOTE_SAVED
        # lbl_color["bg"] = "green"
        # KEY_SYMBOL_SHOW = True
        show_all_notes.destroy()
        txt_text.focus_set()

    note_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    note_list.bind("<Double-1>", open_note)
    note_list.bind("<Return>", open_note)
    # print(help(note_list.pack_configure))
    show_all_notes.mainloop()


def remove_all_notes():
    answer = mb.askyesno(
        title="Удалить всё",
        message="Удалить все заметки?")
    if answer:
        cursor.execute("DROP TABLE article;")
        cursor.execute("""CREATE TABLE IF NOT EXISTS article(
        title VARCHAR(255),
        body TEXT,
        create_date VARCHAR(255));""")
        db.commit()
        print("База данных пересоздана.")
    else:
        return


def new_note():
    answer = mb.askyesno(
        title="Новая заметка",
        message="Создать новую заметку?")
    if answer:
        if txt_text.state == NOTE_NOT_SAVED:
            print("Файл не сохранен")
            answer = mb.askyesno(
                title="Сохранить файл",
                message="Сохранить файл?")
            if answer:
                save_note()

        global new_chars
        global clear_chars
        new_chars = list()
        clear_chars = list()
        txt_text.delete("1.0", tk.END)
    else:
        return


my_font_style = ('Georgia', 13)
txt_text = tk.Text(font=my_font_style, wrap=tk.WORD)
txt_text.bind("<BackSpace>", delete_last_char)

# обработка нажатия клавиши энтер
txt_text.bind("<Return>", enter_key)
txt_text.bind("<Key>", handle_keypress)
txt_text.bind("<Control-KeyPress>", ctrlo)
txt_text.state = NOTE_NOT_SAVED
txt_text.pack(fill=tk.BOTH, expand=True)

menu = tk.Menu(window)
window.config(menu=menu)
menu_file = tk.Menu(menu, tearoff=0)
menu_file.add_command(label="Новая заметка", command=new_note)
menu_file.add_command(label="Открыть", command=show_note)
menu_file.add_command(label="Сохранить не в файл", command=save_note)
menu_file.add_command(label="Сохранить в файл")
menu_file.add_command(label="Удалить все заметки",
                      command=remove_all_notes)
menu_file.add_command(label="Настройки")

menu.add_cascade(label="Файл", menu=menu_file)

menu_help = tk.Menu(menu, tearoff=0)
menu_help.add_command(label="Помощь")
menu_help.add_command(label="О программе")

menu.add_cascade(label="Справка", menu=menu_help)

frm_down = tk.Frame(master=window, bg="black")
frm_down.pack(fill=tk.X)
lbl_color = tk.Label(text="E", bg="green", master=frm_down, width="4")
lbl_color.pack(side=tk.RIGHT, padx=10)

lbl_word_count = tk.Label(text="Слов: 0", fg="white", bg="black",
                          master=frm_down)
lbl_word_count.pack()

window.mainloop()
