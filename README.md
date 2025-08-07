
# 🧠 Reddit Radicalization Detector

This project scrapes Reddit posts, analyzes them using a local language model (Zephyr 7B), and detects antisemitic or radical content. Data can be stored locally (JSON) or remotely via Supabase.

---

## 📦 Requirements

To run this project, you need:

- Python 3.10+
- `pip` (Python package manager)
- A system that can run [llama-cpp-python](https://github.com/abetlen/llama-cpp-python):
  - macOS (with Metal) or
  - Linux/Windows with CPU support (no GPU required)
- Reddit API credentials (CLIENT_ID, CLIENT_SECRET)
- (Optional) Supabase project

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourname/reddit-radicalization-detector.git
cd reddit-radicalization-detector
```

---

### 2. Create a virtual environment and install dependencies

```bash
python3 -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

### 3. Download the LLM model (Zephyr 7B)

```bash
mkdir -p models
wget -O models/zephyr-7b-alpha.Q4_K_M.gguf \
  https://huggingface.co/TheBloke/zephyr-7B-alpha-GGUF/resolve/main/zephyr-7b-alpha.Q4_K_M.gguf
```

Make sure `core/llm_scoring.py` uses this path:

```python
MODEL_PATH = "models/zephyr-7b-alpha.Q4_K_M.gguf"
```

---

### 4. Create a `.env` file

```ini
CLIENT_ID=your_reddit_client_id
CLIENT_SECRET=your_reddit_client_secret
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
```

You can create Reddit credentials at https://www.reddit.com/prefs/apps

---

## 🧪 How to run

All scripts are managed via the `Makefile`.

### 🔧 Common commands

| Command                          | What it does |
|----------------------------------|---------------|
| `make search_from_scratch`       | Scrapes posts by keywords, users or subreddits |
| `make score_all_posts`           | Scores all unscored posts |
| `make score_user`                | Scores all posts from a specific user |
| `make score_all_users`           | Calculates user-level radical scores |
| `make search_radicalized_users` | Finds top radicalized users and their posts |

Each script uses configuration defined in `input.json`.

---

## 📝 Example input.json

```json
{
  "search_from_scratch": {
    "keywords": ["jews", "zionism"],
    "subreddits": ["politics"],
    "usernames": [],
    "limit": 100,
    "output": "json"
  }
}
```

---

## 📂 Project structure

```
.
├── core/
│   ├── db.py                 # Database (Supabase) helpers
│   ├── json_storage.py       # JSON file I/O
│   ├── llm_scoring.py        # LLM loading and scoring logic
│   ├── user_scoring.py       # User-level scoring function
├── scripts/                  # Main entrypoint scripts
├── data/                     # posts.json and users.json (if using local mode)
├── models/                   # Zephyr GGUF model
├── input.json
├── .env
├── Makefile
└── requirements.txt
```
