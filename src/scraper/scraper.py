
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import time

def extract_article(url, url_id):
    
    # Extract article title and text from a given URL
    
    try:
        # Set headers to mimic a browser (helps avoid being blocked)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        
        # Send GET request to the URL
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise error if request failed
        
        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract article title
        # Try multiple common title selectors
        title = ''
        title_tag = soup.find('h1', class_='entry-title') or \
                    soup.find('h1', class_='tdb-title-text') or \
                    soup.find('h1') or \
                    soup.find('title')
        
        if title_tag:
            title = title_tag.get_text().strip()
        
        # Extract article content
        # Try multiple common content selectors for this specific website
        article_content = ''
        
        # Strategy 1: Look for article tag or specific content classes
        content_tag = soup.find('div', class_='td-post-content') or \
                      soup.find('div', class_='tdb-block-inner') or \
                      soup.find('article') or \
                      soup.find('div', class_='entry-content')
        
        if content_tag:
            # Remove script and style elements
            for script in content_tag(['script', 'style', 'nav', 'footer', 'header']):
                script.decompose()
            
            # Get text from paragraphs
            paragraphs = content_tag.find_all('p')
            article_content = '\n\n'.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
        
        # If we couldn't get content, try getting all paragraphs
        if not article_content:
            paragraphs = soup.find_all('p')
            article_content = '\n\n'.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
        
        # Combine title and content
        full_text = f"{title}\n\n{article_content}"
        
        # Save to text file
        filename = f'{url_id}.txt'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(full_text)
        
        print(f"Successfully extracted: {url_id}")
        return True
        
    except Exception as e:
        print(f"Error extracting {url_id}: {str(e)}")
        return False


def main():
    """Main function to scrape all articles"""
    
    # Read input Excel file
    print("Reading Input.xlsx...")
    input_file = r'C:\Users\sam\Desktop\Blackcoffer_nlp_analysis\data\input\Input.xlsx'  # Update path if needed
    df = pd.read_excel(input_file)
    
    print(f"Found {len(df)} URLs to scrape\n")
    
    # Create directory for extracted articles
    os.makedirs('extracted_articles', exist_ok=True)
    os.chdir('extracted_articles')
    
    # Track success/failure
    success_count = 0
    failure_count = 0
    
    # Extract each article
    for index, row in df.iterrows():
        url_id = row['URL_ID']
        url = row['URL']
        
        print(f"[{index + 1}/{len(df)}] Extracting {url_id}...")
        
        if extract_article(url, url_id):
            success_count += 1
        else:
            failure_count += 1
        
        # Add small delay to avoid overwhelming the server
        time.sleep(1)
    
    # Print summary
    print("\n" + "="*50)
    print("EXTRACTION COMPLETE")
    print("="*50)
    print(f"Total URLs: {len(df)}")
    print(f"Successful: {success_count}")
    print(f"Failed: {failure_count}")
    print("="*50)


if __name__ == "__main__":
    main()