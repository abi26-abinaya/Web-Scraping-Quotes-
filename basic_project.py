import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Scrape Data
all_quotes = []
all_authors = []

url = "http://quotes.toscrape.com/page/1/"
while url:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    quotes = soup.find_all("span", class_="text")
    authors = soup.find_all("small", class_="author")

    for i in range(len(quotes)):
        all_quotes.append(quotes[i].text)
        all_authors.append(authors[i].text)

    next_btn = soup.find("li", class_="next")
    url = "http://quotes.toscrape.com" + next_btn.a["href"] if next_btn else None

# Step 2: Save to CSV
df = pd.DataFrame({"Quote": all_quotes, "Author": all_authors})
df.to_csv("quotes.csv", index=False, encoding="utf-8")
print("Data saved to quotes.csv")

# Step 3: Analyze Data
author_counts = df["Author"].value_counts()
print("\n Most Quoted Authors:")
print(author_counts.head())

print(f"\n The most quoted author is: {author_counts.idxmax()} ({author_counts.max()} quotes)")

# Step 4: Visualization
top_authors = author_counts.head(5)

plt.figure(figsize=(8,5))
top_authors.plot(kind="bar", color="skyblue", edgecolor="black")
plt.title("Top 5 Most Quoted Authors", fontsize=14)
plt.xlabel("Authors", fontsize=12)
plt.ylabel("Number of Quotes", fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
