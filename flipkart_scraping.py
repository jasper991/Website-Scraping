import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.flipkart.com/search?q=mobile+phone+under+20000&as=on&as-show=on&otracker=AS_Query_OrganicAutoSuggest_3_19_na_na_na&otracker1=AS_Query_OrganicAutoSuggest_3_19_na_na_na&as-pos=3&as-type=RECENT&suggestionId=mobile+phone+under+20000&requestId=52895815-1a4e-46da-8ae2-4f32bfcb941b&as-backfill=on"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    product_containers = soup.find_all('div', {'class': '_1AtVbE'})

    # Create a list to store the data
    data = []

    for product in product_containers:
        title_container = product.find('div', {'class': '_4rR01T'})
        price_container = product.find('div', {'class': '_30jeq3 _1_WHN1'})
        rating_container = product.find('div', {'class': '_3LWZlK'})
        specs_container = product.find('ul', {'class': '_1xgFaf'})
        
        link_container = product.find('a', {'class': '_1fQZEK'}, href=True)  # Updated line to find the link

        title = title_container.text.strip() if title_container else None
        price = price_container.text.strip() if price_container else None
        rating = rating_container.text.strip() if rating_container else None
        specs = ', '.join([spec.text.strip() for spec in specs_container.find_all('li')]) if specs_container else None
        link = f"https://www.flipkart.com{link_container['href']}" if link_container else None

        data.append({
            "Product": title,
            "Price": price,
            "Link": link,
            "Rating": rating,
            "Specs": specs
        })

    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data)

    # Write the DataFrame to an Excel file
    df.to_excel("flipkart_mobiles.xlsx", index=False)

    print("Data has been exported to flipkart_mobiles.xlsx")

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")