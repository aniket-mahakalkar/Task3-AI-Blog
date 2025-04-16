import requests

def google_autocomplete_keywords(query):
    url = "http://suggestqueries.google.com/complete/search"
    params = {"client": "firefox", "q": query}
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        suggestions = response.json()[1]
        return suggestions[:5]  # Top 5 keyword ideas
    else:
        return []

# Example usage
keywords = google_autocomplete_keywords("Simple Kind To Skin Refreshing Face Wash 150 ml")
print(keywords)

import requests

def get_autocomplete_keywords(product_title, max_results=5):
    """
    Uses Google Autocomplete to get related keyword suggestions.
    
    Args:
        product_title (str): The product name or topic.
        max_results (int): Number of keyword suggestions to return.
    
    Returns:
        List[str]: A list of keyword suggestion strings.
    """
    url = "http://suggestqueries.google.com/complete/search"
    params = {
        "client": "firefox",  # lightweight JSON response
        "q": product_title
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        suggestions = response.json()[1]
        return suggestions[:max_results]
    
    except requests.RequestException as e:
        print(f"Error fetching keywords: {e}")
        return []

# Example usage
if __name__ == "__main__":
    product = "Echo Dot 5th Gen"
    keywords = get_autocomplete_keywords(product)
    print("Keyword Suggestions:")
    for kw in keywords:
        print("-", kw)
import csv

def save_keywords_to_csv(product_title, keywords, filename="seo_keywords.csv"):
    with open(filename, "a", newline='') as file:
        writer = csv.writer(file)
        for keyword in keywords:
            writer.writerow([product_title, keyword])
