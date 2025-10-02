from google.adk.agents import Agent
from google.adk.tools import google_search
import os

root_agent = Agent(
    name = "my_first_agent",
    model = "gemini-2.5-pro",
    description = "An example agent that will answer user query based on Google Search",
    instruction = """
    You are a helpful assistant that provides information based on the user's query.
    """,
    tools = [google_search]
)