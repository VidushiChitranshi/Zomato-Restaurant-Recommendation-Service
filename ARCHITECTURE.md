# Zomato Restaurant Recommendation Service

## Project Overview
The Zomato Restaurant Recommendation Service is a modular Python application designed to provide personalized restaurant suggestions. It leverages the [ManikaSaini/zomato-restaurant-recommendation](https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation) dataset from Hugging Face and integrates the Groq LLM API to generate refined, conversational recommendation summaries.

The service follows a clean, phase-wise architecture to ensure maintainability, scalability, and robust testing.

## High-Level Architecture
The application is structured into five distinct phases, each encapsulated in its own module. A root orchestration script (`app.py`) manages the flow of data through these phases:

1.  **Data Acquisition & Preprocessing**: Loading and cleaning the dataset.
2.  **User Input Handling**: Capturing and validating location and price preferences.
3.  **Search Logic**: Filtering the dataset based on validated user criteria.
4.  **LLM Integration**: Enhancing results with AI-generated explanations via Google AI Studio (Gemini).
5.  **Result Display**: Formatting and presenting the final recommendations.

## Folder Structure
```text
Zomato_Service/
├── app.py                  # Root orchestration script
├── requirements.txt        # Project dependencies
├── .env                    # Environment variables (GROQ_API_KEY)
├── phase_1_data/           # Phase 1: Data Acquisition
│   ├── __init__.py
│   ├── dataset_loader.py   # Loader logic
│   └── tests/
│       └── test_loader.py  # Pytest for data loading/cleaning
├── phase_2_input/          # Phase 2: User Input handling
│   ├── __init__.py
│   ├── input_handler.py    # CLI input & validation logic
│   └── tests/
│       └── test_input.py   # Pytest for validation rules
├── phase_3_search/         # Phase 3: Filtering & Search
│   ├── __init__.py
│   ├── search_engine.py    # Core search logic
│   └── tests/
│       └── test_search.py  # Pytest for filtering scenarios
├── phase_4_llm/            # Phase 4: Google AI Gemini Integration
│   ├── __init__.py
│   ├── gemini_client.py    # LLM API wrapper
│   └── tests/
│       └── test_llm.py     # Pytest (with mocking) for LLM logic
└── phase_5_display/        # Phase 5: Output Presentation
    ├── __init__.py
    ├── formatter.py        # Display formatting logic
    └── tests/
        └── test_display.py  # Pytest for output consistency
```

## Phase Responsibilities

### Phase 1 – Data Acquisition (`phase_1_data`)
- **Responsibilities**: Load the dataset from Hugging Face, handle data types, perform null cleaning, and return a clean Pandas DataFrame.
- **Key Files**: `dataset_loader.py`.

### Phase 2 – User Input Handling (`phase_2_input`)
- **Responsibilities**: Capture location and budget (price) from the user via CLI, validate inputs against expected ranges or types.
- **Key Files**: `input_handler.py`.

### Phase 3 – Search & Filtering (`phase_3_search`)
- **Responsibilities**: Execute searches against the preprocessed DataFrame using criteria from Phase 2. Handle edge cases where no matches are found.
- **Key Files**: `search_engine.py`.

### Phase 4 – LLM Integration (`phase_4_llm`)
- **Responsibilities**: Construct prompts using filtered restaurant data and interact with the Google AI Gemini API. Isolate API logic from business logic.
- **Key Files**: `gemini_client.py`.

### Phase 5 – Result Display (`phase_5_display`)
- **Responsibilities**: Final presentation layer. Concatenate data from Phase 3 and narratives from Phase 4 into a clean user-facing format.
- **Key Files**: `formatter.py`.

## Testing Strategy
The project uses `pytest` for unit testing, following a strict "test-per-phase" policy:

| Phase | Testing Focus | Tool/Method |
| :--- | :--- | :--- |
| **Data** | Dataset loading, schema validation, null handling. | `pytest`, `pandas` assertions. |
| **Input**| Boundary testing for price, valid/invalid location checks. | `pytest` with `monkeypatch` for stdin. |
| **Search**| Filtering accuracy, empty result handling. | `pytest` with mock DataFrames. |
| **LLM** | Prompt structure, API response parsing. | `pytest` with `unittest.mock`. |
| **Display**| Formatting correctness, empty result messages. | `pytest`. |

## Execution Flow
1. `app.py` initializes the system.
2. `phase_1` loads the Zomato dataset.
3. `phase_2` prompts the user for "Location" and "Price range".
4. `phase_3` filters the dataset.
5. If results exist, `phase_4` sends top matches to Groq for a summary.
6. `phase_5` prints the final recommendation list and AI summary.

## Setup and Usage

### Environment Setup
1. Clone the repository.
2. Create a `.env` file in the root directory:
   ```env
   GOOGLE_API_KEY=your_api_key_here
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application
```bash
python app.py
```

### Running Tests
To run all tests:
```bash
pytest
```
To run tests for a specific phase:
```bash
pytest phase_1_data/tests/
```

## Scalability and Extension
- **Database Migration**: The search engine can be swapped for a Vector DB (e.g., Pinecone) if semantic search is required.
- **Web Interface**: The modular design allows replacing Phase 2 (CLI) and Phase 5 (Display) with a Flask or FastAPI frontend without touching core logic.
- **Multi-LLM Support**: Phase 4 can be extended to support multiple LLM providers via a common interface.
