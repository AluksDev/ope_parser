import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import ttk
import pdfplumber
import re
import threading

def upload_pdf():
    pdf_path = filedialog.askopenfilename()

    if pdf_path:
        questions_text_box.delete("1.0", tk.END)
        questions_text_box.insert(tk.END, "Parsing PDF...")

        # Run parsing in another thread
        threading.Thread(target=parse_questions_pdf, args=(pdf_path,)).start()

def upload_answers_pdf():
    pdf_path = filedialog.askopenfilename()
    if (pdf_path):
        threading.Thread(target=parse_answers_pdf, args=(pdf_path,)).start()

answer_dictionary = {}
def parse_answers_pdf(pdf_path):
    global answer_dictionary
    answers_pdf = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                answers_pdf += text +"\n"
    parsed_answers = re.findall(r"\d+\s[ABCD]", text)
    answer_legend = {"A": 0, "B": 1, "C": 2, "D": 3}
    for answer in parsed_answers:
        number = int(answer.split(" ")[0])
        letter = answer.split(" ")[1]
        answer_dictionary[number] = answer_legend[letter]
    process_button.config(state="normal")
    answers_label.config(text="Answers loaded")

def parse_questions_pdf(pdf_path):
    full_pdf = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages[1:-1]:
            text = page.extract_text()
            if text:
                full_pdf += text + "\n"

    full_pdf = re.sub(r"Página \d+ de \d{2}", "", full_pdf)

    questions_text_box.after(0, update_textbox, full_pdf)
    upload_answers_button.config(state="normal")


def update_textbox(content):
    questions_text_box.delete("1.0", tk.END)
    questions_text_box.insert(tk.END, content)

def process_selection():
    try:
        selected_text = questions_text_box.get("sel.first", "sel.last")
        blocks = separate_blocks(selected_text)
        for block in blocks:
            result = extract_questions(block)
            add_correct_answer(result)
    except tk.TclError:
        print("No text selected")

def separate_blocks(text):
    blocks = re.split(r"(?=^\d+\s+\S)", text, flags=re.MULTILINE)
    blocks = [b.strip() for b in blocks if b.strip()]
    return blocks

def add_correct_answer(question):
    number = int(question["number"])
    correct = answer_dictionary.get(number)
    if correct is not None:
        question["correct"] = answer_dictionary[number]
        del question["number"]
    print (question)
    print("---------------------------------------------")

def extract_questions(text):
    text = text.replace("\n", " ")

    number_match = re.match(r"^\s*(\d+)\s*", text)
    question_number = number_match.group(1) 

    text = re.sub(r"^\s*\d+\s*", "", text)

    q_match = re.split(r"\bA\)\s*", text, maxsplit=1)
    question = q_match[0].strip()

    answers = re.findall(r"[A-D]\)\s*(.*?)(?=\s*[A-D]\)|$)", text)

    answers = [a.strip() for a in answers]

    return {
        "number": question_number,
        "question": question,
        "options": answers,
        "region_id": region_dropdown.current()
    }
import tkinter as tk
from tkinter import scrolledtext

root = tk.Tk()
root.title("OPE Parser")
root.geometry("550x520") # Shrunk the height back down since dropdowns save a lot of space!
root.configure(bg="#f5f5f5")

button_style = {"padx": 10, "pady": 5, "bd": 1, "relief": "groove"}

# ==========================================
# 1. FILE UPLOAD & CONFIGURATION SECTION
# ==========================================
upload_frame = tk.LabelFrame(root, text=" 1. Document Selection ", padx=15, pady=15, bg="#f5f5f5")
upload_frame.pack(fill="x", padx=20, pady=10)

# --- Region Selector (HTML Select / Dropdown Style) ---
region_label = tk.Label(upload_frame, text="Select Region / Comunidad:", bg="#f5f5f5", font=("Arial", 10, "bold"))
region_label.pack(anchor="w", pady=(0, 5))

# Create the Dropdown (Combobox)
# state="readonly" prevents the user from typing custom text into the box
region_dropdown = ttk.Combobox(upload_frame, state="readonly")
region_dropdown.pack(fill="x", pady=(0, 15))

# Set the options (like <option> tags in HTML)
region_dropdown['values'] = ("Andalucía", "Asturias", "Castilla y León", "Cataluña", "Aragón")

# Pre-select the first option ("Andalucía") by default
region_dropdown.current(0)


# --- Questions Row ---
upload_button = tk.Button(upload_frame, text="Upload questions PDF", command=upload_pdf, **button_style)
upload_button.pack(anchor="w", pady=(0, 10))


# --- Answers Row ---
answers_row = tk.Frame(upload_frame, bg="#f5f5f5")
answers_row.pack(fill="x")

upload_answers_button = tk.Button(
    answers_row,
    text="Upload answers PDF",
    command=upload_answers_pdf,
    state="disabled",
    **button_style
)
upload_answers_button.pack(side="left")

answers_label = tk.Label(answers_row, text="Not selected", fg="gray", bg="#f5f5f5")
answers_label.pack(side="left", padx=15)


# ==========================================
# 2. PROCESSING ACTION SECTION
# ==========================================
process_frame = tk.Frame(root, bg="#f5f5f5")
process_frame.pack(fill="x", padx=20, pady=10)

process_button = tk.Button(
    process_frame,
    text="Process Selection",
    command=process_selection,
    state="disabled",
    bg="#4CAF50",
    fg="white",
    activebackground="#45a049",
    padx=15,
    pady=8,
    bd=0
)
process_button.pack(side="left")

process_label = tk.Label(process_frame, text="", bg="#f5f5f5", font=("Arial", 10, "italic"))
process_label.pack(side="left", padx=15)


# ==========================================
# 3. RESULTS/OUTPUT SECTION
# ==========================================
output_frame = tk.LabelFrame(root, text=" 2. Parsed Output ", padx=10, pady=10, bg="#f5f5f5")
output_frame.pack(expand=True, fill="both", padx=20, pady=(10, 20))

questions_text_box = scrolledtext.ScrolledText(output_frame, wrap="word", bd=1, relief="sunken")
questions_text_box.pack(expand=True, fill="both")

root.mainloop()