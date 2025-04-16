import streamlit as st
import requests
import time
import os
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# Step 1: Scrape Amazon Bestselling Products
def get_top_products():
    Top_products = []
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.amazon.in/gp/bestsellers/beauty")
    time.sleep(3)
    elements = driver.find_elements(By.ID, "gridItemRoot")

    for ele in elements[:3]:
        title = ele.text
        anchor = ele.find_element(By.CSS_SELECTOR, "a.a-link-normal.aok-block")
        href = anchor.get_attribute("href")
        Top_products.append({
            "title": title,
            "link": href,
        })
    driver.quit()
    return Top_products

# Step 2: Google Autocomplete Keywords
def google_autocomplete_keywords(query):
    url = "http://suggestqueries.google.com/complete/search"
    params = {"client": "firefox", "q": query}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        suggestions = response.json()[1]
        return suggestions[:5]
    else:
        return []

# Step 3: Generate Blog Post with OpenAI
def generate_combined_blog(product_infos):
    formatted_products = "\n\n".join([
        f"- **{p['title']}**\n  - Description: {p['description']}\n  - Features: {p['features']}\n  - Keywords: {', '.join(p['keywords'])}"
        for p in product_infos
    ])

    prompt = f"""
Write a 400-500 word blog post introducing the top 3 bestselling beauty products on Amazon India. The post should:
- Mention that these are top-rated and trending products on Amazon India.
- Begin with a warm, engaging introduction on why choosing the right beauty products matters.
- Briefly highlight each of the three products with their unique features and benefits.
- Naturally incorporate relevant SEO keywords throughout.
- Conclude with encouragement for the reader to explore or buy the products.

Here are the product details:

{formatted_products}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert blog writer skilled in SEO and product storytelling."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=700
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating combined blog post: {e}"


# Save Keywords to CSV
def save_keywords_to_csv(product_title, keywords, filename="seo_keywords.csv"):
    with open(filename, "a", newline='') as file:
        writer = csv.writer(file)
        for keyword in keywords:
            writer.writerow([product_title, keyword])

# Streamlit App
def main():
    st.title("AI-Powered Blog Generator for Top Selling Amazon Beauty Products")

    # Step 1: Scrape Top Products
    st.subheader("Scraping Amazon Bestselling Beauty Products...")
    top_products = get_top_products()

    product_infos = []

    for product in top_products:
        st.markdown(f"### {product['title']}")
        st.markdown(f"[View Product on Amazon]({product['link']})")

        # Step 2: Fetch SEO Keywords
        keywords = google_autocomplete_keywords(product['title'])
        if not keywords:
            keywords = []

        st.markdown("**SEO Keywords:**")
        st.write(", ".join(keywords))

        # Save keywords to CSV
        save_keywords_to_csv(product['title'], keywords)

        # Prepare product details for combined blog
        product_details = {
            "title": product['title'],
            "description": "A bestselling beauty product in India, known for its quality and popularity.",
            "features": "Trusted by thousands, suitable for daily use, gentle on skin.",
            "keywords": keywords
        }
        product_infos.append(product_details)

    # Step 3: Generate a Combined Blog Post
    if product_infos:
        st.markdown("## 📝 Generated Blog Post")
        combined_blog = generate_combined_blog(product_infos)
        st.write(combined_blog)

        # Download Button
        st.download_button(
            label="Download Blog Post",
            data=combined_blog,
            file_name="bestselling_beauty_products_blog.txt",
            mime="text/plain"
        )


if __name__ == "__main__":
    main()
