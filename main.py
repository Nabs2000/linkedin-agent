import requests, argparse
from bs4 import BeautifulSoup

def read_job_urls(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('input_jobs', help='List of job URLs')
    args = parser.parse_args()

    jobs = read_job_urls(args.input_jobs)
    print(jobs)
