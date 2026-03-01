#!/usr/bin/env python3
"""
Social Poster - Auto-generate social posts from content
"""
import sys
import urllib.request
import urllib.parse

# Sample blog posts (would integrate with Substack API)
POSTS = [
    {
        "title": "How I built a sports betting model with 68% accuracy",
        "url": "https://allowayai.substack.com/p/sports-betting-ml",
        "summary": "Built an XGBoost model for NBA predictions. Here's what worked."
    },
    {
        "title": "Why regex beat ML for job matching",
        "url": "https://allowayai.substack.com/p/regex-vs-ml",
        "summary": "Sometimes simple is better. Data showed regex outperformed transformers."
    },
    {
        "title": "Building AI agents that actually work",
        "url": "https://allowayai.substack.com/p/ai-agents",
        "summary": "Production-ready agent patterns from 6 months of building."
    }
]

def generate_tweet(post, style="thread"):
    """Generate tweet(s) from blog post"""
    title = post["title"]
    url = post["url"]
    summary = post["summary"]
    
    if style == "single":
        return f"{title}\n\n{summary}\n\n{url}"
    
    elif style == "thread":
        tweets = [
            f"🧵 I just published: {title}",
            f"Key insight: {summary}",
            f"Why it matters: Building AI tools is easy. Making them work in production is hard.",
            f"Link in comments 👇\n{url}"
        ]
        return "\n\n".join(tweets)
    
    return f"{title}: {url}"


def main():
    print(" Social Poster - Generate tweets from blog posts\n")
    
    for i, post in enumerate(POSTS, 1):
        print(f"{i}. {post['title']}")
    
    print("\n--- Single Tweet ---")
    print(generate_tweet(POSTS[0], "single"))
    
    print("\n--- Thread ---")
    print(generate_tweet(POSTS[0], "thread"))


if __name__ == "__main__":
    main()
