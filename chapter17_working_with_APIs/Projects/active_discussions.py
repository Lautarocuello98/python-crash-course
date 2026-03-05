import requests
import plotly.express as px
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def make_session() -> requests.Session:
    """Create a requests session with retries for flaky connections."""
    session = requests.Session()

    retry = Retry(
        total=5,
        connect=5,
        read=5,
        backoff_factor=0.5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET",),
        raise_on_status=False,
    )

    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


session = make_session()

# 1) Get top stories IDs
topstories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
r = session.get(topstories_url, timeout=10)
r.raise_for_status()
submission_ids = r.json()

submission_dicts = []

# 2) Fetch details (grab more than needed, because we'll skip failures/ads/etc.)
for submission_id in submission_ids[:60]:
    item_url = f"https://hacker-news.firebaseio.com/v0/item/{submission_id}.json"

    try:
        r = session.get(item_url, timeout=10)
        r.raise_for_status()
        item = r.json()

        if not item or item.get("type") != "story":
            continue

        num_comments = item.get("descendants", 0)
        if num_comments == 0:
            continue

        title = item["title"]
        hn_link = f"https://news.ycombinator.com/item?id={submission_id}"
        title_link = f"<a href='{hn_link}'>{title}</a>"

        submission_dicts.append(
            {
                "title_link": title_link,
                "comments": num_comments,
                "owner": item.get("by", "unknown"),
                "hn_link": hn_link,
            }
        )

    except (requests.exceptions.RequestException, KeyError, TypeError):
        # RequestException: SSL/network/timeouts/etc.
        # KeyError/TypeError: missing or malformed fields
        continue

# 3) Sort by comment count (most active first) and keep top 15
submission_dicts.sort(key=lambda d: d["comments"], reverse=True)
submission_dicts = submission_dicts[:15]

# 4) Prepare data for Plotly
titles = [d["title_link"] for d in submission_dicts]
comments = [d["comments"] for d in submission_dicts]
hover_texts = [f"{d['owner']}<br />{d['hn_link']}" for d in submission_dicts]

# 5) Plot
title = "Hacker News — Most Active Discussions (by comments)"
labels = {"x": "Submission", "y": "Comments"}

fig = px.bar(
    x=titles,
    y=comments,
    title=title,
    labels=labels,
    hover_name=hover_texts,
)

fig.update_layout(
    title_font_size=28,
    xaxis_title_font_size=20,
    yaxis_title_font_size=20,
)
fig.update_xaxes(tickangle=45)

fig.show()