import requests
import argparse
import os
import openai
import re
from bs4 import BeautifulSoup
from dotenv import load_dotenv

def read_job_urls(file_path):
    """Reads job URLs from a file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

if __name__ == "__main__":

    client = openai.OpenAI()
    parser = argparse.ArgumentParser()
    parser.add_argument('input_jobs', help='Path to file with job URLs')
    args = parser.parse_args()

    job_urls = read_job_urls(args.input_jobs)

    for url in job_urls:
        job_posting_response = client.responses.create(
            model="gpt-4o-mini",
            tools=[{"type": "web_search_preview"}],
            input=f"Find the job title, company, and location for this URL: {url}. Output the results in this format: Position: <position>\nCompany: <company>\nLocation: <location>"
        )

        job_posting = job_posting_response.output_text.split("\n")

        job_position = job_posting[0].split(": ")[1]
        job_company = job_posting[1].split(": ")[1]
        job_location = job_posting[2].split(": ")[1]

        print("Title:", job_position)
        print("Company:", job_company)
        print("Location:", job_location)

        relevant_ppl = client.responses.create(
            model="gpt-4o-mini",
            tools=[{"type": "web_search_preview"}],
            input=f"Google Search for SWE managers at Apple working in Cupertino. Output the results in this format: Name: <name>\nLinkedin URL: <url>"
        )

        print(relevant_ppl.output_text)

        # TODO: Add response text to a JSON file
