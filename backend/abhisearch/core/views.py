from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
import fitz  # PyMuPDF
import subprocess

@api_view(["GET"])
def home(request):
    return JsonResponse({"message": "Welcome to AbhiSearch API"})

@api_view(["POST"])
def upload_pdf(request):
    pdf_file = request.FILES.get("file")
    query = request.POST.get("query", "").strip()

    if not pdf_file:
        return Response({"error": "No file uploaded"}, status=400)

    try:
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
    except Exception as e:
        return Response({"error": f"PDF read error: {str(e)}"}, status=400)

    # Check if the query is asking for a score
    if "rate my resume" in query.lower() or "score" in query.lower():
        prompt = f"""You're a professional resume reviewer.
Below is a resume:

{text[:2000]}

Evaluate this resume and give a score from 0 to 100.
Then, provide 2-3 specific suggestions to improve it.
Respond clearly in this format:

Score: <number>
Suggestions:
- Suggestion 1
- Suggestion 2
- Suggestion 3
"""
    else:
        prompt = f"""You are a helpful AI assistant. A user uploaded their resume and asked a question.

Resume:
{text[:2000]}

User's Question: \"{query}\"

Answer helpfully based on the resume:
"""

    try:
        result = subprocess.run(
            ["ollama", "run", "llama3"],
            input=prompt,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=60,
            encoding='utf-8'
        )

        if result.returncode != 0:
            return Response({"error": "Ollama failed: " + result.stderr}, status=500)

        return Response({"answer": result.stdout.strip()})
    except subprocess.TimeoutExpired:
        return Response({"error": "The AI response timed out. Please try again."}, status=500)
    except Exception as e:
        return Response({"error": f"Server error: {str(e)}"}, status=500)