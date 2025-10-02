# Natural Language Queries for BigQuery Agent

This agent can translate natural language queries into SQL and execute them against BigQuery.

## Query Format

You can use natural language with optional special syntax:

- Table names in brackets: `[table_name]`
- Column names in brackets: `[column_name]`
- Conditional logic: `if X then Y else Z`
- Aggregations: `count`, `sum`, `average`, etc.
- Grouping: `group by [column]`

## Example 1: Market Name Analysis

```
get col [market.name] in table [raw_gecko_volume_profile] 
count distinct [market.name] group by [coin_id] 
if count = 1 then return 1 
if count > 3 then return 2 
else return 0
```

The agent will translate this to appropriate SQL with:
- SELECT with coin_id and COUNT(DISTINCT market.name)
- CASE statement for the conditional logic
- GROUP BY and ORDER BY clauses
- Limiting results to 5-10 rows

## Example 2: Price Volatility Analysis

```
get col [price.usd] in table [raw_gecko_price_profile]
count distinct [price.usd] group by [coin_id]
if count > 10 then return "High Volatility"
else return "Stable"
```

## Example 3: Volume Analysis

```
get col [volume.usd] in table [raw_gecko_volume_profile]
average [volume.usd] group by [market.name]
if average > 1000000 then return "High Volume"
if average > 100000 then return "Medium Volume"
else return "Low Volume"
```

## Example 4: Free-form Query

```
Show me the top 5 coins with the highest trading volume yesterday
```

## Example 5: Complex Analysis

```
Compare the average price of Bitcoin across different markets 
over the last week and show which market had the least volatility
```

## How to Use

1. Start the ADK web server: `adk web`
2. Access the web interface at http://127.0.0.1:8000
3. Select the BigQuery Tool Agent
4. Enter your natural language query
5. The agent will analyze, generate SQL, and execute it
