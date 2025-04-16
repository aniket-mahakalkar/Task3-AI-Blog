import streamlit as st
import requests
import time
import os
import openai
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Step 1: Scraping Amazon Top Products
def download_image(image_url, save_path):
    try:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        with open(save_path, "wb") as f:
            f.write(response.content)
        print(f"Image saved to: {os.path.abspath(save_path)}")
        return True
    except Exception as e:
        print(f"Error downloading image: {e}")
        return False

def get_top_products():
    Top_products = []
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.amazon.in/gp/bestsellers/beauty")
    time.sleep(3)
    elements = driver.find_elements(By.ID, "gridItemRoot")

    for ele in elements[:5]:
        title = ele.text
        anchor = ele.find_element(By.CSS_SELECTOR, "a.a-link-normal.aok-block")
        href = anchor.get_attribute("href")
        img = ele.find_element(By.TAG_NAME, "img")
        img_src = img.get_attribute("src")
        path = img_src[-36:]
        Top_products.append({
            "title": title,
            "link": href,
            "image": img_src,
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

# Step 3: Generate Blog Post with OpenAI GPT-3
openai.api_key = "sk-proj-My api key was here"  # Insert your OpenAI API key here

def generate_blog_post(keywords):
    prompt = f"Write a 150-200 word blog post about a product based on the following keywords: {', '.join(keywords)}. Make it engaging and natural."
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Or use other models like "gpt-3.5-turbo"
            prompt=prompt,
            max_tokens=250,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        st.error(f"Error generating blog post: {e}")
        return ""

# Save Keywords to CSV (Step 4)
def save_keywords_to_csv(product_title, keywords, filename="seo_keywords.csv"):
    with open(filename, "a", newline='') as file:
        writer = csv.writer(file)
        for keyword in keywords:
            writer.writerow([product_title, keyword])

# Streamlit app
def main():
    st.title("AI-based Blog Creation Tool")

    # Step 1: Get Top Products
    st.subheader("Top Amazon Bestselling Products")
    top_products = get_top_products()

    for product in top_products:
        st.write(f"**{product['title']}**")
        st.image(product['image'], caption=product['title'])
        st.markdown(f"[View Product]({product['link']})")

    # Step 2: User Input for Product Name
    product_name = st.text_input("Enter a Product Name for SEO Keywords:")
    if product_name:
        st.subheader("Fetching SEO Keyword Suggestions...")
        keywords = google_autocomplete_keywords(product_name)

        if keywords:
            st.write("Top Keywords:")
            for keyword in keywords:
                st.write(f"- {keyword}")

            # Save keywords to CSV
            save_keywords_to_csv(product_name, keywords)
            
            # Step 3: Generate Blog Post
            st.subheader("Generated Blog Post:")
            blog_post = generate_blog_post(keywords)
            st.write(blog_post)

            # Option to download the blog post
            st.download_button(
                label="Download Blog Post",
                data=blog_post,
                file_name=f"{product_name}_blog_post.txt",
                mime="text/plain"
            )

if __name__ == "__main__":
    main()
