import openai

openai.api_key = "sk-pro 'My Api key was Here' "  # Insert your OpenAI API key here
def generate_blog_post(product_details, keywords):
    title = product_details["title"]
    description = product_details.get("description", "No description available.")
    features = product_details.get("features", "No features available.")
    
    prompt = f"""
    Write a 300-word blog post about the product '{title}'. The post should:
    - Start with an engaging introduction that talks about the importance and benefits of the product.
    - Highlight key features and benefits of the product naturally, focusing on what makes it stand out.
    - Incorporate the following SEO keywords in a natural way: {', '.join(keywords)}.
    - Provide readers with actionable insights, like why they should buy or how it can help them.
    - End with a conclusion encouraging readers to purchase or learn more about the product.
    
    Here are the product details to help:
    
    Product Title: {title}
    Product Description: {description}
    Product Features: {features}
    SEO Keywords: {', '.join(keywords)}
    """

    try:
        response = openai.openai.completions.create(
            model="gpt-4",  # or any suitable model you wish to use
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error generating blog post: {e}"

# Example Usage:
product_details = {
    "title": "Echo Dot 5th Gen",
    "description": "Echo Dot 5th Gen is a smart speaker with Alexa, offering superior sound quality and hands-free voice control.",
    "features": "Compact design, superior sound quality, hands-free Alexa voice control, smart home integration."
}

keywords = ["Echo Dot 5th Gen", "smart speaker", "Alexa", "voice control", "compact design"]

blog_post = generate_blog_post(product_details, keywords)
print(blog_post)