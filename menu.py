import tkinter as tk


class MenuBar(tk.Menu):
    def __init__(self, window, article):
        self.menu = tk.Menu(window)
        window.config(menu=self.menu)
        self.menu_file = tk.Menu(self.menu, tearoff=0)
        self.menu_file.add_command(label="Новая заметка", command=article.new_note)
        # self.menu_file.add_command(label="Новая заметка")
        self.menu_file.add_command(label="Открыть", command=article.show_note)
        # self.menu_file.add_command(label="Открыть")
        self.menu_file.add_command(label="Сохранить", command=article.save_note)
        # self.menu_file.add_command(label="Сохранить")
        self.menu_file.add_command(label="Удалить все заметки",
                              command=article.remove_all_notes)
        # self.menu_file.add_command(label="Удалить все заметки")
        self.menu_file.add_command(label="Настройки")

        self.menu.add_cascade(label="Файл", menu=self.menu_file)

        self.menu_help = tk.Menu(self.menu, tearoff=0)
        self.menu_help.add_command(label="Помощь")
        self.menu_help.add_command(label="О программе")

        self.menu.add_cascade(label="Справка", menu=self.menu_help)