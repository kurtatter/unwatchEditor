import tkinter as tk


window = tk.Tk()

new_chars = list()  # зашифрованный список
clear_chars = list()  # незашифрованный список
KEY_SYMBOL_SHOW = True  # флажок переключения зашифрованного вида текста на незашифрованный

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
# в незашифрованный список а в зашифрованный список мы добавляем символ шифрования
def enter_key(event=None):
    global select_all
    select_all = False
    clear_chars.append("\n") # new line
    new_chars.append(chr(35)) # char '#'


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
        # print(event.char)  # отбражает какую клавишу мы нажимали, может быть полезна при тестировании кода
        clear_chars.append(event.char)
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


txt_text = tk.Text(font = ('Georgia' , 13), wrap=tk.WORD)
txt_text.bind("<BackSpace>", delete_last_char)

# обработка нажатия клавиши энтер
txt_text.bind("<Return>", enter_key)
txt_text.bind("<Key>", handle_keypress)
txt_text.bind("<Control-KeyPress>",ctrlo)

txt_text.pack(fill=tk.BOTH, expand=True)

menu = tk.Menu(window)
window.config(menu=menu)
menu_file = tk.Menu(menu, tearoff=0)
menu_file.add_command(label="Открыть")
menu_file.add_command(label="Сохранить")
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

lbl_word_count = tk.Label(text="Слов: 0", fg="white", bg="black", master=frm_down)
lbl_word_count.pack()

window.mainloop()
