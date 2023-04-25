import openai
import requests
from bs4 import BeautifulSoup



api_key = "enter your api key"

model_engine = "text-davinci-002"  # Use a pre-trained model specifically designed for generating questions

openai.api_key = api_key

# Define the URL to fetch
url = "https://newsroom.ucla.edu/stories/jackie-robinson-75th-anniversary-integrated-baseball#:~:text=Robinson%20won%20a%20World%20Series,first%20year%20on%20the%20ballot"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
text = soup.get_text()
# print("text===============",text)
# Use OpenAI GPT API to generate questions based on scraped text
response = openai.Completion.create(
    engine=model_engine,
    prompt=f"Generate 5 questions about the following:{text}",
    temperature=0.5,
    max_tokens=150,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    n =1,
    stop=None,  # Stop generating questions when a question mark is detected
)

# Filter and sort the generated questions
questions = [q.strip() for q in response.choices[0].text.split("\n") if q.strip() != "" and "?" in q]
questions = sorted(set(questions), key=len)

for i, question in enumerate(questions[:5]):
    print(f"{i+1}. {question}")
