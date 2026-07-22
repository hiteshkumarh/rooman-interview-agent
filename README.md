# rooman-interview-agent
AI Interview Agent built for the Rooman AI Challenge.
## 1. Project Overview

The **AI Interview Agent** is an intelligent interview preparation application developed for the **Rooman AI Challenge**. It provides a realistic, AI-powered technical interview experience by generating role-specific interview questions, evaluating user responses, and delivering detailed feedback with scores and improvement suggestions.

The application is built using **Python**, **Streamlit**, and the **Groq LLM API** to create an interactive and responsive interview experience. Users can enter their profile details, take a personalized technical interview, receive instant AI-based evaluation, and optionally save their interview transcript for future review.

### 2. Key Features

* 🤖 AI-generated interview questions based on job role, skills, and experience.
* 💬 Interactive interview session with one question at a time.
* 📊 AI-powered evaluation with scores and constructive feedback.
* 📄 Comprehensive interview report summarizing overall performance.
* 💾 Manual interview transcript saving in JSON format.
* 🎨 Clean and user-friendly Streamlit interface.

This project demonstrates the practical use of **Large Language Models (LLMs)** for interview preparation by combining prompt engineering, structured evaluation, and a simple web interface to simulate a real technical interview experience.

## 3. Setup

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

## 4. Environment Variables

This project uses `python-dotenv` to load values from `.env` before `os.getenv()` is called. The Groq client initializes with `load_dotenv()` in `llm/client.py`, so `GROQ_API_KEY` is read from the `.env` file automatically.

## Tech Stack

| Category                       | Technology    |
| ------------------------------ | ------------- |
| **Programming Language**       | Python 3.12   |
| **Frontend / UI**              | Streamlit     |
| **Large Language Model (LLM)** | Groq API      |
| **Environment Management**     | python-dotenv |
| **Data Storage**               | JSON          |
| **Version Control**            | Git           |
| **Repository Hosting**         | GitHub        |

### Core Python Libraries

* **Streamlit** – Interactive web application framework.
* **Groq SDK** – Integration with the Groq Large Language Model.
* **python-dotenv** – Loads environment variables from a `.env` file.
* **JSON** – Stores interview transcripts and reports.
* **OS** – File and directory operations.
* **Datetime** – Generates timestamps for interview records.
* **UUID** *(if used)* – Generates unique identifiers for interview sessions.

### Development Tools

* Visual Studio Code
* Git
* GitHub
* Python Virtual Environment (`venv`)

## 5. Installation Steps

Follow these steps to set up and run the AI Interview Agent on your local machine.

### Prerequisites

Before installing the project, make sure you have the following installed:

* Python 3.12 or later
* Git
* A Groq API Key (available from the Groq Console)

---

## Step 1: Clone the Repository

Open your terminal or PowerShell and clone the repository:

```bash
git clone https://github.com/hiteshkumarh/rooman-interview-agent.git
```

---

## Step 2: Navigate to the Project Directory

Move into the project folder:

```bash
cd rooman-interview-agent
```

---

## Step 3: Create a Virtual Environment

Create a Python virtual environment to isolate project dependencies.

**Windows**

```bash
python -m venv .venv
```

**Linux/macOS**

```bash
python3 -m venv .venv
```

---

## Step 4: Activate the Virtual Environment

**Windows (PowerShell)**

```powershell
.\.venv\Scripts\Activate
```

**Windows (Command Prompt)**

```cmd
.venv\Scripts\activate.bat
```

**Linux/macOS**

```bash
source .venv/bin/activate
```

After activation, your terminal should display something similar to:

```text
(.venv)
```

---

## Step 5: Install Project Dependencies

Install all required Python packages using:

```bash
pip install -r requirements.txt
```

Wait until the installation completes successfully.

---

## Step 6: Configure Environment Variables

Create a `.env` file in the project's root directory.

**Windows (PowerShell)**

```powershell
New-Item .env -ItemType File
```

or simply create a file named `.env` manually.

Open the file and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Replace `your_groq_api_key_here` with your actual Groq API key.

> **Note:** Never commit your `.env` file to GitHub. The repository includes a `.env.example` file as a reference.

---

## Step 7: Verify the Installation

Check that the virtual environment is active and the required packages are installed:

```bash
pip list
```

You should see packages such as:

* streamlit
* groq
* python-dotenv

---

## Step 8: Launch the Application

Start the Streamlit application:

```bash
python -m streamlit run app.py
```

or

```bash
streamlit run app.py
```

---

## Step 9: Access the Application

Once the application starts successfully, Streamlit will display a local URL similar to:

```text
Local URL: http://localhost:8501
```

Open the URL in your web browser to begin using the AI Interview Agent.

---

## Step 10: Stop the Application

To stop the application, return to the terminal and press:

```text
Ctrl + C
```

To run the application again later:

1. Open the project folder.
2. Activate the virtual environment.
3. Run:

```bash
python -m streamlit run app.py
```

The AI Interview Agent is now ready to use.

## 6. Project Structure

```text
rooman-interview-agent/
│
├── assets/
│   └── Images and static resources used in the application.
│
├── config/
│   └── Configuration files and application settings.
│
├── llm/
│   ├── client.py          # Groq API client and LLM initialization
│   └── prompts.py         # Prompt templates for question generation and evaluation
│
├── models/
│   └── Data models used throughout the application.
│
├── services/
│   ├── evaluator.py           # Evaluates candidate answers
│   ├── interview_service.py   # Manages the complete interview workflow
│   ├── question_generator.py  # Generates AI interview questions
│   ├── report_generator.py    # Creates the final interview report
│   └── transcript_service.py  # Handles manual transcript saving
│
├── storage/
│   ├── json_storage.py        # JSON storage utility
│   └── transcripts/           # Stores manually saved interview transcripts
│
├── tests/
│   └── Unit and integration tests.
│
├── utils/
│   └── Helper functions and reusable utility modules.
│
├── .env.example          # Sample environment variables
├── .gitignore            # Git ignore rules
├── app.py                # Streamlit application entry point
├── README.md             # Project documentation
├── requirements.txt      # Python dependencies
└── LICENSE               # Project license (optional)
```

### Folder Description

| Folder/File          | Description                                                                                                                       |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| **app.py**           | Main Streamlit application that provides the user interface and controls the interview workflow.                                  |
| **llm/**             | Contains the Groq client and prompt templates used for AI-powered question generation and evaluation.                             |
| **services/**        | Implements the core business logic including interview management, answer evaluation, report generation, and transcript handling. |
| **storage/**         | Manages JSON-based storage for manually saved interview transcripts.                                                              |
| **models/**          | Stores data models used within the application.                                                                                   |
| **config/**          | Contains application configuration files and settings.                                                                            |
| **utils/**           | Includes reusable helper functions and utility modules.                                                                           |
| **assets/**          | Stores static assets such as images and icons used in the application.                                                            |
| **tests/**           | Contains test files for validating application functionality.                                                                     |
| **requirements.txt** | Lists all required Python packages and dependencies.                                                                              |
| **.env.example**     | Template showing the required environment variables.                                                                              |
| **README.md**        | Documentation explaining installation, usage, and project details.                                                                |
| **.gitignore**       | Specifies files and folders that should not be tracked by Git.                                                                   |

## Usage

After launching the application, follow these steps:

1. **Launch the Application**

   * Start the Streamlit application using:

     ```bash
     streamlit run app.py
     ```
   * Open the local URL displayed in your terminal (usually `http://localhost:8501`).

2. **Enter Candidate Details**

   * Provide your:

     * Job Role
     * Technical Skills
     * Years of Experience

3. **Start the Interview**

   * Click the **Start Interview** button.
   * The AI generates personalized interview questions based on your profile.

4. **Answer the Questions**

   * Read each question carefully.
   * Enter your answer in the provided text area.
   * Submit your response to proceed to the next question.

5. **View the Evaluation**

   * After completing all questions, the AI evaluates your responses.
   * Review:

     * Overall Score
     * Question-wise Feedback
     * Strengths
     * Areas for Improvement
     * Final Recommendation

6. **Save Interview Transcript (Optional)**

   * Click the **Save Interview** button to manually save your interview transcript in JSON format.
   * The transcript is stored in the `storage/transcripts/` directory.

7. **Start a New Interview**

   * Click **Start New Interview** to begin another interview session with a different profile.

---

# Screenshots

> Add screenshots of the application to help users understand the workflow.

### Landing Page

*(Insert screenshot here)*

```
assets/screenshots/landing-page.png
```

### Dashboard

*(Insert screenshot here)*

```
assets/screenshots/dashboard.png
```

### Interview Questions

*(Insert screenshot here)*

```
assets/screenshots/interview.png
```

### Evaluation Report

*(Insert screenshot here)*

```
assets/screenshots/evaluation.png
```

> **Optional:** You can also include a short GIF demonstrating the complete interview flow.

---

# Future Improvements

The following enhancements are planned for future versions of the AI Interview Agent:

* Add voice-based interviews using Speech-to-Text and Text-to-Speech.
* Support multiple interview domains such as Frontend, Backend, Data Science, DevOps, and Cloud.
* Generate downloadable PDF interview reports.
* Provide detailed analytics and performance tracking across multiple interview sessions.
* Add user authentication and personalized interview history.
* Support follow-up questions based on previous answers for a more realistic interview experience.
* Enable multilingual interview support.
* Integrate a database (e.g., PostgreSQL or MongoDB) for persistent storage.
* Deploy the application on a cloud platform for public access.
* Support multiple LLM providers (e.g., Groq, OpenAI, Gemini) with configurable model selection.
* Add an admin dashboard to monitor usage and interview statistics.
