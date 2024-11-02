import requests
from bs4 import BeautifulSoup
import pandas as pd

# Step 1: Send a request to the news website
url = "https://www.bbc.com/news"
response = requests.get(url)


soup = BeautifulSoup(response.content, "html.parser")

# Step 3: Find all sections with a partial match on class
sections = soup.find_all('section', class_=lambda x: x and "sc-3f5e3434-1" in x)

headlines_data = []  # To store only headlines and links

# Loop through each section to get headlines and links
for section in sections:
    # Collect all headlines and links within the section
    for item in section.find_all("h2"):
        headline_text = item.get_text(strip=True)

        # Find the <a> tag that might contain the link
        link_tag = item.find_parent("a")
        if link_tag and "href" in link_tag.attrs:
            link = link_tag["href"]
            # If the link is relative, add the base URL
            base_url = "https://www.bbc.com"
            full_link = link if link.startswith("http") else base_url + link
        else:
            full_link = "No link available"

        # Append only headlines and links to the list
        headlines_data.append({
            "Headline": headline_text,
            "Link": full_link
        })

# Step 4: Save results to a CSV file
if headlines_data:  # Check if there is any data to save
    df = pd.DataFrame(headlines_data)
    df.to_csv("news_headlines.csv", index=False)
    print("Data has been saved to news_headlines.csv")
else:
    print("No headlines found. Please check the selector.")
# else:
#     print(f"Failed to retrieve the page. Status code: {response.status_code}")
