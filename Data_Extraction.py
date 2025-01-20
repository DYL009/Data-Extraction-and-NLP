#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import time

# Load the list of URLs from Input.xlsx
input_file = 'Input.xlsx'
data = pd.read_excel(input_file)

# Create a directory to save the extracted articles
os.makedirs("extracted_articles", exist_ok=True)

def extract_article_text(url):
    """Fetch and return article title and text content from a URL."""
    try:
        # Send a request to fetch the page content
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract title and paragraphs (customize based on HTML structure)
        title = soup.find('title').get_text() if soup.find('title') else "No Title"
        paragraphs = soup.find_all('p')
        article_text = '\n'.join([para.get_text() for para in paragraphs])

        return title, article_text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None, None

# Data structure to collect output records
output_data = []

# Loop through URLs and extract content
for index, row in data.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    
    # Extract content from the URL
    title, article_text = extract_article_text(url)
    
    if article_text:
        # Save the article as a text file
        filename = f"extracted_articles/{url_id}.txt"
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(f"Title: {title}\n\n{article_text}")
        
        # Append data to output list
        output_data.append({
            'URL_ID': url_id,
            'URL': url,
            'Title': title,
            'Content': article_text
        })
        print(f"Saved article for URL_ID {url_id}")
    else:
        print(f"Failed to extract article for URL_ID {url_id}")
    
    # Save progress every 10 URLs
    if (index + 1) % 10 == 0:
        pd.DataFrame(output_data).to_csv('interim_output.csv', index=False)
        print(f"Interim save completed after {index + 1} URLs.")

    # Throttle requests to avoid server overload
    time.sleep(1)  # Adjust as needed to avoid blocking

# Final save after processing all URLs
output_df = pd.DataFrame(output_data)
output_df.to_csv('final_output.csv', index=False)
print("All data saved to final_output.csv.")


# In[ ]:





# In[ ]:




