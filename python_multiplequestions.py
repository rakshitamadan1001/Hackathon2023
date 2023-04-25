import openai
import requests
from bs4 import BeautifulSoup

api_key = "Enter your own API key"

model_engine = "text-davinci-002"  # Use a pre-trained model specifically designed for generating questions

openai.api_key = api_key

urls = [ "https://www.tennis365.com/tennis-features/how-tennis-changed-from-white-to-yellow-tennis-balls-thanks-to-david-attenborough/",
        "https://www.nytimes.com/2016/05/08/sports/tennis/even-four-years-later-bad-feelings-linger-over-the-blue-clay-in-",
        "https://www.theguardian.com/travel/gallery/2017/mar/09/outdoor-swimming-paris-canals-river-seine-outdoor-swimming-societys"]

for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text()

    response = openai.Completion.create(
        engine=model_engine,
        prompt=f"Generate 5 questions about the following:{text}",
        temperature=0.5,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        n=1,
        stop=None,  # Stop generating questions when a question mark is detected
    )

    questions = [q.strip() for q in response.choices[0].text.split("\n") if q.strip() != "" and "?" in q]
    questions = sorted(set(questions), key=len)

    print(f"Questions for {url}:")
    for i, question in enumerate(questions[:5], start=1):
        print(f"Q{i}. {question}")
    print("\n")

