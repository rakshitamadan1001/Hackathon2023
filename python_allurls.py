import openai
import requests
from bs4 import BeautifulSoup
import random

api_key = "Enter your open AI key"

model_engine = "text-davinci-002"  # Use a pre-trained model specifically designed for generating questions

openai.api_key = api_key

urls = [ "https://www.tennis365.com/tennis-features/how-tennis-changed-from-white-to-yellow-tennis-balls-thanks-to-david-attenborough/", 
        "https://www.nytimes.com/2016/05/08/sports/tennis/even-four-years-later-bad-feelings-linger-over-the-blue-clay-in-", 
        "https://www.theguardian.com/travel/gallery/2017/mar/09/outdoor-swimming-paris-canals-river-seine-outdoor-swimming-societys"]

combined_text = ""
for url in urls:
    # Randomly select a URL from the list of URLs
    url = random.choice(urls)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text()
    combined_text += text


    response = openai.Completion.create(
        engine=model_engine,
        prompt=f"Generate 1 question from the following websites: {urls}",
        temperature=1.0,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        n=1,
        stop=None,  # Stop generating questions when a question mark is detected
    )
    qa_pairs = [q.strip() for q in response.choices[0].text.split("\n") if q.strip() != ""]
    qa_pairs = [qa_pair.split("?") for qa_pair in qa_pairs if len(qa_pair.split("?")) == 2]
    qa_pairs = [(q.strip() + "?", a.strip()) for q, a in qa_pairs]

    questions = [q.strip() for q in response.choices[0].text.split("\n") if q.strip() != "" and "?" in q]
    questions = sorted(set(questions), key=len)

    for i, (question, answer) in enumerate(qa_pairs[:5], start=1):
        print(f"Q{i}. {question}")
    user_answer = input("Your answer: ")
    if user_answer.lower().strip() == answer.lower().strip():
        print("Correct!")
    else:
        print(f"Wrong. The correct answer is: {answer}")
