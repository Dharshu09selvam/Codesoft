import tkinter as tk
from tkinter import messagebox
import time

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe AI")
        self.window.configure(bg="#1E1E2F")
        self.window.state("zoomed")  # Maximize the window

        # Fullscreen Frame
        self.main_frame = tk.Frame(self.window, bg="#1E1E2F")
        self.main_frame.pack(expand=True)

        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        self.timer_label = tk.Label(self.main_frame, text="Time Left: 10s",
                                    font=("Consolas", 18), fg="#C7F9CC", bg="#1E1E2F")
        self.timer_label.pack(pady=10)

        self.board_frame = tk.Frame(self.main_frame, bg="#1E1E2F")
        self.board_frame.pack()

        self.player = "X"
        self.ai = "O"
        self.timer = 10
        self.timer_active = False

        self.create_buttons_with_animation()
        self.start_timer()

    def create_buttons_with_animation(self):
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.board_frame, text="", font=('Consolas', 36),
                                height=2, width=5,
                                bg="#2C2C54", fg="#FFFFFF",
                                activebackground="#6C5CE7", activeforeground="#FFFFFF",
                                relief="flat", bd=5,
                                command=lambda row=i, col=j: self.on_click(row, col))
                btn.grid(row=i, column=j, padx=10, pady=10)
                btn.update()
                self.buttons[i][j] = btn
                # Fade-in animation
                self.window.after((i * 3 + j) * 150, lambda b=btn: b.config(bg="#2C2C54"))

    def start_timer(self):
        self.timer = 10
        self.timer_active = True
        self.update_timer()

    def update_timer(self):
        if self.timer_active:
            self.timer_label.config(text=f"Time Left: {self.timer}s")
            if self.timer == 0:
                self.timer_active = False
                self.ai_move()
            else:
                self.timer -= 1
                self.window.after(1000, self.update_timer)

    def on_click(self, row, col):
        if self.board[row][col] == "" and self.timer_active:
            self.animate_click(self.buttons[row][col])
            self.make_move(row, col, self.player)
            self.timer_active = False
            if not self.check_winner(self.player):
                self.window.after(500, self.ai_move)

    def animate_click(self, button):
        original_color = button.cget("bg")
        button.config(bg="#A29BFE")
        self.window.update_idletasks()
        self.window.after(100)
        button.config(bg=original_color)

    def make_move(self, row, col, player):
        self.board[row][col] = player
        color = "#6C5CE7" if player == "X" else "#00CEC9"
        self.buttons[row][col].config(text=player, state="disabled", bg=color)

    def ai_move(self):
        best_score = float('-inf')
        best_move = None
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = self.ai
                    score = self.minimax(self.board, False)
                    self.board[i][j] = ""
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        if best_move:
            self.make_move(best_move[0], best_move[1], self.ai)
            if not self.check_winner(self.ai):
                self.start_timer()

    def minimax(self, board, is_maximizing):
        winner = self.evaluate_winner(board)
        if winner == self.ai:
            return 1
        elif winner == self.player:
            return -1
        elif self.is_draw(board):
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "":
                        board[i][j] = self.ai
                        score = self.minimax(board, False)
                        board[i][j] = ""
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "":
                        board[i][j] = self.player
                        score = self.minimax(board, True)
                        board[i][j] = ""
                        best_score = min(score, best_score)
            return best_score

    def evaluate_winner(self, board):
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != "":
                return board[i][0]
            if board[0][i] == board[1][i] == board[2][i] != "":
                return board[0][i]
        if board[0][0] == board[1][1] == board[2][2] != "":
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != "":
            return board[0][2]
        return None

    def is_draw(self, board):
        return all(cell != "" for row in board for cell in row) and self.evaluate_winner(board) is None

    def check_winner(self, player):
        winner = self.evaluate_winner(self.board)
        if winner:
            messagebox.showinfo("Game Over", f"{winner} wins!")
            self.reset_game()
            return True
        elif self.is_draw(self.board):
            messagebox.showinfo("Game Over", "It's a draw!")
            self.reset_game()
            return True
        return False

    def reset_game(self):
        for i in range(3):
            for j in range(3):
                self.board[i][j] = ""
                self.buttons[i][j].config(text="", state="normal", bg="#2C2C54")
        self.start_timer()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()
