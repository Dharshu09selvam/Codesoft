import tkinter as tk
from tkinter import scrolledtext

def get_response(user_input):
    user_input = user_input.lower().strip()

    if user_input in ['hi', 'hello', 'hey']:
        return "Hello! How can I help you today?"
    elif 'how are you' in user_input:
        return "I'm just a program, but I'm functioning as expected! 😊"
    elif 'your name' in user_input:
        return "I'm Chatbot 1.0, your virtual buddy!"
    elif 'help' in user_input:
        return "You can ask me about my name, how I'm doing, or just say hello."
    elif 'weather' in user_input:
        return "I can’t fetch live weather yet, but it’s always a good day to chat!"
    elif 'bye' in user_input:
        return "Goodbye! Talk to you soon. 👋"
    elif 'tell about yourself' in user_input:
        return "I'm a chatbot created to assist you with a variety of tasks, from giving greetings to sharing jokes. I'm always here to chat!"
    elif 'crack a joke' in user_input:
        return "Why don't skeletons fight each other? They don't have the guts! 😄"
    elif 'interview tip' in user_input:
        return "One great tip for interviews is to research the company thoroughly, and don’t forget to prepare questions to ask the interviewer!"
    else:
        return "Sorry, I didn’t quite get that. Can you rephrase?"

def send_message():
    user_msg = entry.get()
    if user_msg.strip() == "":
        return
    chat_window.config(state=tk.NORMAL)
    chat_window.insert(tk.END, "You: " + user_msg + "\n")
    response = get_response(user_msg)
    chat_window.insert(tk.END, "Bot: " + response + "\n\n")
    chat_window.config(state=tk.DISABLED)
    entry.delete(0, tk.END)
    chat_window.yview(tk.END)

root = tk.Tk()
root.title("Rule-Based Chatbot")
root.geometry("500x600")
root.configure(bg="#1e1e2f")

title = tk.Label(root, text="🧠 Chatbot 1.0", font=("Helvetica", 20, "bold"), fg="#ffffff", bg="#1e1e2f")
title.pack(pady=10)

chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, font=("Courier", 12))
chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chat_window.configure(bg="#2c2f33", fg="#ffffff", insertbackground="white")


entry = tk.Entry(root, font=("Helvetica", 14), bg="#393e46", fg="#eeeeee", insertbackground="white")
entry.pack(padx=10, pady=5, fill=tk.X)
entry.bind("<Return>", lambda event: send_message())

send_button = tk.Button(root, text="Send", command=send_message, font=("Helvetica", 12), bg="#00adb5", fg="white")
send_button.pack(pady=5)

root.mainloop()
