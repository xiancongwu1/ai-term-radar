import feedparser
import re
from datetime import datetime, timedelta
from collections import Counter

# Config
RSS_FEEDS = [
    "https://hnrss.org/newest?q=AI+OR+LLM+OR+model",
    "https://www.reddit.com/r/artificial/.rss"
]
KEYWORDS = ["model", "agent", "framework", "dataset", "tool"]
LOOKBACK_HOURS = 24

# Fetch and parse feeds
entries = []
for url in RSS_FEEDS:
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            published = entry.get('published_parsed')
            if published:
                pub_time = datetime(*published[:6])
                if datetime.now() - pub_time < timedelta(hours=LOOKBACK_HOURS):
                    entries.append(entry.title + " " + entry.get('summary', ''))
    except Exception as e:
        print(f"Error fetching {url}: {e}")

# Extract potential new terms (camelCase, hyphenated, or keyword+number)
content = " ".join(entries)
patterns = [
    r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b',  # CamelCase
    r'\b[a-z]+-[a-z]+\b',                # hyphenated
    r'\b(?:' + '|'.join(KEYWORDS) + r')\s?\d+\b'  # keyword+number
]
terms = []
for pattern in patterns:
    terms.extend(re.findall(pattern, content))

# Filter out common words and duplicates
common = {"the", "and", "for", "with", "from", "this"}
term_counts = Counter([t.lower() for t in terms if t.lower() not in common])

# Output top 10 new terms
today = datetime.now().strftime("%Y-%m-%d")
print(f"# AI Term Radar {today}")
for term, count in term_counts.most_common(10):
    print(f"- {term} ({count} mentions)")
}
---
No need for a README or extra files; this snippet is self-contained and runnable with `pip install feedparser`. Replace RSS feeds or keywords to match your niche.