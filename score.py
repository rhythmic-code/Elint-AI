 
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
