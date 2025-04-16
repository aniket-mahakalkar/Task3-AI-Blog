# AI_Blog_Generator-Task3


# 🚀 Streamlit + OpenAI + Selenium App

This application integrates **Streamlit** for a user-friendly interface, **OpenAI's API** for language generation, and **Selenium** for browser automation. It is designed to take user input, process it using OpenAI models, and optionally automate browser-based tasks like scraping or web interaction.

---

## 🧠 How the App Works

1. **User Input via Streamlit**  
   - The app provides a clean and interactive web UI using Streamlit.
   - Users can type in prompts or commands into a text field.

2. **OpenAI API Integration**  
   - Once the user submits a prompt, the app sends it to the OpenAI API.
   - The OpenAI model processes the prompt and returns a response.
   - The response is displayed instantly on the Streamlit interface.

3. **Selenium Automation (Optional)**  
   - If enabled, the app can trigger Selenium-based scripts.
   - These scripts can navigate web pages, extract data, or simulate clicks and input on websites.
   - `webdriver-manager` is used to handle browser drivers automatically.

4. **Environment Variables**  
   - API keys and other sensitive configurations are stored in a `.env` file.
   - The `python-dotenv` library loads these values securely into the app at runtime.

---

## 📦 Prerequisites

- Python 3.7+
- `pip` installed
- OpenAI API Key

---

## 🔧 Installation

1. **Clone the Repository**  
   ```bash
   git clone <your_repo_url>
   cd <your_project_folder>

**To Run the code :**
```bash
pip install -r requirements.txt
streamlit run Blog_Generator.py
    
