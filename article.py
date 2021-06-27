import operator
import sqlite3
from datetime import datetime
from tkinter import messagebox as mb
from tkinter import simpledialog
import tkinter as tk


class NoteList(tk.Tk):
    def __init__(self, article, window):
        super().__init__()
        self.article = article
        self.window = window

        self.article.cursor.execute("SELECT title, create_date FROM article;")

        listbox_border = tk.Frame(self, bd=10,
                                  relief="sunken", background="white")
        listbox_border.pack(padx=10, pady=10, fill=None, expand=False)
        note_list = tk.Listbox(listbox_border, width=100, height=10,
                               borderwidth=0, highlightthickness=0,
                               background=listbox_border.cget("background"))
        vsb = tk.Scrollbar(listbox_border, orient="vertical",
                           command=note_list.yview)
        note_list.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")

        titles = list(map(operator.itemgetter(0, 1), self.article.cursor.fetchall()))
        print(titles)
        for i in titles:
            note = i[0] + " #дата: " + i[1]
            note_list.insert('end', note)

        def open_note(event):
            cur_item = note_list.curselection()
            cur_note_title = note_list.get(cur_item).split("#")[0].strip()
            print(cur_note_title)
            self.article.cursor.execute("SELECT body FROM article WHERE title='{title}';"
                                        .format(title=cur_note_title))
            body_text = self.article.cursor.fetchone()[0]
            print(body_text)
            self.article.clear_chars = list(body_text)
            self.article.new_chars = list(self.article.SECRET_SYMBOL * len(body_text))
            self.article.txt_text.delete("1.0", 'end')
            self.article.txt_text.insert("1.0", "".join(self.article.new_chars))
            self.article.txt_text.state = self.article.NOTE_SAVED
            self.destroy()
            self.article.txt_text.focus_set()

        note_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        note_list.bind("<Double-1>", open_note)
        note_list.bind("<Return>", open_note)


class Article:
    def __init__(self, window, txt_text, frm_down, lbl_color, lbl_word_count):
        self.window = window
        self.txt_text = txt_text
        self.frm_down = frm_down
        self.lbl_color = lbl_color
        self.lbl_word_count = lbl_word_count

    new_chars = list()  # зашифрованный список
    clear_chars = list()  # незашифрованный список

    # флажок переключения зашифрованного
    # вида текста на незашифрованный
    KEY_SYMBOL_SHOW = True
    # Геральдическая лилия
    SECRET_SYMBOL = "\u269C"

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
    def show_symbols(self, event=None):
        # global KEY_SYMBOL_SHOW
        # Если отображается зашифрованный текст, тогда мы всё удаляем в виджете
        # и добавляем в виджет незашифрованный текст
        # и меняем цвет индикатора Е на красный
        if self.KEY_SYMBOL_SHOW:
            self.txt_text.delete("1.0", 'end')
            self.txt_text.insert("1.0", "".join(self.clear_chars))
            self.lbl_color["bg"] = "red"
            self.KEY_SYMBOL_SHOW = False
        # Если отображается незашифрованный текст, тогда мы всё удаляем в виджете
        # и добавляем в виджет зашифрованный текст
        # и меняем цвет индикатора Е на зеленый
        else:
            self.txt_text.delete("1.0", 'end')
            self.txt_text.insert("1.0", "".join(self.new_chars))
            self.lbl_color["bg"] = "green"
            self.KEY_SYMBOL_SHOW = True

    # обработка удаления последнего симова с обоих списков
    # как зашифрованного так и списка в незашифрованном виде
    def delete_last_char(self, event=None):
        # global select_all
        self.lbl_word_count["text"] = f"Слов: {self.get_count_word(self.clear_chars)}"
        if self.select_all:
            self.txt_text.delete("1.0", 'end')
            self.clear_chars.clear()
            self.new_chars.clear()
            self.select_all = False
        if self.clear_chars:
            del self.clear_chars[-1]
        elif not self.clear_chars:
            print("Clear chars: None")
        if self.new_chars:
            del self.new_chars[-1]
        elif not self.new_chars:
            print("New chars: None")

    # обработка нажатия клавиши <Enter>, мы симовл перехода на новую строку
    # в незашифрованный список а в зашифрованный список
    # мы добавляем символ шифрования
    def enter_key(self, event=None):
        # global select_all
        self.select_all = False
        # new line
        self.clear_chars.append("\n")
        # char '#'
        # new_chars.append(chr(35))
        self.new_chars.append(self.SECRET_SYMBOL)

    # Получение количества напечатаных слов
    def get_count_word(self, text_list_symbols):
        count = 0
        for line in "".join(text_list_symbols).splitlines():
            count += len(line.split())
        return count

    # Обработка нажатий клавиш <Ctrl + x>, <Ctrl + c>, <Ctrl + v>
    # чтобы они работали в нашем виджете
    def handle_keypress(self, event):
        self.select_all = False
        self.lbl_word_count["text"] = f"Слов: {self.get_count_word(self.clear_chars)}"

        try:
            char_code = ord(event.char)
            # print(event.char)  # отбражает какую клавишу мы нажимали,
            # может быть полезна при тестировании кода
            self.clear_chars.append(event.char)
            self.txt_text.state = self.NOTE_NOT_SAVED
            if self.lbl_color["bg"] == "red":
                self.lbl_color["bg"] = "green"
            if char_code in self.correct_symbols:
                self.KEY_SYMBOL_SHOW = True
                self.txt_text.delete("1.0", 'end')
                self.new_chars.append(self.SECRET_SYMBOL)
                self.txt_text.insert("1.0", "".join(self.new_chars))
        except TypeError:
            ...

    def ctrlo(self, event):
        # print(event.keycode)  # отображает код комбинации с использование Ctrl
        print(self.txt_text.state)

        if event.keycode == 79:
            self.show_symbols(event)

    select_all = False

    def select_all_text(self, event):
        global select_all
        select_all = True
        self.txt_text.tag_add('sel', "1.0", 'end')

        self.txt_text.mark_set('insert', "1.0")
        self.txt_text.see('insert')
        return 'break'

    def set_word_count(self, event):
        print(self.get_count_word(self.clear_chars))

    def save_note(self):
        title = "Сохранить заметку"
        prompt = "Введите название заметки:" + (" " * 42)
        if self.txt_text.state is self.NOTE_NOT_SAVED:
            note_name = simpledialog.askstring(title, prompt, parent=self.window)
            all_text = "".join(self.clear_chars)
            current_date = datetime.today().strftime("%d.%m.%Y %H:%M")
            print(all_text)
            if note_name:
                print(note_name)
                self.cursor.execute("INSERT INTO article VALUES(?, ?, ?);",
                                    (note_name.strip(), all_text, current_date))
                self.db.commit()
                self.txt_text.state = self.NOTE_SAVED
                self.txt_text.focus_set()
                print("Заметка сохранена!")
        else:
            print("Запись уже сохранена!")
            self.txt_text.focus_set()

    def show_note(self):
        print("Открыть файл")
        if self.txt_text.state == self.NOTE_NOT_SAVED and len(self.txt_text.get("1.0", 'end')) > 3:
            print("Файл не сохранен")
            answer = mb.askyesno(
                title="Сохранить файл",
                message="Сохранить файл?")
            if answer:
                self.save_note()
        show_all_notes = NoteList(self, window=self.window)
        show_all_notes.mainloop()

    def remove_all_notes(self):
        answer = mb.askyesno(
            title="Удалить всё",
            message="Удалить все заметки?")
        if answer:
            self.cursor.execute("DROP TABLE article;")
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS article(
            title VARCHAR(255),
            body TEXT,
            create_date VARCHAR(255));""")
            self.db.commit()
            print("База данных пересоздана.")
        else:
            return

    def new_note(self):
        answer = mb.askyesno(
            title="Новая заметка",
            message="Создать новую заметку?")
        if answer:
            if self.txt_text.state == self.NOTE_NOT_SAVED:
                print("Файл не сохранен")
                answer = mb.askyesno(
                    title="Сохранить файл",
                    message="Сохранить файл?")
                if answer:
                    self.save_note()

            self.new_chars = list()
            self.clear_chars = list()
            self.txt_text.delete("1.0", 'end')
        else:
            return
