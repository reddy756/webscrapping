from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

# Set up the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
ratings = []
reviews = []
for i in range(1,3):

# URL of the product page
    product_url = (f'https://www.amazon.in/Apple-MacBook-Chip-13-inch-256GB/product-reviews/B08N5W4NNB/'
                   f'ref=cm_cr_arp_d_paging_btm_next_{i}?ie=UTF8&reviewerType=all_reviews&pageNumber=2')
    driver.get(product_url)

# Allow time for the page to load
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # Find all review containers
    data = soup.find_all('div', class_="a-section review aok-relative")

    # Extract ratings and reviews
    for url in data:
        rating = url.find('span', class_='a-icon-alt')
        if rating:
            ratings.append(rating.text.strip())

        review_heading = url.find('span', {'data-hook': 'review-body'})
        if review_heading:
            reviews.append(review_heading.text.strip())



    # Create a DataFrame from the ratings and review bodies
df = pd.DataFrame({
    'Rating': ratings,
    'Review Body': reviews
})

    # Display the DataFrame
print(df)

    # Save to CSV
df.to_csv('amazon_reviews.csv', index=False, encoding='utf-8-sig')

# Close the driver
driver.quit()








#-------------------------------------------------- using TextBlob -----------------------------------------------

import pandas as pd
import nltk
import pandas as pd
from textblob import TextBlob

# Load the CSV file
df = pd.read_csv('amazon_reviews.csv')

# Select the column you want to analyze (replace 'column_name' with your actual column name)
text_column = df['Review Body']

# Define a function to calculate sentiment
def get_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity  # Returns a value between -1 and 1

# Apply sentiment analysis
df['sentiment'] = text_column.apply(get_sentiment)

# Save the results to a new CSV file
df.to_csv('sentiment_results.csv', index=False)

#-------------------------------------------------- Graph representation -----------------------------

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV file
data = pd.read_csv("sentiment_results.csv")

# Plot 1: Histogram of Scores
plt.figure(figsize=(10, 6))
sns.histplot(data['sentiment'], bins=20, kde=True, color='skyblue')
plt.title('Sentiment Score Distribution')
plt.xlabel('Sentiment Score')
plt.ylabel('Frequency')
plt.show()

# Plot 2: Box Plot of Scores
plt.figure(figsize=(10, 6))
sns.boxplot(x=data['sentiment'], color='lightcoral')
plt.title('Sentiment Score Spread')
plt.xlabel('Sentiment Score')
plt.show()

# Plot 3: Line Plot with Review Text Annotation
plt.figure(figsize=(12, 8))
sns.lineplot(data=data['sentiment'], marker='o', color='purple')
plt.title('Sentiment Score Over Reviews')
plt.xlabel('Review Order')
plt.ylabel('Sentiment Score')

# Annotate each point with the corresponding review text
for i in range(len(data)):
    plt.text(i, data['sentiment'][i], str(data['Review Body'][i]),
             horizontalalignment='left', size='small', color='black', weight='semibold')

plt.show()






