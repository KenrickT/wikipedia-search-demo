import pandas as pd
from urllib.parse import urlparse
from utils_data_source.fetch_data import fetch_wikipedia_data, get_wikipedia_full_page_text
from utils_data_source.process_text import shorten_paragraph

def get_wikipedia_title_from_url(wikipedia_url):
    parsed_url = urlparse(wikipedia_url)
    path_segments = parsed_url.path.split('/')
    
    # Find the segment that contains the title
    title_segment_index = path_segments.index('wiki') + 1 if 'wiki' in path_segments else None
    
    if title_segment_index is not None and title_segment_index < len(path_segments):
        return path_segments[title_segment_index].replace('_', ' ')
    else:
        print("Invalid Wikipedia URL")
        return None


def push_new_data(old_data, new_data, filepath):

    new_data["title"] = new_data["url"].apply(get_wikipedia_title_from_url)
    new_data["summary"] = new_data["title"].apply(lambda x: fetch_wikipedia_data(x)["summary"])
    new_data["summary_short"] = new_data["summary"].apply(lambda x: shorten_paragraph(x, max_tokens=80))
    new_data["full_page_text"] = new_data["title"].apply(get_wikipedia_full_page_text)

    df = pd.concat([old_data, new_data], axis=0).drop_duplicates(subset="url", keep="first").reset_index(drop=True)
    df.to_csv(filepath)