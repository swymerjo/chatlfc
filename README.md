# ChatLFC

ChatLFC is a an AI application built using Streamlit and Langchain. It provides users with information about Liverpool FC's current 2024/25 season, including recent match results and player statistics. 

## Features

- **Recent Match Results:** View the latest match scores for Liverpool FC.
- **Player Stats:** Ask about individual player statistics such as goals, assists, player minutes, and more.
- **Interactive Chat:** Engage in a conversation with the assistant to get tailored information about Liverpool FC.

## Technologies Used

- Python
- Streamlit
- Langchain
- OpenAI API
- Beautiful Soup for web scraping (used in `scraper_functions.py`)

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/chatlfc.git
   cd chatlfc

2. **Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install the required packages:**
    ```bash
    pip install -r requirements.txt

4. **Add your OpenAI API key to the `secrets.toml` file:**
   ```bash
    OPENAI_API_KEY = "your_openai_api_key"

5. **Run the Streamlit app:**
   ```bash
   streamlit run app.py

## Usage
Once the app is running, open your browser and go to http://localhost:8501 to interact with ChatLFC. Type in your questions about Liverpool FC, and the assistant will respond with the relevant information.

## Contribution
Contributions are welcome! If you'd like to contribute, please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License.

## Acknowledgments

- [**Streamlit**](https://streamlit.io/) for the web app framework.
- [**Langchain**](https://langchain.readthedocs.io/en/latest/) for facilitating language model interactions.
- [**OpenAI**](https://openai.com/api/) for providing the language model API.
- [**FBref.com**](https://fbref.com/) for match and player data.




