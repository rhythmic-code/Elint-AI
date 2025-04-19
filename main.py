
from collector import fetch_resumes, process_resumes
from score     import run_scoring
from feedback  import process_feedback

def main():
    # 1) Fetch & unpack new resumes
    records = fetch_resumes(limit=50)
    if not records:
        print("No new resumes found.")
        return

    # 2) Mask/inspect them
    process_resumes(records)

    # 3) Score them
    run_scoring()

    # 4) Send out feedback emails
    process_feedback()

if __name__ == "__main__":
    main()
