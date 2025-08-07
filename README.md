# Reddit Radicalization Detector

This project provides an automated system for detecting and analyzing antisemitic content on Reddit. It combines data collection, language analysis, and radicalization scoring into a modular pipeline that outputs structured information about users and their posts.

It can be run entirely offline using JSON, or with Supabase as a cloud database.

---

## 📦 Setup

### Requirements

- Python 3.10+
- pip
- Reddit API credentials
- (Optional) Supabase project credentials

### Installation

```bash
git clone https://github.com/angelosedler/reddit-radicalization-detector.git
cd reddit-radicalization-detector
python3 -m venv venv
source venv/bin/activate         # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Download the Zephyr Model

```bash
pip install huggingface-hub
huggingface-cli download TheBloke/zephyr-7B-alpha-GGUF zephyr-7b-alpha.Q4_K_M.gguf \  --local-dir models --local-dir-use-symlinks False
```

### Set up `.env`

```env
CLIENT_ID=your_reddit_client_id
CLIENT_SECRET=your_reddit_client_secret
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
```

---

## 🛠️ Running the Project

All scripts are in the `scripts/` folder and configured via `input.json`. You can run each with:

```bash
make <command>
# or manually:
PYTHONPATH=. python3 scripts/<script>.py
```

---

## ⚙️ Commands and Inputs

### 1. `search_from_scratch`

**Function:** Scrape Reddit by keywords, subreddits, or usernames.  
**Output:** Stores posts and users in `json` or `db`.

**Input:**
```json
"search_from_scratch": {
  "keywords": ["zionism"],
  "subreddits": ["conspiracy"],
  "usernames": ["example_user"],
  "limit": 50,
  "output": "json"
}
```

---

### 2. `search_radicalized_users`

**Function:** Find top radicalized users and retrieve their posts.  
**Input:**
```json
"search_radicalized_users": {
  "input": "json",
  "output": "db",
  "users_limit": 10,
  "limit": 50,
  "date_limit": "01/07/2024"
}
```

---

### 3. `score_all_posts`

**Function:** Score all unscored posts.  
**Input:**
```json
"score_all_posts": {
  "input": "json",
  "output": "json",
  "limit": 100
}
```

---

### 4. `score_user`

**Function:** Score all unscored posts from a single user and assign them a `radical_score`.  
**Input:**
```json
"score_user": {
  "username": "example_user",
  "input": "json",
  "output": "json",
  "limit": 50
}
```

---

### 5. `score_all_users`

**Function:** Score all users by aggregating their scored posts.  
**Input:**
```json
"score_all_users": {
  "input": "json",
  "output": "json"
}
```

---

## 🗃 Output Format

Depending on configuration, the system saves data to:
- `data/posts.json`
- `data/users.json`
- Or updates tables in Supabase

Each post has a `radical_score`, `language`, `explanation`, and metadata.
Each user has a computed `radical_score` and description.

---

## 📈 Output Files

- `posts.csv`: Top 300 posts from db, sorted by `radical_score`
- `users.csv`: Top 300 users from db, sorted by `radical_score`

---

## 📄 Further Documentation

- See `Project Presentation` for a general overview
- See `Technical & Business Specification` for internals, architecture and design decisions
