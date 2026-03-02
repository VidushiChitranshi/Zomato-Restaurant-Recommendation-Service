# 🍴 Zomato AI Restaurant Recommendation Service

A professional, modular Python application that provides personalized restaurant suggestions using the [ManikaSaini/zomato-restaurant-recommendation](https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation) dataset and **Google Gemini AI**.

## 🚀 Experience the App
- **Live Demo**: [zomato-ai.streamlit.app](#) *(Deploy using the steps below)*
- **Core Tech**: Streamlit, FastAPI, Google Gemini API, Pandas, Hugging Face Datasets.

---

## 🏗️ Architecture & Structure
The project follows a clean, phase-based architecture housed within a professional `app/` directory.

### Folder Structure
```text
Zomato_Service/
├── streamlit_app.py        # 🚀 Main Entry Point (Streamlit UI)
├── app/                    # 📦 Core Logic Package
│   ├── main_cli.py         # 💻 CLI Entry Point
│   ├── phase_1_data/       # Data Acquisition (Hugging Face)
│   ├── phase_2_input/      # Input Handling & Validation
│   ├── phase_3_search/     # Search & Filtering Engine
│   ├── phase_4_llm/        # Google Gemini AI Integration
│   ├── phase_5_display/    # Formatters & UI Logic
│   └── phase_6_web/        # FastAPI Backend & Web UI
├── tests/                  # 🧪 Integration Tests
├── requirements.txt        # Python Dependencies
└── README.md               # Project Documentation
```

---

## 🛠️ Setup & Local Development

### 1. Prerequisites
- Python 3.9+
- A Google AI Studio API Key ([Get one here](https://aistudio.google.com/))

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/VidushiChitranshi/Zomato-Restaurant-Recommendation-Service.git
cd Zomato-Restaurant-Recommendation-Service

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the root directory:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 4. Running the Applications
- **Streamlit (Recommended)**:
  ```bash
  streamlit run streamlit_app.py
  ```
- **FastAPI Backend**:
  ```bash
  python app/phase_6_web/api.py
  ```
- **CLI Mode**:
  ```bash
  python app/main_cli.py
  ```

---

## 🧪 Testing
The project maintains high code quality with over 50 unit and integration tests.
```bash
# Run all tests
pytest
```

## 🔐 Deployment (Streamlit Cloud)
To deploy this service on Streamlit Community Cloud:
1. Connect your GitHub repository to [Streamlit Cloud](https://share.streamlit.io/).
2. Set the Main File Path to `streamlit_app.py`.
3. **Advanced Settings**: Add your `GOOGLE_API_KEY` to the **Secrets** section:
   ```toml
   GOOGLE_API_KEY = "your_key_here"
   ```

---
Built with ❤️ by Vidushi Chitranshi
