
# import spacy
# import os
# import textstat
# import pdfplumber
# from collections import Counter
# import re

# # Load spaCy NLP model
# nlp = spacy.load('en_core_web_sm')

# # Directory setup
# RESUME_DIR = 'resumes'
# METRICS_DIR = 'temp_metrics'
# OUTPUT_FILE = 'resume_scores.txt'
# os.makedirs(METRICS_DIR, exist_ok=True)

# # Skills & JD keywords (customize as needed)
# SKILL_LIST = ['python', 'java', 'c++', 'sql', 'aws', 'communication', 'leadership']
# JD_KEYWORDS = ['software development', 'python', 'agile', 'team collaboration']


# # ----------- Scoring Functions -----------

# def extract_text_from_pdf(pdf_path):
#     text = ''
#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             page_text = page.extract_text()
#             if page_text:
#                 text += page_text
#     return text


# def extract_skills(resume_text, skill_list):
#     doc = nlp(resume_text)
#     tokens = [token.text.lower() for token in doc]
#     return Counter(skill for skill in tokens if skill in skill_list)


# def score_work_experience(text):
#     keywords = ['experience', 'worked', 'internship', 'years', 'employed', 'developer', 'engineer']
#     score = sum(10 for keyword in keywords if keyword in text.lower())
#     year_mentions = re.findall(r'\b\d+\s+years?\b', text.lower())
#     score += len(year_mentions) * 5
#     return min(score, 100)


# def score_education(text):
#     keywords = ['bachelor', 'master', 'phd', 'university', 'college', 'degree', 'b.tech', 'm.tech']
#     score = sum(12 for keyword in keywords if keyword in text.lower())
#     return min(score, 100)


# def score_skills(extracted_skills):
#     return (len(extracted_skills) / len(SKILL_LIST)) * 100


# def score_keywords(text):
#     matches = sum(1 for kw in JD_KEYWORDS if kw.lower() in text.lower())
#     return (matches / len(JD_KEYWORDS)) * 100


# def score_formatting(text):
#     headings = ['summary', 'experience', 'education', 'skills', 'projects']
#     found = sum(1 for heading in headings if heading in text.lower())
#     return (found / len(headings)) * 100


# def evaluate_readability(text):
#     return textstat.flesch_kincaid_grade(text)


# def calculate_cv_score(work, edu, skills, keywords, formatting):
#     return round(
#         0.30 * work +
#         0.20 * edu +
#         0.25 * skills +
#         0.15 * keywords +
#         0.10 * formatting, 2
#     )


# # ----------- Main Resume Processing Loop -----------

# with open(OUTPUT_FILE, 'w', encoding='utf-8') as out_file:
#     for file in os.listdir(RESUME_DIR):
#         if file.endswith('.pdf'):
#             file_path = os.path.join(RESUME_DIR, file)
#             text = extract_text_from_pdf(file_path)

#             skills = extract_skills(text, SKILL_LIST)
#             work_score = score_work_experience(text)
#             edu_score = score_education(text)
#             skills_score = score_skills(skills)
#             keyword_score = score_keywords(text)
#             formatting_score = score_formatting(text)

#             final_score = calculate_cv_score(work_score, edu_score, skills_score, keyword_score, formatting_score)
#             readability = evaluate_readability(text)
#             jd_matches = sum(1 for kw in JD_KEYWORDS if kw.lower() in text.lower())

#             # Console Output
#             print(f"\n📄 {file}")
#             print(f"Work Experience Score: {work_score}")
#             print(f"Education Score: {edu_score}")
#             print(f"Skills Score: {skills_score:.2f}")
#             print(f"Keyword Score: {keyword_score:.2f}")
#             print(f"Formatting Score: {formatting_score:.2f}")
#             print(f"✅ Final CV Score: {final_score}/100")
#             print(f"Readability Score (Flesch-Kincaid): {readability}")
#             print(f"Extracted Skills: {skills.most_common(5)}")
#             print(f"JD Keywords Matched: {jd_matches}/{len(JD_KEYWORDS)}")

#             # Write individual metric file
#             with open(os.path.join(METRICS_DIR, f"{file}.txt"), 'w', encoding='utf-8') as metrics_file:
#                 metrics_file.write(f"Work Experience Score: {work_score}\n")
#                 metrics_file.write(f"Education Score: {edu_score}\n")
#                 metrics_file.write(f"Skills Score: {skills_score:.2f}\n")
#                 metrics_file.write(f"Keyword Score: {keyword_score:.2f}\n")
#                 metrics_file.write(f"Formatting Score: {formatting_score:.2f}\n")
#                 metrics_file.write(f"Final CV Score: {final_score}\n")
#                 metrics_file.write(f"Readability Score: {readability}\n")
#                 metrics_file.write(f"JD Keywords Matched: {jd_matches}/{len(JD_KEYWORDS)}\n")
#                 metrics_file.write(f"Extracted Skills: {skills.most_common(5)}\n")

#             # Write final score summary
#             out_file.write(f"{file} - Final CV Score: {final_score}/100\n")
# score.py
import os
import re
import spacy
import pdfplumber
from collections import Counter
import textstat

nlp = spacy.load('en_core_web_sm')

RESUME_DIR  = 'resumes'
METRICS_DIR = 'temp_metrics'
OUTPUT_FILE = 'resume_scores.txt'
os.makedirs(METRICS_DIR, exist_ok=True)

SKILL_LIST  = ['python','java','c++','sql','aws','communication','leadership']
JD_KEYWORDS = ['software development','python','agile','team collaboration']

def extract_text_from_pdf(path):
    text=''
    with pdfplumber.open(path) as pdf:
        for p in pdf.pages:
            t = p.extract_text()
            if t: text+=t
    return text

def extract_skills(text):
    tokens = [tok.text.lower() for tok in nlp(text)]
    return Counter(t for t in tokens if t in SKILL_LIST)

def score_work_experience(text):
    kws = ['experience','worked','internship','years','employed','developer','engineer']
    sc = sum(10 for k in kws if k in text.lower())
    sc += len(re.findall(r'\b\d+\s+years?\b', text.lower()))*5
    return min(sc,100)

def score_education(text):
    kws=['bachelor','master','phd','university','college','degree','b.tech','m.tech']
    return min(sum(12 for k in kws if k in text.lower()),100)

def score_skills(ex_skills):
    return (len(ex_skills)/len(SKILL_LIST))*100

def score_keywords(text):
    return (sum(1 for k in JD_KEYWORDS if k in text.lower())/len(JD_KEYWORDS))*100

def score_formatting(text):
    heads=['summary','experience','education','skills','projects']
    return (sum(1 for h in heads if h in text.lower())/len(heads))*100

def evaluate_readability(text):
    return textstat.flesch_kincaid_grade(text)

def calculate_cv_score(work,edu,skills,kw,fmt):
    return round(0.30*work + 0.20*edu + 0.25*skills + 0.15*kw + 0.10*fmt,2)

def run_scoring():
    with open(OUTPUT_FILE,'w',encoding='utf-8') as out:
        for fn in os.listdir(RESUME_DIR):
            if not fn.lower().endswith('.pdf'):
                continue
            path = os.path.join(RESUME_DIR,fn)
            txt  = extract_text_from_pdf(path)

            w  = score_work_experience(txt)
            e  = score_education(txt)
            s  = score_skills(extract_skills(txt))
            k  = score_keywords(txt)
            f  = score_formatting(txt)
            final = calculate_cv_score(w,e,s,k,f)
            rd = evaluate_readability(txt)
            jd = sum(1 for k in JD_KEYWORDS if k in txt.lower())

            # write metric file
            with open(os.path.join(METRICS_DIR,f"{fn}.txt"),'w',encoding='utf-8') as m:
                m.write(f"Work Experience Score: {w}\n")
                m.write(f"Education Score: {e}\n")
                m.write(f"Skills Score: {s:.2f}\n")
                m.write(f"Keyword Score: {k:.2f}\n")
                m.write(f"Formatting Score: {f:.2f}\n")
                m.write(f"Final CV Score: {final}\n")
                m.write(f"Readability Score: {rd}\n")
                m.write(f"JD Keywords Matched: {jd}/{len(JD_KEYWORDS)}\n")
                m.write(f"Extracted Skills: {extract_skills(txt).most_common(5)}\n")

            out.write(f"{fn} - Final CV Score: {final}/100\n")
            print(f"Scored {fn}: {final}/100")
