# 🎬 Movie Data Extractor

A structured movie information extraction application built with **Python, LangChain, Mistral AI, Pydantic, and Streamlit**.

The application takes unstructured movie-related text and extracts important information into a consistent, structured format using an LLM and Pydantic validation.

## ✨ Features

* 🤖 AI-powered movie information extraction
* 🧩 Structured output using **Pydantic**
* 🔗 LangChain prompt management
* 🧠 Mistral AI integration
* 🎨 Interactive Streamlit web interface
* 📋 Extracts movie title, release year, genre, director, cast, rating, and summary
* 🚫 Prompt-based hallucination control for unknown information
* 📦 JSON output for structured movie data
* 🔐 Environment-based API key configuration

## 🛠️ Tech Stack

| Technology    | Purpose                               |
| ------------- | ------------------------------------- |
| Python        | Core programming language             |
| LangChain     | LLM integration and prompt management |
| Mistral AI    | Large Language Model                  |
| Pydantic      | Structured output validation          |
| Streamlit     | Web UI                                |
| python-dotenv | Environment variable management       |

## 🏗️ Project Structure

```text
Movie-data-extractor/
│
├── json reply/
│   ├── Core.py
│   └── Ui.py
│
├── .gitignore
├── .env
├── pyproject.toml
├── uv.lock
├── LICENSE
└── README.md
```

> `.env`, virtual environments, and other sensitive/local files should not be committed to GitHub.

## ⚙️ How It Works

The application follows this pipeline:

```text
User Input
    ↓
Streamlit UI
    ↓
LangChain ChatPromptTemplate
    ↓
Mistral AI
    ↓
PydanticOutputParser
    ↓
Structured Movie Object
    ↓
JSON / UI Output
```

### Example Input

```text
Inception is a 2010 science-fiction action film directed by
Christopher Nolan. It stars Leonardo DiCaprio, Joseph Gordon-Levitt,
Ellen Page, Tom Hardy and Ken Watanabe. The movie follows a skilled
thief who enters people's dreams to steal secrets.
```

### Example Output

```json
{
  "title": "Inception",
  "release_year": 2010,
  "genre": [
    "Science Fiction",
    "Action"
  ],
  "director": "Christopher Nolan",
  "cast": [
    "Leonardo DiCaprio",
    "Joseph Gordon-Levitt",
    "Ellen Page",
    "Tom Hardy",
    "Ken Watanabe"
  ],
  "rating": null,
  "summary": "A skilled thief who enters people's dreams to steal secrets."
}
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Rohit-code07/Movie-data-extractor.git
cd Movie-data-extractor
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

If using pip:

```bash
pip install -r requirements.txt
```

Or if you are using `uv`:

```bash
uv sync
```

### 4. Configure the API key

Create a `.env` file in the project root:

```env
MISTRAL_API_KEY=your_mistral_api_key
```

**Never commit your `.env` file or expose your API key publicly.**

### 5. Run the Streamlit application

```bash
streamlit run "json reply/Ui.py"
```

The application will be available at:

```text
http://localhost:8501
```

## 🧠 Structured Output

The project uses a Pydantic model to define the expected movie schema:

```python
class Movie(BaseModel):
    title: str
    release_year: Optional[int] = None
    genre: List[str]
    director: Optional[str] = None
    cast: List[str]
    rating: Optional[float] = None
    summary: str
```

This gives the LLM a defined structure instead of returning arbitrary text.

## 🔍 Handling Missing Information

The prompt instructs the model:

* Do not invent facts.
* Use `null` for unknown optional fields.
* Return only the structured movie output.

For example, if the input doesn't contain the director:

```json
{
  "director": null
}
```

This helps make the output predictable and easier to consume programmatically.

## 📸 Application

The Streamlit interface allows users to:

1. Enter unstructured movie information.
2. Send the information to the LLM.
3. Extract structured movie details.
4. View the extracted information in a readable interface.
5. Inspect the resulting JSON.

## 📄 License

This project is licensed under the **MIT License**.

See the [`LICENSE`](LICENSE) file for details.

## 👨‍💻 Author

**Rohit Verma**

GitHub: [Rohit-code07](https://github.com/Rohit-code07)
