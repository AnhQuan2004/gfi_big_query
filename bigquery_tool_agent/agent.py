from google.adk.agents import Agent
import google.auth
from google.adk.tools.bigquery import BigQueryCredentialsConfig, BigQueryToolset
from google.adk.tools.bigquery.config import BigQueryToolConfig, WriteMode
import json

# Configure BigQuery tool
tool_config = BigQueryToolConfig(write_mode=WriteMode.ALLOWED)

# Define a credentials config - here we are using application default credentials
# https://cloud.google.com/docs/authentication/provide-credentials-adc
application_default_credentials, _ = google.auth.default()
credentials_config = BigQueryCredentialsConfig(
    credentials=application_default_credentials
)

# Instantiate a BigQuery toolset
bigquery_toolset = BigQueryToolset(
    credentials_config=credentials_config,
    bigquery_tool_config=tool_config
)

# We'll let the agent handle the query parsing and SQL generation
# No need for hardcoded functions

# Function to transform BigQuery results to the desired format
def transform_results(results):
    """
    Transform BigQuery results to a more structured format based on the actual data received.
    The function dynamically adapts to the columns present in the results.
    """
    transformed_results = []
    
    for item in results:
        # Create a base transformed item with the primary key
        transformed_item = {}
        
        # Identify the primary key (usually coin_id or similar)
        primary_key = None
        for key in item:
            if key.endswith('_id') or key == 'id':
                primary_key = key
                transformed_item[primary_key] = item[primary_key]
                break
        
        if primary_key is None and len(item) > 0:
            # If no ID field found, use the first field as primary key
            primary_key = list(item.keys())[0]
            transformed_item[primary_key] = item[primary_key]
        
        # Process score fields (ending with _score)
        for key in item:
            if key.endswith('_score'):
                transformed_item['result'] = item[key]
                break
        
        # Create detail object with counts and lists
        detail = {}
        for key in item:
            if key.endswith('_count'):
                base_name = key.replace('_count', '')
                detail[f'total_{base_name}'] = item[key]
            elif key.endswith('_list'):
                base_name = key.replace('_list', '')
                detail[f'{base_name}_detail'] = item[key]
        
        if detail:
            transformed_item['detail'] = detail
        
        # Add remaining fields that weren't specifically transformed
        for key, value in item.items():
            if (key != primary_key and 
                not key.endswith('_score') and 
                not key.endswith('_count') and 
                not key.endswith('_list')):
                transformed_item[key] = value
        
        # Add source information if primary key looks like a coin_id
        if primary_key and primary_key == 'coin_id':
            transformed_item['primary_source'] = 'coingecko'
            transformed_item['source'] = 'coingecko'
            transformed_item['source_link'] = f'https://www.coingecko.com/en/coins/{item[primary_key]}'
        
        transformed_results.append(transformed_item)
    
    return transformed_results

# We'll use post-processing instructions instead of callbacks
# The agent will need to manually transform the results using the transform_results function

# Create the Agent
root_agent = Agent(
    name="BigQuery_Agent",
    model="gemini-2.5-pro",
    description=(
        "Agent to answer questions about BigQuery data and models and execute "
        "SQL queries from natural language."
    ),
    instruction="""
    You are an expert Google BigQuery SQL query generator. Your sole purpose is to convert a simplified, logic-based input into a complete, structured, and runnable BigQuery SQL query, following a strict set of rules.
    
    After executing the query, you should process the results to make them more useful.
    
    When you receive results from a BigQuery query, follow these steps:
    
    1. First, show the original query results to the user
    2. Then, explain what the results mean in plain language
    3. If the user asks for a specific format, try to structure your response accordingly
    
    The results should be presented in a clear, readable format that helps the user understand the data.

Core Rules:

Table Path: The final query must always use the hardcoded project and dataset path: `gfi-455410`.raw_data.TABLE_NAME, where TABLE_NAME is extracted from the input logic.

Standard Columns: The SELECT statement must always contain the following columns in this specific order:
a. The column being grouped by (e.g., coin_id).
b. The result of the COUNT(DISTINCT ...) operation, aliased as COLUMN_NAME_count.
c. The result of the conditional CASE statement, aliased as COLUMN_NAME_score.
d. An array of the distinct values, aliased as COLUMN_NAME_list. The formula for this is: ARRAY_AGG(DISTINCT COLUMN_NAME IGNORE NULLS).

Logic Translation:

Translate count distinct COLUMN into COUNT(DISTINCT COLUMN).

Translate if...then...else logic into a CASE WHEN ... THEN ... END statement.

Translate group by COLUMN into a GROUP BY COLUMN clause.

Ordering: Always end the query with an ORDER BY clause, sorting by the column you grouped by.

Output Format: The output must be a single, clean SQL code block and nothing else.

Example:

Input Logic:

get col market.name in table raw_gecko_volume_profile
count distinct market.name group by coin_id
if count = 1 then return 1
if count > 3 then return 2
else return 0


Expected SQL Output:

SELECT
  coin_id,
  COUNT(DISTINCT market.name) AS distinct_market_names_count,
  CASE
    WHEN COUNT(DISTINCT market.name) = 1 THEN 1
    WHEN COUNT(DISTINCT market.name) > 3 THEN 2
    ELSE 0
  END AS market_name_score,
  ARRAY_AGG(DISTINCT market.name IGNORE NULLS) AS market_names_list
FROM
  `gfi-455410`.raw_data.raw_gecko_volume_profile
GROUP BY
  coin_id
ORDER BY
  coin_id;

    """,
    tools=[bigquery_toolset]
)

# If this module is run directly, export the agent
if __name__ == "__main__":
    # Export the agent for use with the ADK web server
    root_agent.export()