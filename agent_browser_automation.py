import os
import json
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    PromptAgentDefinition,
    BrowserAutomationPreviewTool,
    BrowserAutomationToolParameters,
    BrowserAutomationToolConnectionParameters,
)

load_dotenv()

endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(endpoint=endpoint, credential=credential) as project_client,
    project_client.get_openai_client() as openai_client,
):

    # [START tool_declaration]
    tool = BrowserAutomationPreviewTool(
        browser_automation_preview=BrowserAutomationToolParameters(
            connection=BrowserAutomationToolConnectionParameters(
                project_connection_id=os.environ["BROWSER_AUTOMATION_PROJECT_CONNECTION_ID"],
            )
        )
    )
    # [END tool_declaration]

    agent = project_client.agents.create_version(
        agent_name="pkAgent",
        definition=PromptAgentDefinition(
            model=os.environ["FOUNDRY_MODEL_NAME"],
            instructions="""You are an Agent helping with browser automation tasks.
            You can answer questions, provide information, and assist with various tasks
            related to web browsing using the Browser Automation tool available to you.""",
            tools=[tool],
        ),
    )
    print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

    stream_response = openai_client.responses.create(
        stream=True,
        tool_choice="required",
        input="""
            Your goal is to report the percent of Microsoft year-to-date stock price change.
            To do that, go to the website finance.yahoo.com.
            At the top of the page, you will find a search bar.
            Enter the value 'MSFT', to get information about the Microsoft stock price.
            At the top of the resulting page you will see a default chart of Microsoft stock price.
            Click on 'YTD' at the top of that chart, and report the percent value that shows up just below it.""",
        extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
    )

    for event in stream_response:
        if event.type == "response.created":
            print(f"Follow-up response created with ID: {event.response.id}")
        # elif event.type == "response.output_text.delta":
        #     print(f"Delta: {event.delta}")
        elif event.type == "response.text.done":
            print("\nFollow-up response done!")
        elif event.type == "response.output_item.done":
            item = event.item
            if item.type == "browser_automation_preview_call":  # TODO: support browser_automation_preview_call schema
                arguments_str = getattr(item, "arguments", "{}")

                # Parse the arguments string into a dictionary
                arguments = json.loads(arguments_str)
                query = arguments.get("query")

                print(f"Call ID: {getattr(item, 'call_id')}")
                print(f"Query arguments: {query}")
        elif event.type == "response.completed":
            print("\nFollow-up completed!")
            print(f"Full response: {event.response.output_text}")

    print("\nCleaning up...")
    project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
    print("Agent deleted")