
import os
import re
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from dotenv import load_dotenv

load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_metrics_from_file(fn_line):
    fn = fn_line.split(" - ")[0].strip()
    metrics = {
        'filename': fn,
        'final_score': 'N/A', 'work_exp':'N/A','education':'N/A',
        'skills':'N/A','keywords':'N/A','formatting':'N/A',
        'readability':'N/A','jd_matches':'N/A','top_skills':'N/A'
    }
    mf = f"temp_metrics/{fn}.txt"
    if os.path.exists(mf):
        for l in open(mf):
            k,v = l.split(":",1)
            v = v.strip()
            lk = k.lower()
            if 'work experience' in lk:    metrics['work_exp']=v
            elif 'education score' in lk:  metrics['education']=v
            elif 'skills score' in lk:     metrics['skills']=v
            elif 'keyword score' in lk:    metrics['keywords']=v
            elif 'formatting score' in lk: metrics['formatting']=v
            elif 'final cv score' in lk:   metrics['final_score']=v
            elif 'readability score' in lk:metrics['readability']=v
            elif 'jd keywords matched' in lk:metrics['jd_matches']=v
            elif 'extracted skills' in lk: metrics['top_skills']=v
    return metrics

# def send_feedback(email_to, m):
#     msg = MIMEMultipart()
#     msg['From']    = EMAIL_USER
#     msg['To']      = email_to
#     msg['Subject'] = f"Feedback: {m['filename']}"
#     body = f"""
#     <p>Hi,</p>
#     <p>Your resume <strong>{m['filename']}</strong> scored <strong>{m['final_score']}/100</strong>.</p>
#     <ul>
#       <li>Work: {m['work_exp']}</li>
#       <li>Education: {m['education']}</li>
#       <li>Skills: {m['skills']}</li>
#       <li>Keywords: {m['keywords']}</li>
#       <li>Formatting: {m['formatting']}</li>
#       <li>Readability: {m['readability']}</li>
#       <li>JD Matches: {m['jd_matches']}</li>
#       <li>Top Skills: {m['top_skills']}</li>
#     </ul>
#     """
#     msg.attach(MIMEText(body,'html'))
#     try:
#         with smtplib.SMTP_SSL('smtp.gmail.com',465) as s:
#             s.login(EMAIL_USER,EMAIL_PASS)
#             s.send_message(msg)
#         logging.info(f"Sent to {email_to}")
#     except Exception as e:
#         logging.error(f"Failed to {email_to}: {e}")
def send_feedback(to_email, metrics):
    subject = f"📄 Feedback on Your Resume: {metrics['filename']}"

    body = f"""
    <html>
    <body>
    <p>Hello,</p>
    <p>Thank you for submitting your resume. Here is your CV evaluation:</p>
    <ul>
        <li><strong>Resume Name:</strong> {metrics['filename']}</li>
        <li><strong>Work Experience Score:</strong> {metrics['work_exp']}</li>
        <li><strong>Education Score:</strong> {metrics['education']}</li>
        <li><strong>Skills Score:</strong> {metrics['skills']}</li>
        <li><strong>Keyword Score:</strong> {metrics['keywords']}</li>
        <li><strong>Formatting Score:</strong> {metrics['formatting']}</li>
        <li><strong>Readability Score:</strong> {metrics['readability']}</li>
        <li><strong>Final CV Score:</strong> {metrics['final_score']}/100</li>
        <li><strong>JD Keywords Matched:</strong> {metrics['jd_matches']}</li>
        <li><strong>Top Extracted Skills:</strong> {metrics['top_skills']}</li>
    </ul>
    <p>This evaluation is based on your resume’s content and its alignment with the job description.</p>
    <p>If you’d like personalized tips or have questions, feel free to reply to this email.</p>
    <p>Best of luck with your job search!</p>
    <p>Warm regards,<br>HR Team</p>
    </body>
    </html>
    """

    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    try:
        logging.info(f"Sending feedback to: {to_email}")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
        logging.info(f"✅ Feedback sent to {to_email}")
    except Exception as e:
        logging.error(f"❌ Failed to send email to {to_email}: {e}")

def process_feedback():
    if not os.path.exists('resume_scores.txt'):
        logging.error("No scores to email.")
        return
    for line in open('resume_scores.txt'):
        if 'Final CV Score:' not in line: continue
        m = parse_metrics_from_file(line)
        sender = m['filename'].split('_')[0]
        if re.match(r"[^@]+@[^@]+\.[^@]+", sender):
            send_feedback(sender, m)
        else:
            logging.warning(f"Bad email: {sender}")
