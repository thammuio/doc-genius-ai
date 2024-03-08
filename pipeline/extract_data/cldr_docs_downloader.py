import random
import asyncio
import aiohttp
from aiohttp import ClientSession
import backoff
from xml.etree import ElementTree
from bs4 import BeautifulSoup, NavigableString
import re
import os
from urllib.parse import urlparse, unquote

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15",
    # Add more user agents here
]

def sanitize_filename(title):
    sanitized = re.sub(r'[\\/*?:"<>|]', '', title)
    return sanitized[:200]

def sanitize_path(path):
    sanitized = re.sub(r'[\\/*?:"<>|]', '_', path)
    return sanitized

def create_directory_structure(url):
    parsed_url = urlparse(url)
    path_segments = parsed_url.path.strip('/').split('/')
    
    # Select the first three segments after 'docs.cloudera.com', if present
    if 'docs.cloudera.com' in path_segments:
        start_index = path_segments.index('docs.cloudera.com') + 1
    else:
        start_index = 0

    # Limit to the next three segments
    end_index = start_index + 3
    relevant_segments = path_segments[start_index:end_index]

    # Check if the last segment is a file (e.g., .html), and exclude it if so
    if relevant_segments and '.' in relevant_segments[-1]:
        relevant_segments.pop()

    # Only create directories if there are 1 to 3 valid segments
    if 0 < len(relevant_segments) <= 3:
        directory_path = os.path.join(*relevant_segments)
        os.makedirs(directory_path, exist_ok=True)
        return directory_path
    else:
        raise ValueError("Unable to determine appropriate directory structure from URL.")

def normalize_whitespace(text):
    return re.sub(r'\s+', ' ', text).strip()

@backoff.on_exception(backoff.expo, aiohttp.ClientResponseError, max_tries=5, giveup=lambda e: e.status not in [503, 429])
async def fetch(url, session):
    try:
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        async with session.get(url, headers=headers) as response:
            if response.status in [503, 429]:
                # Handle Too Many Requests or Service Unavailable
                await asyncio.sleep(60)  # Wait for 60 seconds before retrying
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message="Service Unavailable or Too Many Requests",
                    headers=response.headers
                )
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

def extract_relevant_content(soup):
    content = []

    for tag in soup.find_all(True):  # True will match every tag
        if (tag.name == 'div' and 'p' in tag.get('class', [])) or tag.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol', 'table', 'br', 'pre', 'section', 'dl', 'dt', 'dd']:
            formatted_text = format_text(tag)
            if formatted_text:
                content.append(formatted_text)

    # Join the content and remove excessive newlines
    joined_content = '\n'.join(content)

    return joined_content

def format_text(tag):
    if tag.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        return normalize_whitespace(tag.get_text()) + '\n'
    elif tag.name == 'p':
        return normalize_whitespace(tag.get_text()) + '\n'
    elif tag.name in ['ul', 'ol']:
        items = ['- ' + normalize_whitespace(li.get_text()) for li in tag.find_all('li', recursive=False)]
        return '\n'.join(items) + '\n'
    elif tag.name == 'br':
        return '\n'
    elif tag.name == 'pre':
        return '\n' + tag.get_text() + '\n'
    elif tag.name == 'table':
        return format_table(tag) + '\n'
    elif tag.name in ['dl', 'dt', 'dd']:
        if tag.name == 'dl':
            return '\n'.join([format_text(child) for child in tag.children if child.name in ['dt', 'dd']])
        else:
            return normalize_whitespace(tag.get_text()) + '\n'
    else:
        return normalize_whitespace(tag.get_text())

def format_table(table_tag):
    table_content = []

    # Process table headers
    headers = table_tag.find_all('th')
    if headers:
        header_titles = [normalize_whitespace(header.get_text()) for header in headers]
        table_content.append(' | '.join(header_titles))

    # Process table body rows
    body_rows = table_tag.find_all('tr')
    for row in body_rows:
        # Skip header row in body if it's already processed
        if row.find('th'):
            continue
        cells = row.find_all(['td', 'th'])  # Include both 'td' and 'th' for mixed rows
        cell_texts = [normalize_whitespace(cell.get_text()) for cell in cells]
        table_content.append(' | '.join(cell_texts))

    return '\n'.join(table_content)


async def scrape_and_save(url, session):
    html = await fetch(url, session)
    if html:
        # Using 'html5lib' parser without specifying from_encoding
        soup = BeautifulSoup(html, 'html5lib')
        title = soup.find('title').get_text(strip=True) if soup.find('title') else 'No Title'
        text_content = extract_relevant_content(soup)
        base_directory = create_directory_structure(url)
        filepath = os.path.join(base_directory, f'{sanitize_filename(title)}.txt')
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(text_content)

async def process_sitemap(url, session):
    if url.endswith('sitemap.xml'):
        nested_urls = await get_sitemap_urls(url, session)
        tasks = [scrape_and_save(nested_url, session) for nested_url in nested_urls]
        await asyncio.gather(*tasks)
    else:
        await scrape_and_save(url, session)

async def main():
    main_sitemap_url = 'https://docs.cloudera.com/sitemap.xml'
    async with ClientSession() as session:
        main_sitemap_urls = await get_sitemap_urls(main_sitemap_url, session)
        tasks = [process_sitemap(url, session) for url in main_sitemap_urls]
        await asyncio.gather(*tasks)
    print('Scraping complete. Data saved in TXT format.')

if __name__ == '__main__':
    asyncio.run(main())
