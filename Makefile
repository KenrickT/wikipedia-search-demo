install:
	pip install -r requirements.txt
	python -m spacy download en_core_web_lg

run:
	venv/bin/python -m streamlit run app.py

scrape:
	venv/bin/python ./utils_data_source/generate_csv.py