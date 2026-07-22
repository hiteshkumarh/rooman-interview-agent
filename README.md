# rooman-interview-agent
AI Interview Agent built for the Rooman AI Challenge.
## Project Overview

The **AI Interview Agent** is an intelligent interview preparation application developed for the **Rooman AI Challenge**. It provides a realistic, AI-powered technical interview experience by generating role-specific interview questions, evaluating user responses, and delivering detailed feedback with scores and improvement suggestions.

The application is built using **Python**, **Streamlit**, and the **Groq LLM API** to create an interactive and responsive interview experience. Users can enter their profile details, take a personalized technical interview, receive instant AI-based evaluation, and optionally save their interview transcript for future review.

### Key Features

* 🤖 AI-generated interview questions based on job role, skills, and experience.
* 💬 Interactive interview session with one question at a time.
* 📊 AI-powered evaluation with scores and constructive feedback.
* 📄 Comprehensive interview report summarizing overall performance.
* 💾 Manual interview transcript saving in JSON format.
* 🎨 Clean and user-friendly Streamlit interface.

This project demonstrates the practical use of **Large Language Models (LLMs)** for interview preparation by combining prompt engineering, structured evaluation, and a simple web interface to simulate a real technical interview experience.

## Setup

1. Install dependencies:
   ```powershell
   python -m pip install -r requirements.txt
   ```

2. Create a `.env` file in the project root and add your Groq API key:
   ```text
   GROQ_API_KEY=your_api_key_here
   ```

   On Windows PowerShell, do not execute `GROQ_API_KEY=...` directly, because PowerShell treats that as a command. Instead create the file with:
   ```powershell
   New-Item -Path .env -ItemType File -Force
   Set-Content -Path .env -Value 'GROQ_API_KEY=your_api_key_here'
   ```

   Or open the file in a text editor:
   ```powershell
   notepad .env
   ```

3. Run the application:
   ```powershell
   streamlit run app.py
   ```

## Environment Variables

This project uses `python-dotenv` to load values from `.env` before `os.getenv()` is called. The Groq client initializes with `load_dotenv()` in `llm/client.py`, so `GROQ_API_KEY` is read from the `.env` file automatically.
