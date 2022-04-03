import os
import sys
import win32api
from datetime import datetime
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

WORK_PATH = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))


def quit():
    answer = messagebox.askokcancel(title="Выход", message='Закрыть программу?')
    if answer:
        root.destroy()


def select_dir():
    dir_path = filedialog.askdirectory()
    entry_field.delete(0, END)
    entry_field.insert(0, dir_path)


def start_sorting():
    cur_path = entry_field.get()
    if cur_path:
        for folder, subfolders, files in os.walk(cur_path):
            for file in files:
                if file.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                    filepath = os.path.join(folder, file)
                    modification_time = os.path.getmtime(filepath)
                    date = datetime.fromtimestamp(modification_time)
                    date = date.strftime("%Y-%m-%d")
                    date_folder = os.path.join(cur_path, date)
                    if not os.path.exists(date_folder):
                        os.mkdir(date_folder)
                    file_attrs = win32api.GetFileAttributes(os.path.join(folder, file))
                    if file_attrs == 32:
                        os.rename(filepath, os.path.join(date_folder, file))
                    elif file_attrs == 33:
                        messagebox.showerror('Error!', f'Файл {file} защищён от записи')
        messagebox.showinfo('Success', 'Сортировка выполнена успешно')
        entry_field.delete(0, END)
    else:
        messagebox.showwarning('Warning', 'Выберите папку с фотографиями')


if __name__ == '__main__':
    root = Tk()
    root.protocol("WM_DELETE_WINDOW", quit)
    root.title('PhotoSort')
    root.geometry("500x150+600+300")
    iconbit = os.path.join(WORK_PATH, 'pic.ico')
    root.iconbitmap(iconbit)

    style = ttk.Style()
    style.configure('my.TButton', font=("Helvetica", 15))

    frame = Frame(root, bg="#56ADFF", bd=5)
    frame.pack(pady=10, padx=10, fill=X)

    entry_field = ttk.Entry(frame)
    entry_field.pack(side=LEFT, ipady=2, expand=True, fill=X)

    btn_dialog = ttk.Button(frame, text="Выбрать папку", command=select_dir)
    btn_dialog.pack(side=LEFT, padx=5)

    btn_start = ttk.Button(root, text="Start", style="my.TButton", command=start_sorting)
    btn_start.pack(fill=X, padx=10)

    root.mainloop()
