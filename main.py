import streamlit as st
from bs4 import BeautifulSoup
import pandas as pd
import requests
import base64  # For CSV download
import re

def clean_text(text):
    # Remove non-ASCII characters
    cleaned_text = re.sub(r'[^\x00-\x7F]+', '', text)
    return cleaned_text

selected_tag = st.selectbox('Choose your topic:', ['Humor','Love','Life','Books','Inspirational'])
tag = selected_tag.lower()

url = f"https://quotes.toscrape.com/tag/{tag}/"

res = requests.get(url)
content = BeautifulSoup(res.content, 'html.parser')

quotes = content.find_all('div', class_='quote')

quote_data = []

for quote in quotes:
    text = quote.find('span', class_='text').text
    author = quote.find('small', class_='author').text
    link = quote.find('a')['href']
    # Clean text
    text = clean_text(text)
    author = clean_text(author)
    full_link = "https://quotes.toscrape.com"+ link
    quote_data.append({
        'Quotes': text,
        'Authors': author,
        'Links': full_link
  })

if quote_data:  # Check if quotes exist before attempting download
  csv_content = pd.DataFrame(quote_data)  # Generate CSV content
  csv_string = csv_content.to_csv(index=False) # Get CSV string representation

  # Download button with decoded content
  download_button = st.download_button(
      label="Download Quotes (CSV)",
      data=csv_string,  # Provide actual CSV string
      file_name="quotes.csv",
      mime="text/csv"
  )

  # Add a horizontal line for separation
  st.markdown("---")

  st.markdown(f"<h2 style='text-align: center;'>{selected_tag} Quotes</h2>", unsafe_allow_html=True)
  st.markdown(f"")

  for quote in quote_data:
    st.markdown(f"<p style='font-size: 18px;'>{quote['Quotes']}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: right;'><a href=https://quotes.toscrape.com{quote['Links']} target='_blank'>- {quote['Authors']}</a></p>", unsafe_allow_html=True)
    st.markdown("---")
else:
  st.warning("No quotes found for this topic.")
