import os
import tempfile
import threading
import PyPDF2
from gtts import gTTS
import tkinter as tk
from tkinter import filedialog, ttk, scrolledtext, messagebox
import customtkinter as ctk
import speech_recognition as sr

# --- Initialize CustomTkinter ---
ctk.set_appearance_mode("System")  # Options: "System", "Dark", "Light"
ctk.set_default_color_theme("dark-blue")

# --- PDF Parsing Logic (Placeholder) ---
def parse_pdf(file_path):
    try:
        reader = PyPDF2.PdfReader(file_path)
        text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
        return text
    except Exception as e:
        return f"Error parsing PDF: {e}"

# --- Text-to-Speech ---
def speak_text(text):
    try:
        tts = gTTS(text=text)
        temp_audio = tempfile.mktemp(suffix=".mp3")
        tts.save(temp_audio)
        os.system(f"start {temp_audio}")  # Windows only
    except Exception as e:
        messagebox.showerror("TTS Error", str(e))

# --- AI Placeholder (Replace with real model call) ---
def ai_answer(doc_text, question):
    # Placeholder response
    return f"This is a dummy answer to: '{question}' based on uploaded document."

# --- Main GUI App ---
class AbhiSearchApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AbhiSearch – AI Doc Search")
        self.geometry("1000x700")
        self.resizable(True, True)

        self.pdf_files = []
        self.docs_text = {}

        self.build_ui()

    def build_ui(self):
        # Header
        header_frame = ctk.CTkFrame(self)
        header_frame.pack(fill='x', padx=10, pady=10)

        title = ctk.CTkLabel(header_frame, text="🔍 AbhiSearch", font=("Segoe UI", 28, "bold"))
        title.pack(side='left')

        theme_btn = ctk.CTkButton(header_frame, text="🌗 Toggle Theme", command=self.toggle_theme)
        theme_btn.pack(side='right')

        upload_btn = ctk.CTkButton(header_frame, text="📤 Upload PDFs", command=self.upload_pdfs)
        upload_btn.pack(side='right', padx=10)

        # Body: Split View
        body = ctk.CTkFrame(self)
        body.pack(fill='both', expand=True, padx=10, pady=5)

        # Left Sidebar
        self.sidebar = ctk.CTkFrame(body, width=250)
        self.sidebar.pack(side='left', fill='y', padx=5)

        self.pdf_listbox = tk.Listbox(self.sidebar, height=20, bg="#222", fg="white")
        self.pdf_listbox.pack(fill='both', expand=True, padx=5, pady=5)
        self.pdf_listbox.bind("<<ListboxSelect>>", self.show_pdf_preview)

        # Central Panel
        center = ctk.CTkFrame(body)
        center.pack(side='left', fill='both', expand=True, padx=10)

        self.preview_label = ctk.CTkLabel(center, text="PDF Preview", font=("Segoe UI", 16))
        self.preview_label.pack(pady=5)

        self.preview_box = scrolledtext.ScrolledText(center, wrap='word', height=12)
        self.preview_box.pack(fill='both', expand=True, padx=5, pady=5)

        self.answer_label = ctk.CTkLabel(center, text="AI Answer", font=("Segoe UI", 16))
        self.answer_label.pack(pady=5)

        self.answer_box = ctk.CTkTextbox(center, height=6)
        self.answer_box.pack(fill='x', padx=5)

        # Bottom Bar
        bottom = ctk.CTkFrame(self)
        bottom.pack(fill='x', padx=10, pady=10)

        self.query_entry = ctk.CTkEntry(bottom, placeholder_text="Ask a question about your document...")
        self.query_entry.pack(side='left', fill='x', expand=True, padx=5)

        mic_btn = ctk.CTkButton(bottom, text="🎙️", width=40, command=self.dummy_voice_input)
        mic_btn.pack(side='left', padx=5)

        ask_btn = ctk.CTkButton(bottom, text="🧠 Ask AI", command=self.ask_ai)
        ask_btn.pack(side='left', padx=5)

        self.tts_toggle = ctk.CTkCheckBox(bottom, text="🔊 Read aloud")
        self.tts_toggle.pack(side='left', padx=10)

    def toggle_theme(self):
        current = ctk.get_appearance_mode()
        ctk.set_appearance_mode("Light" if current == "Dark" else "Dark")

    def upload_pdfs(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        for path in file_paths:
            filename = os.path.basename(path)
            self.pdf_files.append(path)
            self.docs_text[filename] = parse_pdf(path)
            self.pdf_listbox.insert('end', filename)

    def show_pdf_preview(self, event):
        selection = self.pdf_listbox.curselection()
        if selection:
            filename = self.pdf_listbox.get(selection[0])
            self.preview_box.delete('1.0', 'end')
            self.preview_box.insert('end', self.docs_text.get(filename, ""))

    def ask_ai(self):
        selection = self.pdf_listbox.curselection()
        if not selection:
            messagebox.showwarning("No File Selected", "Please select a PDF first.")
            return

        filename = self.pdf_listbox.get(selection[0])
        question = self.query_entry.get()
        doc_text = self.docs_text.get(filename, "")
        if not question:
            messagebox.showwarning("No Question", "Please enter a question.")
            return

        self.answer_box.delete("0.0", "end")
        self.answer_box.insert("end", "Typing answer...")
        self.after(300, lambda: self.display_answer(doc_text, question))

    def display_answer(self, doc_text, question):
        answer = ai_answer(doc_text, question)
        self.answer_box.delete("0.0", "end")
        self.answer_box.insert("end", answer)
        if self.tts_toggle.get():
            threading.Thread(target=speak_text, args=(answer,), daemon=True).start()

    def voice_input(self):
     recognizer = sr.Recognizer()
     with sr.Microphone() as source:
        self.query_entry.delete(0, 'end')
        self.query_entry.insert(0, "Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            self.query_entry.delete(0, 'end')
            self.query_entry.insert(0, text)
        except sr.UnknownValueError:
            self.query_entry.delete(0, 'end')
            self.query_entry.insert(0, "Sorry, couldn't understand.")
        except Exception as e:
            self.query_entry.delete(0, 'end')
            self.query_entry.insert(0, f"Error: {e}")


if __name__ == "__main__":
    app = AbhiSearchApp()
    app.mainloop()
