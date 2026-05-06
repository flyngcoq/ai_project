import re
import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi

def extract_urls(text):
    """Extracts all URLs from a given text."""
    url_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    return re.findall(url_pattern, text)

def scrape_general_url(url):
    """Scrapes the title, meta description, and main text content of a general URL."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,ko;q=0.8",
    }
    try:
        response = requests.get(url, timeout=15, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.title.string if soup.title else "No Title"
        
        # Try to find meta description
        description = ""
        meta_desc = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
        if meta_desc:
            description = meta_desc.get("content", "")

        # Extract main text (paragraphs)
        paragraphs = soup.find_all('p')
        body_text = "\n".join([p.get_text() for p in paragraphs[:15]])
        
        final_content = f"Title: {title}\nDescription: {description}\nBody:\n{body_text}"
        
        return {
            "type": "website",
            "title": title.strip(),
            "content": final_content.strip(),
            "url": url
        }
    except Exception as e:
        return {"error": str(e), "url": url}

def get_youtube_id(url):
    """Extracts YouTube ID from various URL formats."""
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'youtu\.be\/([0-9A-Za-z_-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def scrape_youtube_url(url):
    """Scrapes YouTube metadata and transcript if available."""
    video_id = get_youtube_id(url)
    if not video_id:
        return scrape_general_url(url)
    
    # Get metadata from page even if transcript fails
    meta_info = scrape_general_url(url)
    
    result = {
        "type": "youtube",
        "video_id": video_id,
        "url": url,
        "title": meta_info.get("title", f"YouTube Video ({video_id})"),
        "content": meta_info.get("content", ""),
        "transcript": ""
    }
    
    # Try to get transcript
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko', 'en'])
        transcript_text = " ".join([item['text'] for item in transcript_list])
        result["transcript"] = transcript_text
    except Exception as e:
        result["transcript"] = "자막을 직접 가져올 수 없습니다. 메타데이터 정보를 활용하세요."
        
    return result

def enrich_content_with_urls(text):
    """Finds URLs in text and appends scraped info."""
    urls = list(set(extract_urls(text))) # Unique URLs only
    if not urls:
        return text
    
    enriched_info = "\n\n--- 🌐 Scraped Web Info ---\n"
    for url in urls:
        print(f"Scraping URL: {url}...")
        if "youtube.com" in url or "youtu.be" in url:
            info = scrape_youtube_url(url)
            enriched_info += f"### 🎥 YouTube: {info.get('title')}\n"
            enriched_info += f"**URL**: {url}\n"
            enriched_info += f"**Metadata**: {info.get('content')[:500]}...\n"
            enriched_info += f"**Transcript Snippet**: {info.get('transcript')[:500]}...\n\n"
        else:
            info = scrape_general_url(url)
            if "error" in info:
                enriched_info += f"### ❌ Error scraping {url}: {info['error']}\n\n"
            else:
                enriched_info += f"### 📄 Page: {info.get('title')}\n"
                enriched_info += f"**URL**: {url}\n"
                enriched_info += f"**Content**: {info.get('content')[:1000]}...\n\n"
                
    return text + enriched_info
