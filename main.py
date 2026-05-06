import tkinter as tk
from tkinter import messagebox
from typing import Optional


class TicTacToeApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Крестики-нолики | ИИ + Матч до 3 побед")
        self.root.geometry("480x650")
        self.root.configure(bg="#1a1a2e")

        self.MATCH_TARGET = 3
        self.scores = {"X": 0, "O": 0}
        self.current_player = "X"
        self.game_active = False
        self.match_over = False
        self.buttons = []
        self.settings_widgets = []

        self.human_player = "X"
        self.ai_player = "O"
        self.ai_enabled = True

        self._setup_ui()
        self._unlock_controls()  # 👈 ЯВНО РАЗБЛОКИРУЕМ НАСТРОЙКИ ПРИ ЗАПУСКЕ
        self._update_status("Выбери сторону и нажми СТАРТ", "#ffd700")

    def _setup_ui(self):
        tk.Label(self.root, text="КРЕСТИКИ-НОЛИКИ", font=("Arial", 22, "bold"),
                 bg="#1a1a2e", fg="#e94560").pack(pady=10)

        settings_frame = tk.Frame(self.root, bg="#16213e", padx=10, pady=10)
        settings_frame.pack(pady=5, fill="x", padx=20)

        tk.Label(settings_frame, text="Ты играешь за:", bg="#16213e", fg="white", font=("Arial", 10)).pack(side="left")
        self.player_var = tk.StringVar(value="X")

        rb_x = tk.Radiobutton(settings_frame, text="X", variable=self.player_var, value="X", bg="#16213e", fg="white",
                              selectcolor="#0f3460", font=("Arial", 9), state="normal",
                              command=self._on_settings_change)
        rb_x.pack(side="left", padx=5)
        self.settings_widgets.append(rb_x)

        rb_o = tk.Radiobutton(settings_frame, text="O", variable=self.player_var, value="O", bg="#16213e", fg="white",
                              selectcolor="#0f3460", font=("Arial", 9), state="normal",
                              command=self._on_settings_change)
        rb_o.pack(side="left")
        self.settings_widgets.append(rb_o)

        tk.Label(settings_frame, text="|", bg="#16213e", fg="#555").pack(side="left", padx=10)

        self.ai_var = tk.BooleanVar(value=True)
        cb_ai = tk.Checkbutton(settings_frame, text="🤖 ИИ", variable=self.ai_var, bg="#16213e", fg="#4da8da",
                               selectcolor="#0f3460", font=("Arial", 9), state="normal",
                               command=self._on_settings_change)
        cb_ai.pack(side="left")
        self.settings_widgets.append(cb_ai)

        # Кнопка СТАРТ
        self.start_btn = tk.Button(self.root, text="▶️ НАЧАТЬ ИГРУ", bg="#00c853", fg="white",
                                   font=("Arial", 14, "bold"), command=self._start_game, state="normal")
        self.start_btn.pack(pady=10)

        self.status_lbl = tk.Label(self.root, text="Готово к игре", font=("Arial", 12), bg="#1a1a2e", fg="#ffd700")
        self.status_lbl.pack(pady=5)

        score_frame = tk.Frame(self.root, bg="#1a1a2e")
        score_frame.pack(pady=5)
        self.lbl_x = tk.Label(score_frame, text="X: 0", font=("Arial", 16, "bold"), fg="#e94560", bg="#1a1a2e")
        self.lbl_x.pack(side="left", padx=30)
        self.lbl_o = tk.Label(score_frame, text="O: 0", font=("Arial", 16, "bold"), fg="#4da8da", bg="#1a1a2e")
        self.lbl_o.pack(side="right", padx=30)

        board_frame = tk.Frame(self.root, bg="#1a1a2e")
        board_frame.pack(pady=10)
        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                btn = tk.Button(board_frame, text="", font=("Arial", 30, "bold"), width=4, height=2,
                                bg="#2d2d44", fg="white", relief="flat", activebackground="#3a3a5a",
                                state="disabled", command=lambda r=i, c=j: self._on_cell_click(r, c))
                btn.grid(row=i, column=j, padx=5, pady=5)
                row.append(btn)
            self.buttons.append(row)

        ctrl_frame = tk.Frame(self.root, bg="#1a1a2e")
        ctrl_frame.pack(pady=10)
        tk.Button(ctrl_frame, text="🔄 Сброс", bg="#0f3460", fg="white", font=("Arial", 10),
                  command=self._reset_round).pack(side="left", padx=10)
        tk.Button(ctrl_frame, text="🏆 Новый матч", bg="#e94560", fg="white", font=("Arial", 10),
                  command=self._new_match).pack(side="left", padx=10)

    def _on_settings_change(self):
        if not self.game_active:
            self.human_player = self.player_var.get()
            self.ai_player = "O" if self.human_player == "X" else "X"
            self.ai_enabled = self.ai_var.get()
            print(f"🔧 Настройки: Ты={self.human_player}, ИИ={self.ai_player}, ИИ_включен={self.ai_enabled}")
            first = "Ты (X)" if self.human_player == "X" else "ИИ (X)"
            self._update_status(f"Первым ходит: {first}. Нажми СТАРТ.", "#ffd700")

    def _update_status(self, text, color="#ffd700"):
        self.status_lbl.config(text=text, fg=color)

    def _lock_controls(self):
        for w in self.settings_widgets:
            w.config(state="disabled")
        self.start_btn.config(state="disabled", bg="#555")

    def _unlock_controls(self):
        for w in self.settings_widgets:
            w.config(state="normal")
        self.start_btn.config(state="normal", bg="#00c853", text="▶️ НАЧАТЬ ИГРУ")

    def _start_game(self):
        print("✅ СТАРТ НАЖАТ. Запуск партии...")
        if self.match_over:
            self.match_over = False
        self.game_active = True
        self.human_player = self.player_var.get()
        self.ai_player = "O" if self.human_player == "X" else "X"
        self.ai_enabled = self.ai_var.get()

        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", state="normal", bg="#2d2d44")

        self.current_player = "X"
        self._lock_controls()

        who_first = "Ты" if self.human_player == "X" else "ИИ"
        self._update_status(f"Ходит: {self.current_player} ({who_first})", "#00c853")

        if self.ai_enabled and self.current_player == self.ai_player:
            self.root.after(600, self._ai_move)

    def _reset_round(self):
        if not self.game_active: return
        self.current_player = "X"
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", state="normal", bg="#2d2d44")
        who_first = "Ты" if self.human_player == "X" else "ИИ"
        self._update_status(f"Ходит: {self.current_player} ({who_first})", "#00c853")
        if self.ai_enabled and self.current_player == self.ai_player:
            self.root.after(600, self._ai_move)

    def _new_match(self):
        self.scores = {"X": 0, "O": 0}
        self.match_over = False
        self.game_active = False
        self._update_scoreboard()
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", state="disabled", bg="#2d2d44")
        self._unlock_controls()
        self._on_settings_change()  # Обновляем статус под текущие настройки

    def _on_cell_click(self, row, col):
        if not self.game_active or self.match_over: return
        if self.buttons[row][col]["text"] != "": return
        if self.ai_enabled and self.current_player == self.ai_player: return

        self._make_move(row, col, self.current_player)
        if self._check_winner(self.current_player):
            self._round_end(self.current_player)
            return
        if self._is_board_full():
            messagebox.showinfo("Ничья", "Поле заполнено!")
            self._reset_round()
            return

        self.current_player = "O" if self.current_player == "X" else "X"
        if self.ai_enabled and self.current_player == self.ai_player:
            self._update_status("ИИ думает...", "#4da8da")
            self.root.after(500, self._ai_move)
        else:
            self._update_status(f"Твой ход ({self.current_player})", "#00c853")

    def _make_move(self, r, c, player):
        color = "#e94560" if player == "X" else "#4da8da"
        self.buttons[r][c].config(text=player, fg=color)

    def _ai_move(self):
        if not self.game_active: return
        best_score = -float("inf")
        best_move = None
        for i in range(3):
            for j in range(3):
                if self.buttons[i][j]["text"] == "":
                    self.buttons[i][j]["text"] = self.ai_player
                    score = self._minimax(False, 0)
                    self.buttons[i][j]["text"] = ""
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        if best_move:
            self._make_move(best_move[0], best_move[1], self.ai_player)
            if self._check_winner(self.ai_player):
                self._round_end(self.ai_player)
                return
            if self._is_board_full():
                messagebox.showinfo("Ничья", "Поле заполнено!")
                self._reset_round()
                return
            self.current_player = self.human_player
            self._update_status(f"Твой ход ({self.current_player})", "#00c853")

    def _minimax(self, is_maximizing, depth):
        if self._check_winner(self.ai_player): return 10 - depth
        if self._check_winner(self.human_player): return depth - 10
        if self._is_board_full(): return 0

        if is_maximizing:
            best = -float("inf")
            for i in range(3):
                for j in range(3):
                    if self.buttons[i][j]["text"] == "":
                        self.buttons[i][j]["text"] = self.ai_player
                        best = max(best, self._minimax(False, depth + 1))
                        self.buttons[i][j]["text"] = ""
            return best
        else:
            best = float("inf")
            for i in range(3):
                for j in range(3):
                    if self.buttons[i][j]["text"] == "":
                        self.buttons[i][j]["text"] = self.human_player
                        best = min(best, self._minimax(True, depth + 1))
                        self.buttons[i][j]["text"] = ""
            return best

    def _check_winner(self, player):
        b = self.buttons
        for i in range(3):
            if b[i][0]["text"] == b[i][1]["text"] == b[i][2]["text"] == player: return True
            if b[0][i]["text"] == b[1][i]["text"] == b[2][i]["text"] == player: return True
        if b[0][0]["text"] == b[1][1]["text"] == b[2][2]["text"] == player: return True
        if b[0][2]["text"] == b[1][1]["text"] == b[2][0]["text"] == player: return True
        return False

    def _is_board_full(self):
        return all(self.buttons[i][j]["text"] != "" for i in range(3) for j in range(3))

    def _round_end(self, winner):
        self.game_active = False
        self.scores[winner] += 1
        self._update_scoreboard()
        msg = "🎉 Ты победил!" if winner == self.human_player else "🤖 ИИ победил!"
        messagebox.showinfo("Раунд окончен", msg)
        if self.scores[winner] >= self.MATCH_TARGET:
            self.match_over = True
            final = "🏆 ТЫ выиграл матч!" if winner == self.human_player else "🤖 ИИ выиграл матч!"
            self._update_status(final, "#ffd700")
            messagebox.showinfo("Матч окончен", final)
            self._unlock_controls()
        else:
            self._update_status("Следующий раунд через 2 сек...", "#ecf0f1")
            self.root.after(2000, self._reset_round)

    def _update_scoreboard(self):
        self.lbl_x.config(text=f"X: {self.scores['X']}")
        self.lbl_o.config(text=f"O: {self.scores['O']}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = TicTacToeApp()
    app.run()