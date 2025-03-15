import requests, argparse, openai, os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

def read_job_urls(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines

if __name__ == "__main__":

    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    client = openai.OpenAI()
    parser = argparse.ArgumentParser()
    parser.add_argument('input_jobs', help='List of job URLs')
    args = parser.parse_args()

    jobs = read_job_urls(args.input_jobs)
    first_job = jobs[0]
