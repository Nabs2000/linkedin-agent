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
    job_scraper_agent = client.beta.assistants.create(
        name="Job Scraping Assistant",
        instructions="You are an expert in obtaining job details from their websites. Use your ability to scrape the Internet to obtain these details.",
        model="gpt-4o",
        tools=[{"type": "file_search"}],
    )

    parser = argparse.ArgumentParser()
    parser.add_argument('input_jobs', help='List of job URLs')
    args = parser.parse_args()

    jobs = read_job_urls(args.input_jobs)

    # Upload the user provided file to OpenAI
    message_file = client.files.create(
        file=open(args.input_jobs, "rb"), purpose="assistants"
    )

    # Create a thread and attach the file to the message
    thread = client.beta.threads.create(
    messages=[
        {
        "role": "user",
        "content": "Please tell me the job title, company, and location.",
        # Attach the new file to the message.
        "attachments": [
            { "file_id": message_file.id, "tools": [{"type": "file_search"}] }
        ],
        }
    ]
    )

    # The thread now has a vector store with that file in its tool resources.
    print(thread.tool_resources.file_search)

    # Use the create and poll SDK helper to create a run and poll the status of
    # the run until it's in a terminal state.

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id, assistant_id=job_scraper_agent.id
    )

    messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

    message_content = messages[0].content[0].text
    annotations = message_content.annotations
    citations = []
    for index, annotation in enumerate(annotations):
        message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
        if file_citation := getattr(annotation, "file_citation", None):
            cited_file = client.files.retrieve(file_citation.file_id)
            citations.append(f"[{index}] {cited_file.filename}")

    print(message_content.value)
    print("\n".join(citations))

