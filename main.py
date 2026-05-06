import tkinter as tk
from tkinter import messagebox
from typing import Optional


class TicTacToeApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Крестики-нолики | ИИ + Матч до 3 побед")
        self.root.geometry("480x680")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a2e")

        self.MATCH_TARGET = 3
        self.scores = {"X": 0, "O": 0}
        self.current_player = "X"
        self.game_active = True
        self.match_over = False
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        # 🤖 Настройки ИИ
        self.ai_player = "O"  # ИИ играет за "O" по умолчанию
        self.human_player = "X"
        self.ai_enabled = True  # Включить/выключить ИИ

        self._setup_ui()
        self._reset_round()

    def _setup_ui(self):
        # Заголовок
        tk.Label(self.root, text="КРЕСТИКИ-НОЛИКИ", font=("Arial", 22, "bold"),
                 bg="#1a1a2e", fg="#e94560").pack(pady=(15, 5))

        # Выбор стороны и ИИ
        choice_frame = tk.Frame(self.root, bg="#16213e")
        choice_frame.pack(pady=10, padx=20, fill="x")

        tk.Label(choice_frame, text="Вы играете за:", bg="#16213e", fg="white", font=("Arial", 10)).pack(side="left",
                                                                                                         padx=5)
        self.player_var = tk.StringVar(value="X")
        tk.Radiobutton(choice_frame, text="X", variable=self.player_var, value="X", bg="#16213e", fg="white",
                       selectcolor="#0f3460", font=("Arial", 9), command=self._on_player_change).pack(side="left")
        tk.Radiobutton(choice_frame, text="O", variable=self.player_var, value="O", bg="#16213e", fg="white",
                       selectcolor="#0f3460", font=("Arial", 9), command=self._on_player_change).pack(side="left",
                                                                                                      padx=10)

        tk.Label(choice_frame, text="|", bg="#16213e", fg="#555").pack(side="left", padx=5)

        self.ai_var = tk.BooleanVar(value=True)
        tk.Checkbutton(choice_frame, text="🤖 ИИ-противник", variable=self.ai_var, bg="#16213e", fg="#4da8da",
                       selectcolor="#0f3460", font=("Arial", 9), command=self._on_ai_toggle).pack(side="left")

        # Счёт
        score_frame = tk.Frame(self.root, bg="#1a1a2e")
        score_frame.pack(pady=10)
        self.lbl_x = tk.Label(score_frame, text="X: 0", font=("Arial", 18, "bold"), fg="#e94560", bg="#1a1a2e")
        self.lbl_x.pack(side="left", padx=25)
        self.lbl_o = tk.Label(score_frame, text="O: 0", font=("Arial", 18, "bold"), fg="#4da8da", bg="#1a1a2e")
        self.lbl_o.pack(side="right", padx=25)

        # Статус
        self.lbl_status = tk.Label(self.root, text="Ход: X", font=("Arial", 13), bg="#1a1a2e", fg="#ecf0f1")
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
        tk.Button(ctrl_frame, text="🔄 Сбросить поле", bg="#0f3460", fg="white", font=("Arial", 10, "bold"),
                  command=self._reset_round).pack(side="left", padx=8)
        tk.Button(ctrl_frame, text="🏆 Новый матч", bg="#e94560", fg="white", font=("Arial", 10, "bold"),
                  command=self._start_new_match).pack(side="left", padx=8)
        tk.Button(ctrl_frame, text="⚙️ Настройки", bg="#555", fg="white", font=("Arial", 10),
                  command=self._show_settings).pack(side="left", padx=8)

    def _on_player_change(self):
        if self.game_active and not self.match_over:
            self.human_player = self.player_var.get()
            self.ai_player = "O" if self.human_player == "X" else "X"
            self.current_player = self.human_player
            self.lbl_status.config(text=f"Ход: {self.current_player}")
            if self.ai_enabled and self.current_player == self.ai_player:
                self.root.after(500, self._ai_move)

    def _on_ai_toggle(self):
        self.ai_enabled = self.ai_var.get()
        if self.ai_enabled and self.game_active and self.current_player == self.ai_player:
            self.root.after(500, self._ai_move)

    def _show_settings(self):
        settings_win = tk.Toplevel(self.root)
        settings_win.title("Настройки")
        settings_win.geometry("300x200")
        settings_win.configure(bg="#1a1a2e")
        settings_win.resizable(False, False)

        tk.Label(settings_win, text="Побед до конца матча:", bg="#1a1a2e", fg="white", font=("Arial", 11)).pack(pady=15)
        target_frame = tk.Frame(settings_win, bg="#1a1a2e")
        target_frame.pack()
        for val in [1, 3, 5]:
            tk.Radiobutton(target_frame, text=str(val), variable=tk.IntVar(value=self.MATCH_TARGET),
                           value=val, bg="#1a1a2e", fg="#4da8da", selectcolor="#0f3460",
                           command=lambda v=val: self._set_match_target(v)).pack(side="left", padx=10)

        tk.Button(settings_win, text="Закрыть", command=settings_win.destroy, bg="#0f3460", fg="white").pack(pady=10)

    def _set_match_target(self, value):
        self.MATCH_TARGET = value
        self._start_new_match()

    def _start_new_match(self):
        self.scores = {"X": 0, "O": 0}
        self.match_over = False
        self._reset_round()
        self._update_scoreboard()
        self.lbl_status.config(text="Матч начат! Ход: " + self.current_player)

    def _reset_round(self):
        if self.match_over:
            self.match_over = False
        self.game_active = True
        self.human_player = self.player_var.get()
        self.ai_player = "O" if self.human_player == "X" else "X"
        self.current_player = self.human_player
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", bg="#2d2d44", state="normal", fg="white")
        self.lbl_status.config(text=f"Ход: {self.current_player}")
        # Если ИИ ходит первым
        if self.ai_enabled and self.current_player == self.ai_player:
            self.root.after(700, self._ai_move)

    def _on_click(self, row, col):
        if not self.game_active or self.match_over:
            return
        if self.ai_enabled and self.current_player == self.ai_player:
            return  # Запрещаем клики, когда ход ИИ

        btn = self.buttons[row][col]
        if btn["text"] != "":
            return

        self._make_move(row, col, self.current_player)

        winner = self._check_winner()
        if winner:
            self._handle_round_end(winner)
            return

        if self._is_board_full():
            messagebox.showinfo("Ничья", "Поле заполнено. Победила дружба!")
            self._reset_round()
            return

        self.current_player = "O" if self.current_player == "X" else "X"
        self.lbl_status.config(text=f"Ход: {self.current_player}")

        # Ход ИИ
        if self.ai_enabled and self.current_player == self.ai_player:
            self.root.after(500, self._ai_move)  # Небольшая задержка для естественности

    def _make_move(self, row, col, player):
        color = "#e94560" if player == "X" else "#4da8da"
        self.buttons[row][col].config(text=player, fg=color)

    # 🤖 === ЛОГИКА ИИ (МИНИМАКС) ===
    def _ai_move(self):
        if not self.game_active or self.match_over:
            return

        best_score = -float("inf")
        best_move = None

        # Перебираем все свободные клетки
        for i in range(3):
            for j in range(3):
                if self.buttons[i][j]["text"] == "":
                    # Пробуем ход
                    self.buttons[i][j]["text"] = self.ai_player
                    score = self._minimax(0, False)
                    self.buttons[i][j]["text"] = ""  # Отменяем ход
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

        if best_move:
            row, col = best_move
            self._make_move(row, col, self.ai_player)

            winner = self._check_winner()
            if winner:
                self._handle_round_end(winner)
                return
            if self._is_board_full():
                messagebox.showinfo("Ничья", "Поле заполнено. Победила дружба!")
                self._reset_round()
                return

            self.current_player = self.human_player
            self.lbl_status.config(text=f"Ход: {self.current_player}")

    def _minimax(self, depth, is_maximizing):
        winner = self._check_winner()
        if winner == self.ai_player:
            return 10 - depth  # Чем быстрее победа, тем лучше
        if winner == self.human_player:
            return depth - 10  # Чем дольше проигрываем, тем хуже
        if self._is_board_full():
            return 0  # Ничья

        if is_maximizing:
            best_score = -float("inf")
            for i in range(3):
                for j in range(3):
                    if self.buttons[i][j]["text"] == "":
                        self.buttons[i][j]["text"] = self.ai_player
                        score = self._minimax(depth + 1, False)
                        self.buttons[i][j]["text"] = ""
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for i in range(3):
                for j in range(3):
                    if self.buttons[i][j]["text"] == "":
                        self.buttons[i][j]["text"] = self.human_player
                        score = self._minimax(depth + 1, True)
                        self.buttons[i][j]["text"] = ""
                        best_score = min(score, best_score)
            return best_score

    # === КОНЕЦ ЛОГИКИ ИИ ===

    def _check_winner(self) -> Optional[str]:
        b = self.buttons
        for i in range(3):
            if b[i][0]["text"] == b[i][1]["text"] == b[i][2]["text"] != "":
                return b[i][0]["text"]
            if b[0][i]["text"] == b[1][i]["text"] == b[2][i]["text"] != "":
                return b[0][i]["text"]
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
        result_text = "Вы победили!" if winner == self.human_player else "ИИ победил!"
        messagebox.showinfo("Партия окончена",
                            result_text + f"\nСчёт: Вы {self.scores[self.human_player]} - {self.scores[self.ai_player]} ИИ")

        if self.scores[winner] >= self.MATCH_TARGET:
            self.match_over = True
            final_msg = "🏆 ВЫ выиграли матч!" if winner == self.human_player else "🤖 ИИ выиграл матч!"
            self.lbl_status.config(text=final_msg)
            messagebox.showinfo("Матч завершён", final_msg)
            for i in range(3):
                for j in range(3):
                    self.buttons[i][j].config(state="disabled")
        else:
            self.lbl_status.config(text="Следующая партия...")
            self.root.after(1500, self._reset_round)

    def _update_scoreboard(self):
        self.lbl_x.config(text=f"X: {self.scores['X']}")
        self.lbl_o.config(text=f"O: {self.scores['O']}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = TicTacToeApp()
    app.run()