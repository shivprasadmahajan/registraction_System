import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3, os, sys
import requests
import webbrowser

# ================= COLORS =================
PRIMARY_COLOR = "#111827"
SECONDARY_COLOR = "#FFFFFF"
ACCENT_COLOR = "#3B82F6"
TEXT_COLOR = "#6B7280"

# ================= DATABASE =================
DB_NAME = "users.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            contact TEXT
        )
    ''')
    conn.commit()
    conn.close()

def register_user(name, email, password, contact):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (name, email, password, contact) VALUES (?, ?, ?, ?)",
                  (name, email, password, contact))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(email, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = c.fetchone()
    conn.close()
    return user

# ================= RESOURCE PATH =================
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ================= LOGIN =================
def show_login(root):
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Login Page")
    root.state('zoomed')
    root.configure(bg=SECONDARY_COLOR)

    form_frame = tk.Frame(root, bg=SECONDARY_COLOR)
    form_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Logo
    logo_path = resource_path("nova.png")
    if os.path.exists(logo_path):
        logo_img = Image.open(logo_path).resize((256, 75), Image.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_img)
        logo_label = tk.Label(form_frame, image=logo_photo, bg=SECONDARY_COLOR)
        logo_label.image = logo_photo
        logo_label.pack(pady=(0, 10))
    else:
        tk.Label(form_frame, text="🧾", font=("Helvetica", 50), bg=SECONDARY_COLOR).pack(pady=(0, 10))

    tk.Label(form_frame, text="NN Billing System", font=("Helvetica", 24, "bold"),
             fg=PRIMARY_COLOR, bg=SECONDARY_COLOR).pack(pady=(0,10))
    tk.Label(form_frame, text="Login to continue", font=("Helvetica", 14),
             fg=TEXT_COLOR, bg=SECONDARY_COLOR).pack()

    # Email
    tk.Label(form_frame, text="Email", font=("Helvetica", 10), fg=TEXT_COLOR, bg=SECONDARY_COLOR).pack(anchor="w", pady=(15,0))
    entry_email = tk.Entry(form_frame, width=40, font=("Helvetica",10), bd=1, relief="solid")
    entry_email.pack(pady=(5,10))

    # Password
    tk.Label(form_frame, text="Password", font=("Helvetica", 10), fg=TEXT_COLOR, bg=SECONDARY_COLOR).pack(anchor="w")
    entry_password = tk.Entry(form_frame, show="*", width=40, font=("Helvetica",10), bd=1, relief="solid")
    entry_password.pack(pady=(5,10))

    # 🔹 Login Button
    def handel_login():
        email = entry_email.get().strip()
        password = entry_password.get().strip()
        user = login_user(email, password)

        if user:
            # Optional: Call API first (just for logging)
            try:
                payload = {"email": user[2]}
                response = requests.post("http://127.0.0.1:5000/dashboard", json=payload)
                if response.status_code == 200:
                    # Open API in browser directly
                    webbrowser.open("http://127.0.0.1:5000/dashboard")
                    root.destroy()  # close Tkinter after redirect
                else:
                    messagebox.showerror("API Error", f"Status Code: {response.status_code}")
            except Exception as e:
                messagebox.showerror("Connection Error", f"Failed to connect to API:\n{e}")
        else:
            messagebox.showerror("Error", "Invalid email or password")

    tk.Button(form_frame, text="Login", width=30, font=("Helvetica",10,"bold"),
              bg=ACCENT_COLOR, fg=SECONDARY_COLOR, bd=0, pady=6, command=handel_login).pack(pady=(10,5))

    # Create Account button
    tk.Button(form_frame, text="Create Account", width=30, font=("Helvetica",10),
              bg=PRIMARY_COLOR, fg=SECONDARY_COLOR, bd=0, pady=6,
              command=lambda: show_register(root)).pack()

# ================= REGISTER =================
def show_register(root):
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Register Page")
    root.state('zoomed')
    root.configure(bg=SECONDARY_COLOR)

    form_frame = tk.Frame(root, bg=SECONDARY_COLOR)
    form_frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(form_frame, text="Create New Account", font=("Helvetica",20,"bold"),
             fg=PRIMARY_COLOR, bg=SECONDARY_COLOR).pack(pady=(0,20))

    tk.Label(form_frame, text="Name", font=("Helvetica",10), fg=TEXT_COLOR, bg=SECONDARY_COLOR).pack(anchor="w")
    entry_name = tk.Entry(form_frame, width=40, font=("Helvetica",10), bd=1, relief="solid")
    entry_name.pack(pady=(5,10))

    tk.Label(form_frame, text="Email", font=("Helvetica",10), fg=TEXT_COLOR, bg=SECONDARY_COLOR).pack(anchor="w")
    entry_email = tk.Entry(form_frame, width=40, font=("Helvetica",10), bd=1, relief="solid")
    entry_email.pack(pady=(5,10))

    tk.Label(form_frame, text="Password", font=("Helvetica",10), fg=TEXT_COLOR, bg=SECONDARY_COLOR).pack(anchor="w")
    entry_password = tk.Entry(form_frame, show="*", width=40, font=("Helvetica",10), bd=1, relief="solid")
    entry_password.pack(pady=(5,10))

    tk.Label(form_frame, text="Contact", font=("Helvetica",10), fg=TEXT_COLOR, bg=SECONDARY_COLOR).pack(anchor="w")
    entry_contact = tk.Entry(form_frame, width=40, font=("Helvetica",10), bd=1, relief="solid")
    entry_contact.pack(pady=(5,10))

    def handle_register():
        name = entry_name.get().strip()
        email = entry_email.get().strip()
        password = entry_password.get().strip()
        contact = entry_contact.get().strip()
        if register_user(name,email,password,contact):
            messagebox.showinfo("Success","Account created successfully!")
            show_login(root)
        else:
            messagebox.showerror("Error","Email already exists!")

    tk.Button(form_frame, text="Register", width=30, font=("Helvetica",10,"bold"),
              bg=ACCENT_COLOR, fg=SECONDARY_COLOR, bd=0, pady=6, command=handle_register).pack(pady=(10,5))
    tk.Button(form_frame, text="Back to Login", width=30, font=("Helvetica",10),
              bg=PRIMARY_COLOR, fg=SECONDARY_COLOR, bd=0, pady=6,
              command=lambda: show_login(root)).pack()

# ================= MAIN =================
if __name__=="__main__":
    init_db()
    root = tk.Tk()
    show_login(root)
    root.mainloop()
