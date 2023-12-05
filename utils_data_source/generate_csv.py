import pandas as pd
from fetch_data import select_wikipedia_titles, parse_wikipedia_data, get_wikipedia_full_page_text
from process_text import clean_text, shorten_paragraph, generate_copilot_summary

topics = ["Japanese Food", "Artificial Intelligence", "Space Exploration"]
titles_list = select_wikipedia_titles(topics)[0:100]
page_data = parse_wikipedia_data(titles_list)

df = pd.DataFrame(page_data)
df["summary_short"] = df["summary"].apply(lambda x: shorten_paragraph(x, max_tokens=80))
df["full_page_text"] = df["title"].apply(get_wikipedia_full_page_text)

df.to_csv(r'./data/wikipedia_data.csv', index=False)
print("Loaded",len(df),"data points.")