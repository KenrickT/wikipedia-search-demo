# wikipedia-search-demo
An exercise on scraping wikipedia articles, and building a rudimentary search tool using Streamlit.

# Instructions

## Install Requirements
Run `make install` to install important libraries and load spacy language model

## (preloaded) Scrape Wikipedia Data
Run `make scrape` to pull data from wikipedia and save the results as a CSV file.
A sample file is already included on the repo, so this step is more relevant when adding new topics.

## Run Streamlit App
run `make run` to begin the streamlit app demo.

# How it works

## Search Input
1. Begin with a search term (e.g. "food")
2. If the search term was already used before, recommended search terms are provided.
3. If no recommendations come up, click Auto-complete to generate new recommendations.
4. Select (via checkbox) the search term you want to go with (e.g. "space food").

## Search Results
1. By default, ranked search results come out on the bottom part of the page.
2. There is an option to filter the search results by stricter categories (via "Search Focus" Dropdown)
3. There is an option to generate a summary for the top-result (via Co-pilot Button). This typically takes around 30-40 seconds to run.

## Additional Feature
1. A user can also manually upload data using CSV files with columns "topic" and "url"
2. Uploading a wikipedia URL will automatically scrape the relevant pages' data and append the results to the existing (csv) dataset.
