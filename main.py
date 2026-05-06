import tkinter as tk

# from tkinter import messagebox  # раскомментируй, когда добавишь окна с результатами
import tkinter as tk
from tkinter import messagebox


class TicTacToeApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Крестики-нолики | Матч до 3 побед")
        self.root.geometry("440x620")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a2e")

        # 🎯 Настройки матча
        self.MATCH_TARGET = 3
        self.scores = {"X": 0, "O": 0}
        self.current_player = "X"
        self.game_active = True
        self.match_over = False
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        self._setup_ui()
        self._reset_round()

    def _setup_ui(self):
        # Заголовок
        tk.Label(self.root, text="КРЕСТИКИ-НОЛИКИ", font=("Arial", 22, "bold"),
                 bg="#1a1a2e", fg="#e94560").pack(pady=(20, 5))

        # Выбор стороны
        choice_frame = tk.Frame(self.root, bg="#16213e")
        choice_frame.pack(pady=10, padx=20, fill="x")
        tk.Label(choice_frame, text="Вы играете за:", bg="#16213e", fg="white", font=("Arial", 11)).pack(side="left",
                                                                                                         padx=5)

        self.player_var = tk.StringVar(value="X")
        tk.Radiobutton(choice_frame, text="X", variable=self.player_var, value="X", bg="#16213e", fg="white",
                       selectcolor="#0f3460", font=("Arial", 10), command=self._on_player_change).pack(side="left",
                                                                                                       padx=2)
        tk.Radiobutton(choice_frame, text="O", variable=self.player_var, value="O", bg="#16213e", fg="white",
                       selectcolor="#0f3460", font=("Arial", 10), command=self._on_player_change).pack(side="left")

        # Счёт
        score_frame = tk.Frame(self.root, bg="#1a1a2e")
        score_frame.pack(pady=10)
        self.lbl_x = tk.Label(score_frame, text="X: 0", font=("Arial", 18, "bold"), fg="#e94560", bg="#1a1a2e")
        self.lbl_x.pack(side="left", padx=30)
        self.lbl_o = tk.Label(score_frame, text="O: 0", font=("Arial", 18, "bold"), fg="#4da8da", bg="#1a1a2e")
        self.lbl_o.pack(side="right", padx=30)

        # Статус
        self.lbl_status = tk.Label(self.root, text="Ход: X", font=("Arial", 14), bg="#1a1a2e", fg="#ecf0f1")
        self.lbl_status.pack(pady=5)

        # Поле 3x3
        board_frame = tk.Frame(self.root, bg="#1a1a2e")
        board_frame.pack(pady=10)
        for i in range(3):
            for j in range(3):
                btn = tk.Button(board_frame, text="", font=("Arial", 32, "bold"), width=4, height=2,
                                bg="#2d2d44", fg="white", relief="flat", activebackground="#3a3a5a",
                                command=lambda r=i, c=j: self._on_click(r, c))
                btn.grid(row=i, column=j, padx=6, pady=6)
                self.buttons[i][j] = btn

        # Кнопки управления
        ctrl_frame = tk.Frame(self.root, bg="#1a1a2e")
        ctrl_frame.pack(pady=15)
        tk.Button(ctrl_frame, text="🔄 Сбросить поле", bg="#0f3460", fg="white", font=("Arial", 11, "bold"),
                  command=self._reset_round).pack(side="left", padx=10)
        tk.Button(ctrl_frame, text="🏆 Новый матч", bg="#e94560", fg="white", font=("Arial", 11, "bold"),
                  command=self._start_new_match).pack(side="left", padx=10)

    def _on_player_change(self):
        """Обновляет стартового игрока при смене выбора"""
        if self.game_active and not self.match_over:
            self.current_player = self.player_var.get()
            self.lbl_status.config(text=f"Ход: {self.current_player}")

    def _start_new_match(self):
        """Полный сброс: счёт, поле, состояние матча"""
        self.scores = {"X": 0, "O": 0}
        self.match_over = False
        self._reset_round()
        self._update_scoreboard()
        self.lbl_status.config(text="Матч начат! Ход: X")

    def _reset_round(self):
        """Сброс только поля (сохраняет счёт матча)"""
        if self.match_over:
            self.match_over = False
        self.game_active = True
        self.current_player = self.player_var.get()
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", bg="#2d2d44", state="normal", fg="white")
        self.lbl_status.config(text=f"Ход: {self.current_player}")

    def _on_click(self, row, col):
        if not self.game_active or self.match_over:
            return

        btn = self.buttons[row][col]
        if btn["text"] != "":
            return  # Клетка занята

        # Делаем ход
        color = "#e94560" if self.current_player == "X" else "#4da8da"
        btn.config(text=self.current_player, fg=color)

        # Проверка победы
        winner = self._check_winner()
        if winner:
            self._handle_round_end(winner)
            return

        # Проверка ничьей
        if self._is_board_full():
            messagebox.showinfo("Ничья", "Поле заполнено. Победила дружба!")
            self._reset_round()
            return

        # Передача хода
        self.current_player = "O" if self.current_player == "X" else "X"
        self.lbl_status.config(text=f"Ход: {self.current_player}")

    def _check_winner(self) -> str | None:
        b = self.buttons
        # Строки и столбцы
        for i in range(3):
            if b[i][0]["text"] == b[i][1]["text"] == b[i][2]["text"] != "":
                return b[i][0]["text"]
            if b[0][i]["text"] == b[1][i]["text"] == b[2][i]["text"] != "":
                return b[0][i]["text"]
        # Диагонали
        if b[0][0]["text"] == b[1][1]["text"] == b[2][2]["text"] != "":
            return b[0][0]["text"]
        if b[0][2]["text"] == b[1][1]["text"] == b[2][0]["text"] != "":
            return b[0][2]["text"]
        return None

    def _is_board_full(self) -> bool:
        return all(self.buttons[i][j]["text"] != "" for i in range(3) for j in range(3))

    def _handle_round_end(self, winner: str):
        self.game_active = False
        self.scores[winner] += 1
        self._update_scoreboard()

        messagebox.showinfo("Партия окончена", f"Игрок {winner} выиграл раунд!")

        # Проверка завершения матча
        if self.scores[winner] >= self.MATCH_TARGET:
            self.match_over = True
            self.lbl_status.config(text=f"🏆 МАТЧ ЗАВЕРШЁН! Победитель: {winner}")
            messagebox.showinfo("Победа в матче", f"Игрок {winner} первым набрал {self.MATCH_TARGET} победы!")
            for i in range(3):
                for j in range(3):
                    self.buttons[i][j].config(state="disabled")
        else:
            self.lbl_status.config(text=f"{winner} побеждает! Следующая партия...")
            # Авто-старт следующей партии через 1.2 сек для динамики
            self.root.after(1200, self._reset_round)

    def _update_scoreboard(self):
        self.lbl_x.config(text=f"X: {self.scores['X']}")
        self.lbl_o.config(text=f"O: {self.scores['O']}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = TicTacToeApp()
    app.run()