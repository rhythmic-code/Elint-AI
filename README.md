# Resume Processing and Feedback Pipeline

A Python‑based automated pipeline that:

- Fetches unread resume attachments (PDF/DOCX) via IMAP
- Masks personal identifiable information (PII)
- Extracts batch year and AI‑related experience
- Scores resumes on work experience, education, skills, formatting, keywords, and readability
- Generates per‑resume metrics and a summary score file
- Sends personalized feedback emails to each candidate
- Provides a single entry point: `main.py`

---

## 📁 Project Structure
```
<project-root>/
├── collector.py         # Fetch & preprocess resumes from email
├── score.py             # Score resumes against JD and skills
├── feedback.py          # Compose and send feedback emails
├── main.py              # Single entry point to run the entire pipeline
├── .env                 # Environment variables (not checked into Git)
├── .gitignore           # Files & folders to ignore in Git
├── requirements.txt     # Python dependencies
├── resumes/             # Fetched resume files
├── temp_metrics/        # Individual resume metric files
└── resume_scores.txt    # Summary of all resume scores
```

---

## ⚙️ Prerequisites

- **Python 3.8+**
- **Git**

---

## 🚀 Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-username>/<your-repo>.git
   cd <your-repo>
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   # macOS/Linux
   source venv/bin/activate
   # Windows
   venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   - Copy `.env.example` (if provided) or create a new `.env` file with:
     ```ini
     EMAIL_USER=your.email@example.com
     EMAIL_PASS=your-app-password
     IMAP_SERVER=imap.gmail.com
     ```
   - **Do not** commit your real credentials. Ensure `.env` is listed in `.gitignore`.

---

## 🏃‍♂️ Usage

Once set up, simply run:

```bash
python main.py
```

This will:

1. **Fetch** up to 50 unread resumes from your inbox (via `collector.py`).
2. **Process** each resume: extract text, mask PII, pull batch year & AI experience.
3. **Score** each resume and write detailed metrics in `temp_metrics/`; build a summary `resume_scores.txt` (via `score.py`).
4. **Email** personalized feedback to each sender, including the detailed breakdown (via `feedback.py`).

---

## 🛠 Customization

- **Adjust scoring criteria** in `score.py`:
  - Update `SKILL_LIST` and `JD_KEYWORDS` to match your job description.
  - Tweak weights in `calculate_cv_score()`.

- **Modify PII masking** in `collector.py`:
  - Update the regex patterns `EMAIL_REGEX`, `PHONE_REGEX`, and `NAME_REGEX`.
  - Extend `BATCH_PATTERNS` to capture other date formats.

---

## 📄 .gitignore Recommendations

Ensure you ignore:

```
__pycache__/
*.py[cod]
env/
venv/
.env
resumes/
temp_metrics/
*.log
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

