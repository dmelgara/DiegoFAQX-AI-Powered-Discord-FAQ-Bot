import openai

with open("openaiAPI.txt") as file:
    openai.api_key = file.read().strip()

def classify_utterance(utterance):
    """
    Uses the completion model to classify the type of user input.
    """
    prompt = f"""Classify the following user message into one of the following categories:
    - faq: if it's a factual question about Canada
    - greeting: if it's a hello-type message
    - farewell: if it's a goodbye message
    - off-topic: if it's not related to Canada at all

    Message: "{utterance}"
    Category:"""

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=5,
        temperature=0.3
    )

    return response.choices[0].text.strip().lower()

def generate_response(utterance):

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant that answers questions about Canada. "
                "Keep your responses short and concise."
            )
        },
        {
            "role": "user",
            "content": utterance
        }
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=150,
        temperature=0.3
    )

    return response.choices[0].message.content.strip()
