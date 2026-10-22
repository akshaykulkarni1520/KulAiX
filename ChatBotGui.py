
import threading
import customtkinter as ctk
from ollama import chat


# ==================================================
# KulAiX | Created & Developed by Akshay Kulkarni
# ==================================================

APP_NAME = "KulAiX"
DEVELOPER = "Akshay Kulkarni"
MODEL = "llama3.2:1b"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ---------------- COLOR PALETTE ----------------

BG = "#090E1A"
SIDEBAR = "#0E1627"
PANEL = "#131E32"
CARD = "#17243A"
ACCENT = "#7868FF"
ACCENT_HOVER = "#6252E8"
CYAN = "#55D6FF"
TEXT = "#F1F5F9"
MUTED = "#8FA1BB"
USER_BUBBLE = "#342C72"
BOT_BUBBLE = "#152238"
BORDER = "#253550"
GREEN = "#34D399"


# ---------------- AI CONFIGURATION ----------------

SYSTEM_PROMPT = """
You are KulAiX, a helpful personal AI assistant
created and developed by Akshay Kulkarni.

You are powered by the locally running Ollama model.

Your capabilities include:
- Python and programming education
- Java, SQL and software development
- Machine learning and deep learning
- Generative AI, LLMs and RAG
- Debugging code and explaining errors
- General questions and problem solving

Explain concepts clearly using simple language,
examples and code when useful.

Format code using Markdown.
Be friendly, accurate and beginner-friendly.

If asked who created you, say:
"I am KulAiX, created and developed by Akshay Kulkarni."
"""

messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

is_generating = False


# ---------------- MAIN WINDOW ----------------

app = ctk.CTk()
app.title("KulAiX | Personal AI Assistant")
app.geometry("1200x760")
app.minsize(850, 600)
app.configure(fg_color=BG)

app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)


# ---------------- SIDEBAR ----------------

sidebar = ctk.CTkFrame(
    app,
    width=255,
    corner_radius=0,
    fg_color=SIDEBAR
)
sidebar.grid(row=0, column=0, sticky="nsew")
sidebar.grid_propagate(False)

# Logo
logo_frame = ctk.CTkFrame(
    sidebar,
    fg_color="transparent"
)
logo_frame.pack(fill="x", padx=22, pady=(28, 8))

logo = ctk.CTkFrame(
    logo_frame,
    width=47,
    height=47,
    corner_radius=14,
    fg_color=ACCENT
)
logo.pack(side="left")
logo.pack_propagate(False)

ctk.CTkLabel(
    logo,
    text="KX",
    font=("Segoe UI", 19, "bold"),
    text_color="#FFFFFF"
).pack(expand=True)

brand_text = ctk.CTkFrame(
    logo_frame,
    fg_color="transparent"
)
brand_text.pack(side="left", padx=11)

ctk.CTkLabel(
    brand_text,
    text="KulAiX",
    font=("Segoe UI", 23, "bold"),
    text_color=TEXT
).pack(anchor="w")

ctk.CTkLabel(
    brand_text,
    text="PERSONAL AI",
    font=("Segoe UI", 9, "bold"),
    text_color=CYAN
).pack(anchor="w")


ctk.CTkLabel(
    sidebar,
    text="YOUR INTELLIGENCE. YOUR INNOVATION.",
    font=("Segoe UI", 9, "bold"),
    text_color=MUTED
).pack(anchor="w", padx=23, pady=(12, 28))


def sidebar_button(title, command, icon=""):
    button = ctk.CTkButton(
        sidebar,
        text=f"{icon}  {title}",
        command=command,
        anchor="w",
        height=45,
        corner_radius=11,
        fg_color="transparent",
        hover_color=CARD,
        text_color=TEXT,
        font=("Segoe UI", 13),
        border_spacing=12
    )
    button.pack(fill="x", padx=14, pady=4)
    return button


ctk.CTkLabel(
    sidebar,
    text="WORKSPACE",
    font=("Segoe UI", 10, "bold"),
    text_color=MUTED
).pack(anchor="w", padx=23, pady=(0, 8))


# ---------------- MAIN CHAT AREA ----------------

main = ctk.CTkFrame(
    app,
    fg_color=BG,
    corner_radius=0
)
main.grid(row=0, column=1, sticky="nsew")

main.grid_columnconfigure(0, weight=1)
main.grid_rowconfigure(1, weight=1)


# ---------------- HEADER ----------------

header = ctk.CTkFrame(
    main,
    fg_color=BG,
    corner_radius=0
)
header.grid(
    row=0,
    column=0,
    sticky="ew",
    padx=28,
    pady=(23, 16)
)
header.grid_columnconfigure(0, weight=1)

ctk.CTkLabel(
    header,
    text="AI WORKSPACE",
    font=("Segoe UI", 10, "bold"),
    text_color=CYAN
).grid(row=0, column=0, sticky="w")

ctk.CTkLabel(
    header,
    text="How can I help you today?",
    font=("Segoe UI", 25, "bold"),
    text_color=TEXT
).grid(row=1, column=0, sticky="w", pady=(5, 3))

status_label = ctk.CTkLabel(
    header,
    text="●  LOCAL MODEL  ·  LLAMA 3.2:1B",
    font=("Segoe UI", 10, "bold"),
    text_color=GREEN
)
status_label.grid(row=2, column=0, sticky="w", pady=(5, 0))

new_chat_top = ctk.CTkButton(
    header,
    text="+  New Chat",
    width=110,
    height=36,
    corner_radius=10,
    fg_color=CARD,
    hover_color=BORDER,
    text_color=TEXT,
    command=lambda: clear_chat()
)
new_chat_top.grid(row=1, column=1, rowspan=2, padx=(12, 0))


# ---------------- CHAT HISTORY ----------------

chat_frame = ctk.CTkScrollableFrame(
    main,
    fg_color=BG,
    corner_radius=12,
    scrollbar_button_color=BORDER,
    scrollbar_button_hover_color=ACCENT
)
chat_frame.grid(
    row=1,
    column=0,
    sticky="nsew",
    padx=24,
    pady=(0, 12)
)
chat_frame.grid_columnconfigure(0, weight=1)


def scroll_to_bottom():
    app.after(
        100,
        lambda: chat_frame._parent_canvas.yview_moveto(1.0)
    )


def add_message(role, text):
    is_user = role == "user"

    row = ctk.CTkFrame(
        chat_frame,
        fg_color="transparent"
    )
    row.grid(
        column=0,
        sticky="e" if is_user else "w",
        padx=8,
        pady=9
    )

    bubble = ctk.CTkFrame(
        row,
        fg_color=USER_BUBBLE if is_user else BOT_BUBBLE,
        corner_radius=16,
        border_width=1,
        border_color=ACCENT if is_user else BORDER
    )
    bubble.pack(
        anchor="e" if is_user else "w",
        padx=(45, 0) if is_user else (0, 45)
    )

    sender_color = CYAN if is_user else "#B8ADFF"
    sender = "YOU" if is_user else "KulAiX  ✦"

    ctk.CTkLabel(
        bubble,
        text=sender,
        font=("Segoe UI", 10, "bold"),
        text_color=sender_color
    ).pack(anchor="w", padx=15, pady=(11, 3))

    ctk.CTkLabel(
        bubble,
        text=text,
        font=("Segoe UI", 13),
        text_color=TEXT,
        wraplength=650,
        justify="left",
        anchor="w"
    ).pack(
        anchor="w",
        padx=15,
        pady=(2, 13)
    )

    scroll_to_bottom()
    return row


def show_welcome():
    welcome = ctk.CTkFrame(
        chat_frame,
        fg_color=CARD,
        corner_radius=20,
        border_width=1,
        border_color=BORDER
    )
    welcome.grid(
        row=0,
        column=0,
        sticky="ew",
        padx=8,
        pady=(25, 20)
    )

    ctk.CTkLabel(
        welcome,
        text="✦",
        font=("Segoe UI", 38, "bold"),
        text_color=CYAN
    ).pack(pady=(22, 0))

    ctk.CTkLabel(
        welcome,
        text="Welcome to KulAiX",
        font=("Segoe UI", 25, "bold"),
        text_color=TEXT
    ).pack(pady=(4, 5))

    ctk.CTkLabel(
        welcome,
        text="Your personal AI companion for learning and creating.",
        font=("Segoe UI", 12),
        text_color=MUTED,
        wraplength=600
    ).pack(padx=15, pady=(0, 14))

    ctk.CTkLabel(
        welcome,
        text="CREATED & DEVELOPED BY AKSHAY KULKARNI",
        font=("Segoe UI", 10, "bold"),
        text_color="#B8ADFF"
    ).pack(pady=(0, 22))

    suggestions = [
        ("01", "Learn Python", "Create a Python roadmap for beginners."),
        ("02", "Explain concepts", "Explain Python OOP with an example."),
        ("03", "Coding practice", "Give me a Python coding challenge."),
        ("04", "Explore GenAI", "Explain LLMs and RAG with examples.")
    ]

    cards = ctk.CTkFrame(
        chat_frame,
        fg_color="transparent"
    )
    cards.grid(row=1, column=0, sticky="ew", padx=8)
    cards.grid_columnconfigure((0, 1), weight=1)

    for index, (number, title, prompt) in enumerate(suggestions):
        card = ctk.CTkButton(
            cards,
            text=f"{number}   {title}\n\n{prompt}",
            command=lambda p=prompt: insert_prompt(p),
            height=90,
            corner_radius=13,
            fg_color=PANEL,
            hover_color=CARD,
            border_width=1,
            border_color=BORDER,
            text_color=TEXT,
            font=("Segoe UI", 12),
            anchor="w"
        )
        card.grid(
            row=index // 2,
            column=index % 2,
            sticky="ew",
            padx=5,
            pady=5
        )

    scroll_to_bottom()


# ---------------- CHAT ACTIONS ----------------

def set_busy(busy):
    global is_generating
    is_generating = busy

    send_button.configure(
        state="disabled" if busy else "normal"
    )

    status_label.configure(
        text="●  KulAiX IS THINKING..." if busy
        else "●  LOCAL MODEL  ·  LLAMA 3.2:1B",
        text_color="#FBBF24" if busy else GREEN
    )


def finish_response(answer=None, error=None, waiting=None):
    if waiting is not None:
        waiting.destroy()

    if error:
        add_message(
            "assistant",
            "I couldn't generate a response.\n\n"
            "Please check that Ollama is running and that "
            "the selected model is installed.\n\n"
            "Run this command in your terminal:\n"
            "ollama run llama3.2:1b"
        )
        print("Ollama error:", error)

    elif answer:
        messages.append({
            "role": "assistant",
            "content": answer
        })
        add_message("assistant", answer)

    set_busy(False)


def generate_response(waiting):
    try:
        # Keep a stable snapshot of conversation history.
        history = messages.copy()

        response = chat(
            model=MODEL,
            messages=history,
            stream=False
        )

        answer = response.message.content

        app.after(
            0,
            lambda: finish_response(
                answer=answer,
                waiting=waiting
            )
        )

    except Exception as exc:
        error_text = str(exc)
        app.after(
            0,
            lambda err=error_text: finish_response(
                error=err,
                waiting=waiting
            )
        )


def send_message(event=None):
    if is_generating:
        return "break"

    question = input_box.get().strip()

    if not question:
        return "break"

    input_box.delete(0, "end")

    messages.append({
        "role": "user",
        "content": question
    })

    add_message("user", question)

    waiting = add_message("assistant", "Thinking...")

    set_busy(True)

    threading.Thread(
        target=generate_response,
        args=(waiting,),
        daemon=True
    ).start()

    return "break"


def clear_chat():
    if is_generating:
        return

    global messages
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for widget in chat_frame.winfo_children():
        widget.destroy()

    show_welcome()


def insert_prompt(prompt):
    if is_generating:
        return

    input_box.delete(0, "end")
    input_box.insert(0, prompt)
    input_box.focus()


# ---------------- SIDEBAR BUTTONS ----------------

sidebar_button(
    "New Conversation",
    clear_chat,
    "+"
)

sidebar_button(
    "Learn Python",
    lambda: insert_prompt(
        "Create a step-by-step Python learning roadmap."
    ),
    "🐍"
)

sidebar_button(
    "Explain Concepts",
    lambda: insert_prompt(
        "Explain Python OOP with a simple example."
    ),
    "✦"
)

sidebar_button(
    "Coding Practice",
    lambda: insert_prompt(
        "Give me a Python coding problem with hints."
    ),
    "⌘"
)

sidebar_button(
    "Explore GenAI",
    lambda: insert_prompt(
        "Explain LLMs, embeddings and RAG with Python examples."
    ),
    "◈"
)


# ---------------- SIDEBAR FOOTER ----------------

footer = ctk.CTkFrame(
    sidebar,
    fg_color=PANEL,
    corner_radius=14,
    border_width=1,
    border_color=BORDER
)
footer.pack(
    side="bottom",
    fill="x",
    padx=14,
    pady=18
)

ctk.CTkLabel(
    footer,
    text="●  LOCAL AI ENGINE",
    font=("Segoe UI", 10, "bold"),
    text_color=GREEN
).pack(anchor="w", padx=13, pady=(13, 5))

ctk.CTkLabel(
    footer,
    text="Powered by Ollama\nLlama 3.2:1B\n\nDeveloped by\nAkshay Kulkarni",
    font=("Segoe UI", 11),
    text_color=MUTED,
    justify="left"
).pack(anchor="w", padx=13, pady=(0, 13))


# ---------------- INPUT AREA ----------------

input_panel = ctk.CTkFrame(
    main,
    fg_color=PANEL,
    corner_radius=17,
    border_width=1,
    border_color=BORDER
)
input_panel.grid(
    row=2,
    column=0,
    sticky="ew",
    padx=24,
    pady=(0, 10)
)
input_panel.grid_columnconfigure(0, weight=1)

input_box = ctk.CTkEntry(
    input_panel,
    placeholder_text="Message KulAiX... Ask anything",
    height=50,
    corner_radius=12,
    border_width=0,
    fg_color=PANEL,
    text_color=TEXT,
    placeholder_text_color=MUTED,
    font=("Segoe UI", 14)
)
input_box.grid(
    row=0,
    column=0,
    sticky="ew",
    padx=(13, 8),
    pady=12
)
input_box.bind("<Return>", send_message)

send_button = ctk.CTkButton(
    input_panel,
    text="Send  ➤",
    command=send_message,
    width=105,
    height=42,
    corner_radius=11,
    fg_color=ACCENT,
    hover_color=ACCENT_HOVER,
    text_color="#FFFFFF",
    font=("Segoe UI", 13, "bold")
)
send_button.grid(
    row=0,
    column=1,
    padx=(0, 12),
    pady=12
)


# ---------------- FOOTER ----------------

ctk.CTkLabel(
    main,
    text="KulAiX  •  Ollama  •  Local Inference  •  Created by Akshay Kulkarni",
    font=("Segoe UI", 10),
    text_color=MUTED
).grid(
    row=3,
    column=0,
    pady=(0, 12)
)


# ---------------- START APPLICATION ----------------

show_welcome()
input_box.focus()

app.mainloop()
