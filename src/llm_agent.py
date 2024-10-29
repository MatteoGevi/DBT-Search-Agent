import requests
import pandas as pd
from constants import CLAUDE_API_TOKEN, CLAUDE_API_URL

# Placeholder metadata - Assuming you have the dbt metadata DataFrame from the previous step
dbt_metadata_df = pd.DataFrame({
    "Model Name": ["customer_data", "sales_data", "product_info"],
    "Model Description": ["Customer demographic and behavior data", "Sales transaction records", "Product specifications"],
    "Column Name": ["customer_id", "sale_id", "product_id"],
    "Column Description": ["Unique customer identifier", "Unique sale identifier", "Unique product identifier"]
})

def prepare_prompt(user_question):
    """Prepare a prompt with metadata context for Claude."""
    
    # Summarize dbt metadata as context
    metadata_summary = "\n".join([
        f"Model: {row['Model Name']}\nDescription: {row['Model Description']}\nColumns: {row['Column Name']} - {row['Column Description']}"
        for _, row in dbt_metadata_df.iterrows()
    ])
    
    # Create a full prompt
    prompt = (
        f"You are a data assistant with knowledge of dbt project metadata. Here is an overview of the models available:\n\n"
        f"{metadata_summary}\n\n"
        f"The user asked: '{user_question}'\n"
        f"Based on the metadata above, please provide relevant information or suggest relevant models and fields."
    )
    
    return prompt

def query_claude(prompt):
    """Send prompt to Claude and retrieve the response."""
    
    headers = {
        "Authorization": f"Bearer {CLAUDE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": prompt,
        "model": "claude-v1",
        "max_tokens_to_sample": 300
    }
    
    response = requests.post(CLAUDE_API_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("completion")
    else:
        print(f"Error querying Claude API: {response.status_code}")
        return None

def main():
    user_question = input("Ask a question about the dbt data models: ")
    prompt = prepare_prompt(user_question)
    response = query_claude(prompt)
    
    if response:
        print("Claude's response:\n")
        print(response)
    else:
        print("Failed to get a response from Claude.")

if __name__ == "__main__":
    main()