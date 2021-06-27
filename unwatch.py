import tkinter as tk

import os
import pathlib

from article import Article
from menu import MenuBar


class Window(tk.Tk):
    ICON_FILE_NAME = "unwatch.ico"

    def __init__(self):
        super().__init__()
        self.title("UnWatch")
        self.iconbitmap(pathlib.Path().cwd().__str__() + "/" + self.ICON_FILE_NAME)

        my_font_style = ('Georgia', 13)
        txt_text = tk.Text(font=my_font_style, wrap=tk.WORD)
        frm_down = tk.Frame(master=self, bg="black")
        lbl_color = tk.Label(text="E", bg="green", master=frm_down, width="4")
        lbl_word_count = tk.Label(text="Слов: 0", fg="white", bg="black",
                                  master=frm_down)
        article = Article(self, txt_text, frm_down, lbl_color, lbl_word_count)
        MenuBar(window=self, article=article)
        txt_text.bind("<BackSpace>", article.delete_last_char)
        # tk.END

        # обработка нажатия клавиши энтер
        txt_text.bind("<Return>", article.enter_key)
        txt_text.bind("<Key>", article.handle_keypress)
        txt_text.bind("<Control-KeyPress>", article.ctrlo)
        txt_text.state = article.NOTE_NOT_SAVED
        txt_text.pack(fill=tk.BOTH, expand=True)
        # menu = tk.Menu(self)
        # self.config(menu=menu)
        # menu_file = tk.Menu(menu, tearoff=0)
        # menu_file.add_command(label="Новая заметка", command=new_note)
        # menu_file.add_command(label="Открыть", command=show_note)
        # menu_file.add_command(label="Сохранить", command=save_note)
        # menu_file.add_command(label="Удалить все заметки",
        #                       command=remove_all_notes)
        # menu_file.add_command(label="Настройки")

        # menu.add_cascade(label="Файл", menu=menu_file)

        # menu_help = tk.Menu(menu, tearoff=0)
        # menu_help.add_command(label="Помощь")
        # menu_help.add_command(label="О программе")

        # menu.add_cascade(label="Справка", menu=menu_help)


        frm_down.pack(fill=tk.X)

        lbl_color.pack(side=tk.RIGHT, padx=10)


        lbl_word_count.pack()


if __name__ == "__main__":
    window = Window()

    window.mainloop()