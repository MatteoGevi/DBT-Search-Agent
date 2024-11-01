# DBT-Search-Agent
Slack Extension as Search Assistant for DBT Models. 

## DBT Cloud Connection

I am using my personal profile to retrieve the metadata and use them to be ingested inside.
https://vq708.us1.dbt.com/70403103965332/projects/70403103976794/setup

## LLM vs NLP Models Approach

For computational matters, NLP can serve really well for if the query is well done. And yet, I do not expect any organisation to be able to handle technical debt when models start piling up. Hence, using LLM can be effective in large organisations. 

## Test Walkthrough

	1.	Initialize the Project with dbt init.
	2.	Define Sources and Models in .yml and .sql files.
	3.	Load Data with dbt seeds if needed.
	4.	Run dbt and Test the setup.
	5.	Use the dbt Metadata API for exploring model metadata.
	6.	Locally test the conversational chatbot
    7.  Integrate with Slack for model search functionality (optional).


