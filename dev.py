import requests

STOCK_API_KEY = "57ADL90TO3X3D8B0"
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
NEWS_API_KEY = "e77b859f046049cf95e883ab367a77b0"
LINK = "https://newsapi.org/v2/everything"
# params = f"{STOCK}from=2023-03-25&sortBy=popularity&apiKey={API_KEY}"
# r = requests.get(LINK, params=params)
# print(r.status_code)
# print(r.json())


# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={STOCK}&interval=5min&apikey={STOCK_API_KEY}'
r = requests.get(url)
data = r.json()

print(data)
## STEP 1: Use https://newsapi.org
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

## STEP 2: Use https://www.alphavantage.co
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

