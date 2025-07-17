💼 AbhiSearch – AI Resume Assistant
--------------------------------------
🔍 Overview
---------------
AbhiSearch is an AI-powered resume analysis tool that enables users to:
-------------------------------------------------------------------------

📄 Upload their resume in PDF format

❓ Ask any question related to their resume (e.g., “What are my strengths?” or “How can I improve it?”)

📊 Or ask the AI to rate their resume and provide improvement suggestions

This project uses the LLaMA 3 model via Ollama for local AI-powered analysis.

⚙️ Tech Stack
------------------------
Layer	Technology
Frontend	🧩 Streamlit
Backend	🛠️ Django REST Framework
AI Model	🧠 LLaMA 3 via Ollama
PDF Parsing	📄 PyMuPDF (fitz)

📁 Project Structure
------------------------------------------------------------------------
bash
Copy
Edit
abhigpt-search/
│
├── backend/
│   ├── views.py        # Core backend logic (upload, process, respond)
│   └── urls.py         # API routing
│
├── app.py              # Streamlit frontend UI
├── venv/               # Python virtual environment
├── README.md           # Project documentation
└── docs/               # (Optional) Test PDF uploads


🔄 How It Works
------------------
🧾 User uploads a PDF resume through the Streamlit interface.

🗣️ User either:

Asks a specific question (e.g., “Summarize my strengths”)

Or requests a resume rating (e.g., “Rate my resume”)

🛠️ The Django backend
-----------------------

Extracts text from the PDF using fitz (PyMuPDF)

Constructs a prompt based on the resume content and user query

🧠 The prompt is passed to Ollama, running the LLaMA 3 model locally.

💬 The AI generates a response which is returned to the frontend.

📲 The response is displayed to the user in Streamlit.

🔧 Backend: API Highlights
------------------------------

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
import fitz  # PyMuPDF for PDF text extraction
import subprocess  # To call local Ollama model

📥 Upload & Analyze Endpoint
-----------------------------------

@api_view(["POST"])
def upload_pdf(request):
    pdf_file = request.FILES.get("file")  # User-uploaded resume (PDF)
    query = request.POST.get("query", "")  # User's input query

    # Step 1: Read PDF using fitz
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = "".join([page.get_text() for page in doc])

    # Step 2: Create AI prompt
    if "rate my resume" in query.lower() or "score" in query.lower():
        prompt = f"... rate this resume and provide suggestions ..."
    else:
        prompt = f"... answer this query based on the resume ..."

    # Step 3: Run LLaMA 3 via Ollama
    result = subprocess.run(["ollama", "run", "llama3"], input=prompt, ...)

    # Step 4: Return AI response
    return Response({"answer": result.stdout.strip()})

    -----------------------------------------------------------------------------------------------------
🧪 Example Queries
✅ “What are the strong points in my resume?”

✅ “Give me suggestions to improve this resume”

✅ “Rate my resume”

✅ Requirements
Python 3.10+

<!-- Streamlit -->

Django REST Framework

PyMuPDF (pip install PyMuPDF)

Ollama with LLaMA 3 model installed locally (ollama run llama3)


# 1. Clone the repo

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate    # On Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start backend (Django API)
cd backend
python manage.py runserver


