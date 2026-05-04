import tkinter as tk

# from tkinter import messagebox  # раскомментируй, когда добавишь окна с результатами

window = tk.Tk()
window.title('Крестики-нолики')
window.geometry('300x350')

current_player = 'X'
buttons = []  # двумерный список: buttons[row][col]


def on_click(row, col):
    global current_player
    btn = buttons[row][col]

    # Не даём перезаписать занятую клетку
    if btn["text"] != "":
        return

    # Ставим знак текущего игрока
    btn.config(text=current_player)

    # Переключаем игрока
    current_player = 'O' if current_player == 'X' else 'X'
    window.title(f'Крестики-нолики | Ход: {current_player}')


for i in range(3):
    row = []
    for j in range(3):
        btn = tk.Button(
            window,
            text="",
            font=("Arial", 20),
            width=5,
            height=2,
            command=lambda r=i, c=j: on_click(r, c)
        )
        btn.grid(row=i, column=j)
        row.append(btn)
    buttons.append(row)

window.mainloop()