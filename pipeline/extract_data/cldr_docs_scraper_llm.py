import asyncio
import aiohttp
from xml.etree import ElementTree
from bs4 import BeautifulSoup
import re
import os
import json
from urllib.parse import urlparse, unquote

def sanitize_filename(title):
    sanitized = re.sub(r'[\\/*?:"<>|]', '', title)
    return sanitized[:200]  # Limit filename length

def sanitize_path(path):
    sanitized = re.sub(r'[\\/*?:"<>|]', '_', path)
    return sanitized

def extract_base_directory(url):
    parsed_url = urlparse(url)
    path_segments = parsed_url.path.strip('/').split('/')
    base_dir = path_segments[0] if len(path_segments) > 0 else 'default'
    return sanitize_path(base_dir)

def create_directory_structure(url):
    base_directory = extract_base_directory(url)
    os.makedirs(base_directory, exist_ok=True)
    return base_directory

async def fetch(url, session):
    try:
        async with session.get(url) as response:
            if response.status in [404, 503]:
                print(f"Skipping URL {url} due to HTTP status: {response.status}")
                return None
            return await response.text()
    except Exception as e:
        print(f"Error fetching URL {url}: {e}")
        return None

async def get_sitemap_urls(sitemap_url, session):
    xml = await fetch(sitemap_url, session)
    if xml:
        root = ElementTree.fromstring(xml)
        urls = [url.text for url in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
        return urls
    return []

def extract_content_for_llm(soup):
    content = {
        "headings": [],
        "paragraphs": [],
        "code": [],
        "lists": [],
        "tables": []
    }

    for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        content["headings"].append(heading.get_text(strip=True))

    for paragraph in soup.find_all('p'):
        content["paragraphs"].append(paragraph.get_text(strip=True))

    for code in soup.find_all('code'):
        content["code"].append(code.get_text(strip=True))

    for list_tag in soup.find_all(['ul', 'ol']):
        list_items = [li.get_text(strip=True) for li in list_tag.find_all('li')]
        content["lists"].append(list_items)

    for table in soup.find_all('table'):
        rows = []
        for row in table.find_all('tr'):
            cells = [cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])]
            rows.append(cells)
        content["tables"].append(rows)

    return content

async def scrape_and_save(url, session):
    html = await fetch(url, session)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('title').get_text(strip=True) if soup.find('title') else 'No Title'
        llm_content = extract_content_for_llm(soup)
        base_directory = create_directory_structure(url)
        filepath = os.path.join(base_directory, f'{sanitize_filename(title)}.json')
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump({
                "url": url,
                "title": title,
                "content": llm_content
            }, file, indent=4, ensure_ascii=False)

async def process_sitemap(url, session):
    if url.endswith('sitemap.xml'):
        nested_urls = await get_sitemap_urls(url, session)
        tasks = [scrape_and_save(nested_url, session) for nested_url in nested_urls]
        await asyncio.gather(*tasks)
    else:
        await scrape_and_save(url, session)

async def main():
    main_sitemap_url = 'https://docs.cloudera.com/sitemap.xml'
    async with aiohttp.ClientSession() as session:
        main_sitemap_urls = await get_sitemap_urls(main_sitemap_url, session)
        tasks = [process_sitemap(url, session) for url in main_sitemap_urls]
        await asyncio.gather(*tasks)
    print('Scraping complete. Data saved in JSON format for LLM training.')

if __name__ == '__main__':
    asyncio.run(main())
