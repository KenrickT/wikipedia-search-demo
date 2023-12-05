import pandas as pd
import streamlit as st

from utils_streamlit.load_data import load_data
from utils_streamlit.file_upload import push_new_data
from utils_streamlit.autocomplete import get_autocomplete_df, filter_autocomplete_df, create_autocomplete_df, create_selections_dataframe
from utils_data_source.process_text import clean_text, vectorize_text, shorten_paragraph, split_text_into_chunks, generate_copilot_summary

#################################################################################

df = load_data()
topics_list = df["topic"].unique().tolist()
st.title('Wikipedia Search Tool')

#################################################################################

AUTOCOMPLETE_FILEPATH = "./data/autocomplete_data.csv"
WIKIPEDIA_FILEPATH = "./data/wikipedia_data.csv"

search_input = st.text_input(label="search_bar", label_visibility="hidden")
autocomplete = st.button("Auto-complete", type="primary")
search_term = ""

if len(search_input) > 0:
    # generate autocomplete suggestions
    if autocomplete is True:
        create_autocomplete_df(AUTOCOMPLETE_FILEPATH, search_input, topics_list)

    # select search option from autocomplete suggestions
    try:
        df_autocomplete = get_autocomplete_df(AUTOCOMPLETE_FILEPATH)
        df_autocomplete_results = filter_autocomplete_df(df_autocomplete, search_input)
        
        if len(df_autocomplete_results)>0:
            selection = create_selections_dataframe(df_autocomplete_results, ["autocomplete_phrase"], search_input)
            selection_count = len(selection)
            
            if selection_count == 1:
                search_term = str(selection.iloc[0,0])
            elif selection_count >= 2:
                st.warning("select only 1 search term", icon="⚠️")

    except:
        pass

    st.divider()

    #################################################################################
    
    max_results = 20
    if len(search_term)>0:
        st.markdown(f"### {max_results} Search Results for `{search_term}`")
        st.markdown("**Quick Filters**")
        
        # setup search result filters and buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            focus = st.selectbox("Search Focus", options=[""]+topics_list)
            copilot = st.button("Co-Pilot", help="Click this for a summary of the top result.")
        with col3:
            new_file = st.file_uploader("Add File", help="Upload a CSV File with `url` column", type=".csv", accept_multiple_files=False)
            if new_file is not None:
                new_data = pd.read_csv(new_file)
                try:
                    new_data = new_data[["topic","url"]]
                    push_new_data(df, new_data, WIKIPEDIA_FILEPATH)
                except:
                    st.warning("Upload a CSV File with `topic` and `url` column")
        st.divider()

        # sort by cosine similarity
        df_results = df.copy()
        df_results["similarity"] = df_results["summary"].apply(lambda x: vectorize_text(clean_text(search_term)).similarity(vectorize_text(clean_text(x))))
        df_results = df_results.sort_values(by="similarity", ascending=False).reset_index(drop=True)

        # filter by Search Focus
        if len(focus) > 0:
            df_results = df_results[df_results["topic"]==focus].reset_index(drop=True)

        # copilot top result  
        if copilot is True:
            full_text = df_results.head(1)["full_page_text"].iloc[0]
            copilot_summary = generate_copilot_summary(full_text)
            
            st.write("#### Co-Pilot Summary:")
            st.write(copilot_summary)
            st.markdown(f"_Read more on: {df_results.head(1)["url"].iloc[0]}_")
        
        # show all results      
        else:
            for idx, row in df_results.head(max_results).iterrows():
                st.markdown(f"#### {row["title"]}\n`Category: {row["topic"]}`")
                st.markdown(row["summary_short"])
                st.markdown(f"_Read more on: {row["url"]}_")
                st.divider()

else:
    pass
