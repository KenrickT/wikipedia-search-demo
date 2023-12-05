from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor

import os
from dotenv import load_dotenv
load_dotenv()

import spacy
nlp = spacy.load("en_core_web_lg")


def clean_text(text:str) -> str:
    doc = nlp(text)
    return " ".join(token.lemma_ for token in doc if not token.is_stop and not token.is_punct and not token.is_space)


def vectorize_text(text:str) -> object:
    return nlp(text)


def shorten_paragraph(text:str, max_tokens:int) -> str:

    if len(text) > 1000:
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        prompt = f"Quickly summarize this paragraph to less than 1000 characters: {text}"
        messages = [
            {"role": "system", "content": "You are a journalist focus on summarizing text."},
            {"role": "user", "content": prompt}
        ]
        chat = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages, max_tokens=max_tokens)
        return str(chat.choices[0].message.content)

    elif len(text) > 500:
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        prompt = f"Quickly summarize this paragraph to less than 500 characters: {text}"
        messages = [
            {"role": "system", "content": "You are a journalist focus on summarizing text."},
            {"role": "user", "content": prompt}
        ]
        chat = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages, max_tokens=max_tokens)
        return str(chat.choices[0].message.content)
    
    else:
        return text


def split_text_into_chunks(text: str, chunk_size: int) -> list:
    doc = nlp(text)
    chunks = []
    current_chunk = []
    current_chunk_size = 0

    for token in doc:
        current_chunk.append(token.text_with_ws)
        current_chunk_size += 1

        if current_chunk_size >= chunk_size:
            chunks.append("".join(current_chunk))
            current_chunk = []
            current_chunk_size = 0

    if current_chunk:
        chunks.append("".join(current_chunk))

    return chunks


def summarize_paragraph(text:str, max_tokens:int) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = f"Summarize: {text}"
    messages = [
        {"role": "system", "content": "You are an assistant focused on summarizing."},
        {"role": "user", "content": prompt}
    ]
    chat = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages, max_tokens=max_tokens)
    return str(chat.choices[0].message.content)


def generate_copilot_summary(top_result_full_text: str) -> str:
    chunks = split_text_into_chunks(top_result_full_text, chunk_size=1500)
    
    with ThreadPoolExecutor(max_workers=100) as executor:
        summary_subsets = list(executor.map(summarize_paragraph, chunks, [500] * len(chunks)))
    
    return summarize_paragraph("".join(summary_subsets), max_tokens=1000)