# Project runner for AF

PYTHON=python3
PYTHONPATH=.

# === Search ===
search_from_scratch:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) scripts/search_from_scratch.py

search_radicalized_users:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) scripts/search_radical_users.py

# === Scoring ===
batch_scoring:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) scripts/batch_scoring.py

score_all_posts:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) scripts/score_all_posts.py

score_user:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) scripts/score_user.py

score_all_users:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) scripts/score_all_users.py

# === Subreddit Scraping ===
scrape_subreddit:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) scripts/subreddit_scraper.py

# === Test LLM ===
test_llm:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) testing/test_llm.py

# === Cleanup (optional) ===
clean_cache:
	rm -rf __pycache__ core/__pycache__ scripts/__pycache__ testing/__pycache__

# === Help ===
help:
	@echo "Available make commands:"
	@echo "  make search_from_scratch   - Run Reddit search based on input.json"
	@echo "  make batch_scoring         - Run scoring for posts"
	@echo "  make scrape_subreddit      - Run raw subreddit scraper"
	@echo "  make test_llm              - Run test LLM load & inference"
	@echo "  make clean_cache           - Remove __pycache__ folders"
