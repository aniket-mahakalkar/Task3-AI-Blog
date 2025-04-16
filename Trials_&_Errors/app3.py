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
apikey= "sk-proj-My Api key was Here"
# # Step 1: Scraping Amazon Bestselling Products

client = OpenAI(api_key=apikey)
# Cleaned-up Version: No Image Downloads, Only Blog Generation
import streamlit as st
import requests
import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import openai



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
def generate_blog_post(product_details, keywords):
    title = product_details["title"]
    description = product_details.get("description", "No description available.")
    features = product_details.get("features", "No features listed.")

    user_prompt = f"""
Write a 200-300 word blog post about the product '{title}'. The post should:
- Start with an engaging introduction about the product's purpose and appeal.
- Naturally incorporate these SEO keywords: {', '.join(keywords)}.
- Highlight unique features and benefits of the product.
- Conclude with a compelling call to action.

Product Title: {title}
Description: {description}
Features: {features}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional SEO blog writer."},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating blog post: {e}"

# Save Keywords to CSV
def save_keywords_to_csv(product_title, keywords, filename="seo_keywords.csv"):
    with open(filename, "a", newline='') as file:
        writer = csv.writer(file)
        for keyword in keywords:
            writer.writerow([product_title, keyword])



# Streamlit App
def main():
    st.title("🪞 AI-Powered Blog Generator for Amazon Beauty Products")
    top_products = get_top_products()
    combined_blog_md = "# 🌟 Top Amazon Beauty Bestsellers\n\n"

    for idx, product in enumerate(top_products, 1):
        st.subheader(f"#{idx}: {product['title']}")
        st.markdown(f"[🔗 View Product on Amazon]({product['link']})")

        keywords = google_autocomplete_keywords(product['title'])
        if keywords:
            st.markdown("**🔑 SEO Keywords:**")
            st.write(", ".join(keywords))

            save_keywords_to_csv(product['title'], keywords)

            product_details = {
                "title": product['title'],
                "description": "This bestselling beauty product is popular among Indian consumers for its quality and affordability.",
                "features": "Gentle on skin, budget-friendly, widely recommended."
            }
            blog_post = generate_blog_post(product_details, keywords)
            st.markdown("**📝 Generated Blog Post:**")
            st.markdown(blog_post)

            # Append blog post in markdown format
            combined_blog_md += f"## {product['title']}\n\n{blog_post}\n\n[View on Amazon]({product['link']})\n\n---\n"

    # Final combined blog download
    st.download_button(
        label="📥 Download Full Blog as Markdown",
        data=combined_blog_md,
        file_name="Amazon_Beauty_Blog.md",
        mime="text/markdown"
    )

if __name__ == "__main__":
    main()