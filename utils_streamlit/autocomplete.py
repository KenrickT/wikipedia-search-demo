import ast
import pandas as pd
from openai import OpenAI

import streamlit as st

import os
from dotenv import load_dotenv
load_dotenv()

def get_autocomplete_df(filepath):
    try:
        df_autocomplete = pd.read_csv(filepath)
    except:
        df_autocomplete = pd.DataFrame()

    return df_autocomplete


def filter_autocomplete_df(df_autocomplete, search_input):
    return df_autocomplete[df_autocomplete["search_phrase"]==search_input].reset_index(drop=True)


def generate_autocomplete_results(text: str, topic: str) -> list:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    prompt = f"""Provide 2 autocompleted phrases for {text}, related to Wikipedia articles about {topic}. Show the output as a python list."""

    messages = [
        {"role": "system", "content": "You are a search engine focused on autocomplete."},
        {"role": "user", "content": prompt}
    ]
    chat = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages, max_tokens=40)
    response = ast.literal_eval(chat.choices[0].message.content)
    response = [text.lower() for text in response]

    return [
        {
            "search_phrase": text,
            "autocomplete_topic": topic,
            "autocomplete_phrase": autocomplete_phrase
        }
        for autocomplete_phrase in response
    ]


def create_autocomplete_df(autocomplete_filepath, search_input, topics_list):
    df_autocomplete = get_autocomplete_df(autocomplete_filepath)
    df_autocomplete_preloaded = filter_autocomplete_df(df_autocomplete, search_input)

    if len(df_autocomplete_preloaded) == 0:
        autocomplete_suggestions = [generate_autocomplete_results(search_input, topic) for topic in topics_list]
        autocomplete_suggestions = [element for sublist in autocomplete_suggestions for element in sublist]
        autocomplete_suggestions = pd.DataFrame(autocomplete_suggestions)
        df_autocomplete = pd.concat([df_autocomplete, autocomplete_suggestions], axis=0).reset_index(drop=True)
        df_autocomplete.to_csv(autocomplete_filepath, index=False)


def create_selections_dataframe(df, relevant_columns, search_input):
    df_with_selections = df[relevant_columns].copy()
    df_with_selections.loc[len(df_with_selections)] = search_input
    df_with_selections = pd.concat([df_with_selections.iloc[[-1]], df_with_selections.iloc[:-1]], ignore_index=True)
    df_with_selections = df_with_selections.rename(columns={"autocomplete_phrase":"Did you mean:"})

    # Get dataframe row-selections from user with st.data_editor
    df_with_selections.insert(0, "Select", False)
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={"Select": st.column_config.CheckboxColumn(required=True)},
        disabled=df.columns,
    )

    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = edited_df[edited_df.Select]
    return selected_rows.drop('Select', axis=1)