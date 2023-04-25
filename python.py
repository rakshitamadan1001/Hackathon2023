import openai
import requests
from bs4 import BeautifulSoup

api_key = "enter your api key"

model_engine = "text-davinci-002"  # Use a pre-trained model specifically designed for generating questions

openai.api_key = api_key

url = "https://www.tennis365.com/tennis-features/how-tennis-changed-from-white-to-yellow-tennis-balls-thanks-to-david-attenborough/"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
text = soup.get_text()

response = openai.Completion.create(
    engine=model_engine,
    prompt=f"You are a quiz master, Generate 5 multiple choice questions with 4 answer options each about the following:{text}",
    temperature=0.5,
    max_tokens=300,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    n=1,
    stop=None,
)

mcq_pairs = [q.strip() for q in response.choices[0].text.split("\n") if q.strip() != ""]
mcq_pairs = [mcq_pair.split("?") for mcq_pair in mcq_pairs if len(mcq_pair.split("?")) == 2]
mcq_pairs = [(q.strip() + "?", a.strip()) for q, a in mcq_pairs]

for i, (question, answer_options) in enumerate(mcq_pairs[:5], start=1):
    print(f"Q{i}. {question}")
    options = answer_options.split(";")
    for j, option in enumerate(options, start=1):
        print(f"{j}. {option.strip()}")