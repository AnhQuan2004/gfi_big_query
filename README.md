# ADK BigQuery Agent

This repository contains agents built with Google's Agent Development Kit (ADK) that can interact with BigQuery.

## Setup

1. Install the ADK:
```bash
pip install google-adk
```

2. Set up Google Cloud credentials:
```bash
gcloud auth application-default login
```

3. Set your Google Cloud Project ID:
```bash
export GOOGLE_CLOUD_PROJECT=your-project-id
```

4. Run the ADK web server:
```bash
adk web
```

## Agents

### BigQuery Tool Agent
Located in `bigquery_tool_agent/`, this agent can:
- Answer questions about BigQuery data
- Execute SQL queries
- Interact with BigQuery models

### My First Agent
Located in `my_first_agent/`, this is a simple agent that uses Google Search to answer queries.

## Environment Configuration

Create `.env` files in both agent directories:

### For bigquery_tool_agent/.env:
```
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_LOCATION=us-central1
GOOGLE_API_KEY=your-api-key
```

### For my_first_agent/.env:
```
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_LOCATION=us-central1
GOOGLE_API_KEY=your-api-key
```

Replace the values with your actual project ID, preferred location, and API key.

## Troubleshooting

If you encounter errors, make sure you have:
1. Set up the `.env` files correctly in each agent directory
2. Logged in with `gcloud auth application-default login`
3. Installed all required dependencies from requirements.txt
