"""
Diego Melgara, FEB 2025
"""
import sys
import os
import string
import spacy
import regex as re
from gptAPI import classify_utterance, generate_response

nlp = spacy.load("en_core_web_sm")

def preprocess(text):
    """Converts text to lowercase, strips whitespace, and removes punctuation."""
    text = text.lower().strip()
    return text.translate(str.maketrans("", "", string.punctuation))

def file_input(filename):
    filepath = f"./data/{filename}"
    print(f"Trying to open: {filepath}")
    try:
        with open(filepath, encoding="utf-8") as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        print(f"ERROR: File '{filename}' not found!")
        return []

def load_FAQ_data():
    """Loads questions, answers, and regex patterns from text files."""
    questions = file_input("questions.txt")
    answers = file_input("answers.txt")
    regex_patterns = file_input("regex.txt")
    return questions, answers, regex_patterns

global intents, responses, regex_patterns
intents, responses, regex_patterns = load_FAQ_data()

def understand(utterance):
    global regex_patterns
    processed = preprocess(utterance)
    best_match = None
    best_score = 0
    for index, pattern in enumerate(regex_patterns):
        try:
            compiled_regex = re.compile(pattern, re.IGNORECASE | re.BESTMATCH)
            match = compiled_regex.search(processed)
            if match:
                match_score = len(match.group()) - sum(match.fuzzy_counts)
                if match_score > best_score:
                    best_score = match_score
                    best_match = index
        except re.error as e:
            print(f"Invalid regex pattern on line {index + 1}: {pattern}")
            print(f"Regex Error: {e}")
    return best_match if best_match is not None else -1

def analyze_fallback(utterance):
    """Analyze unknown questions and provide a fallback response."""
    doc = nlp(utterance)
    # Extract named entities
    entities = [ent.text for ent in doc.ents]
    if entities:
        return f"Sorry, I don't have information about {', '.join(entities)}."
    # Extract noun phrases
    noun_chunks = [chunk.text for chunk in doc.noun_chunks if chunk.root.pos_ not in ["PRON"]]
    if noun_chunks:
        return f"Sorry, I don’t have details on {', '.join(noun_chunks)}."
    return "Sorry, I don’t understand that question."

def generate(intent, utterance=None):
    """Generates the appropriate response based on the detected intent."""
    global responses
    greetings = ["hello", "hi", "hey", "whats up", "hola"]
    if utterance and any(word in utterance.lower() for word in greetings):
        return "Hello! How can I help you today?"
    if utterance and utterance.lower() in ["goodbye", "bye", "see you", "quit", "exit"]:
        return "Nice talking to you!"
    # when there is nomatch, return -1, which calls OpenAI:
    if intent == -1:
        try:
            category = classify_utterance(utterance)
            if category == "off-topic":
                return "Sorry, that question is outside my scope. Try asking about Canada!"
        except Exception as e:
            print("Error during classification:", e)
        try:
            return generate_response(utterance)
        except Exception as e:
            print("Error generating response with OpenAI:", e)
            return analyze_fallback(utterance)
    else:
        return responses[intent]



# def main():
#     print("Hello! When you're done talking, just say 'goodbye'.\n")
#     while True:
#         utterance = input(">>> ").strip()
#         if utterance.lower() in ["goodbye", "bye", "see you", "quit", "exit"]:
#             print("Nice talking to you!")
#             sys.exit()
#         intent = understand(utterance)
#         print("Intent:", intent)
#         response = generate(intent, utterance)
#         print(response)
#         print()
#     print("Nice talking to you!")
#
# if __name__ == "__main__":
#     main()
