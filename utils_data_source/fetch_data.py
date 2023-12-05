import requests

def search_wikipedia_pages(topic: str) -> list:
    base_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": topic,
        "srlimit": 34
    }

    response = requests.get(base_url, params=params, timeout=100)
    data = response.json()

    if "query" in data and "search" in data["query"]:
        return data["query"]["search"]
    else:
        return []


def select_wikipedia_titles(topics_list: list) -> list:
    return [
        {
            "topic": topic,
            "title": page["title"],
        }
        for topic in topics_list
        for page in search_wikipedia_pages(topic)
    ]


def fetch_wikipedia_data(title: str) -> dict:
    base_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts|info",
        "inprop": "url",
        "exintro": True,
        "explaintext": True,
        "titles": title
    }

    response = requests.get(base_url, params=params, timeout=100)
    data = response.json()

    if "-1" in data["query"]["pages"]:
        print("Page not found.")
        return None

    page_id = list(data["query"]["pages"].keys())[0]
    page_info = data["query"]["pages"][page_id]

    return {
        "title": page_info["title"],
        "summary": page_info["extract"],
        "url": page_info["fullurl"]
    }


def parse_wikipedia_data(titles_list: list) -> list:
    return [
      {
          "topic": title["topic"],
          "title": title["title"],
          "url": fetch_wikipedia_data(title["title"])["url"],
          "summary": fetch_wikipedia_data(title["title"])["summary"]
      }
      for title in titles_list
    ]


def get_wikipedia_full_page_text(title: str) -> str:

    base_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "titles": title,
        "explaintext": True
    }

    response = requests.get(base_url, params=params)
    data = response.json()
    page = next(iter(data['query']['pages'].values()))
    content = page['extract'] if 'extract' in page else "Page not found!"

    return content