import requests
import pandas as pd

# Assuming df is your original dataframe and 'base_token_urls' is the column with URLs
def fetch_data(url):
    # Request data from the URL and return it as a pandas Series or DataFrame
    response = requests.get(url)
    data = response.json()  # adjust this line based on the response format
    return pd.Series(data)

# Use apply to fetch data for all URLs and create a new dataframe
new_df = df['base_token_urls'].apply(fetch_data)

# Merge the new dataframe with the original one
result_df = pd.concat([df, new_df], axis=1)
