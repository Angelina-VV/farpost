import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json

async def fetch_content(url: str) -> str:
    """Asynchronously fetches the content of a URL."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            return await response.text()

async def get_ruble_exchange_rate() -> float:
    """Fetches the current ruble exchange rate from the Central Bank of Russia."""
    url = 'http://www.cbr.ru/development/sxml/'
    xml_content = await fetch_content(url)
    soup = BeautifulSoup(xml_content, 'xml')
    rate = soup.find('Valute', {'ID': 'R01235'})
    if rate:
        value = rate.Value.text
        return float(value.replace(',', '.'))
    else:
        raise ValueError("Failed to retrieve ruble exchange rate.")

async def scrape_sp500_data() -> list:
    """Scrapes S&P 500 data from the given URL."""
    url = "https://markets.businessinsider.com/index/components/s&p_500"
    html_content = await fetch_content(url)
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', class_='table')

    if not table:
        raise ValueError("Table not found on the page.")

    companies_data = []
    for row in table.find_all('tr')[1:]:  # Skip header row
        cells = row.find_all('td')
        if cells:
            name = cells[0].text.strip()
            last_price = float(cells[1].text.strip())
            annual_growth = cells[7].text.strip()
            annual_growth = float(annual_growth.split(" ")[0]) if annual_growth != '-' else 0

            companies_data.append({
                'name': name,
                'last_price': last_price,
                'annual_growth': annual_growth,
                'code': 'N/A',  # Placeholder
                'P/E': 'N/A',  # Placeholder
                'potential_profit': 0  # Placeholder
            })
    return companies_data

async def main():
    """Main function to orchestrate data scraping and saving."""
    try:
        ruble_rate = await get_ruble_exchange_rate()
        companies_data = await scrape_sp500_data()

        # Calculate price in rubles (only available metric for now)
        for company in companies_data:
            company['last_price_rub'] = company['last_price'] * ruble_rate

        # Sort and select top 10
        top_expensive = sorted(companies_data, key=lambda x: x['last_price_rub'], reverse=True)[:10]
        top_growth = sorted(companies_data, key=lambda x: x['annual_growth'], reverse=True)[:10]

        def save_to_json(data: list, filename: str, key: str):
            """Saves data to a JSON file."""
            output = [{"code": item['code'], "name": item['name'], key: item[key.lower().replace(' ', '_')]} for item in data]
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=4, ensure_ascii=False)

        # Save to JSON files
        save_to_json(top_expensive, 'top_expensive.json', 'price')
        save_to_json(top_growth, 'top_growth.json', 'growth')

        print("Data scraping and saving complete.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
