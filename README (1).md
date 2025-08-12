# PeakCommerce Email Automation Chatbot

This project is a **Retrieval-Augmented Generation (RAG)** powered email automation tool built for PeakCommerce customer support.  
It uses a combination of **Sentence Transformers**, **Nearest Neighbors search**, and **Hugging Face LLaMA models** to provide intelligent email responses for customer inquiries.

The front-end is powered by **Streamlit**, allowing customers to fill out a simple form.  
The back-end processes their queries, retrieves relevant knowledge from previously scraped data, and generates a professional email response.

---

## Features
- 📨 Automated email drafting for customer inquiries.
- 🧠 RAG pipeline using `sentence-transformers` and `sklearn.neighbors`.
- 🤖 Integrates with Hugging Face API (Meta LLaMA 3-8B-Instruct).
- 📜 Maintains a short-term memory of past conversations.
- 🎨 Streamlit-based UI with a branded look and feel.
- 📂 JSON-based storage for scraped data and conversation history.

---

## Project Structure
```
.
├── main.py                 # Streamlit front-end
├── rag.py                  # RAG pipeline & email generation logic
├── PeakCommerce_Logo.jpg   # Branding asset for UI
├── emails_generated.json   # Scraped and cleaned knowledge base
├── memory.json             # Stored chat history
├── app.log                 # Optional logging file
├── README.md
└── requirements.txt
```

---

## Installation & Setup

### 1) Clone the repository
```bash
git clone https://github.com/kennedkqiraj/email_automation.git
cd email_automation
```

### 2) Create and activate a virtual environment
**Windows (PowerShell)**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies
```bash
pip install -r requirements.txt
```

### 4) Set your Hugging Face API token
Edit `rag.py` and replace:
```python
os.environ["HUGGINGFACE_TOKEN"] = "Add your token"
```
with your actual Hugging Face token, or set it as an environment variable:
```bash
export HUGGINGFACE_TOKEN=your_token_here
```

---

## Running the Application

### Run the Streamlit app:
```bash
streamlit run main.py
```

Open your browser and go to **http://localhost:8501**.

---

## How it Works
1. **User Input:** The customer fills in their first name, last name, email, and message in the Streamlit form.
2. **RAG Pipeline:**  
   - The query is parsed for contact details.  
   - Relevant knowledge is retrieved from `emails_generated.json` using semantic search (`NearestNeighbors`).  
   - A custom prompt is crafted and sent to the Hugging Face LLaMA API.
3. **Email Draft:** The model returns a professional, context-aware draft email.
4. **Memory Update:** The query and response are stored in `memory.json` for context in future interactions.

---

## Requirements
See `requirements.txt` for all dependencies.

---

## License
MIT — feel free to use, modify, and distribute.

---

## Acknowledgments
- [Sentence Transformers](https://www.sbert.net/)
- [scikit-learn](https://scikit-learn.org/)
- [Streamlit](https://streamlit.io/)
- [Hugging Face](https://huggingface.co/)
