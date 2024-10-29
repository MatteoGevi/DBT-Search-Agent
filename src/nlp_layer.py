import re

def search_models(prompt, dbt_df):
    keywords = prompt.lower().split()
    matched_models = dbt_df[dbt_df['description'].str.contains('|'.join(keywords), case=False) |
                            dbt_df['columns'].apply(lambda cols: any(word in cols for word in keywords))]
    return matched_models