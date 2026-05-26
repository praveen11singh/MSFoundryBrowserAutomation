# MSFoundry Browser Automation

An AI-powered browser automation agent built on **Azure AI Foundry** (formerly Azure AI Studio). This project demonstrates how to create and run an autonomous agent that can navigate web pages, interact with UI elements, and extract real-time information using Microsoft's `BrowserAutomationPreviewTool`.

---

## Overview

This project uses the Azure AI Projects SDK to spin up a prompt-based agent equipped with browser automation capabilities. The example task navigates to Yahoo Finance, searches for the Microsoft (MSFT) stock ticker, and retrieves the year-to-date (YTD) price change percentage — all autonomously.

---

## Features

- Connects to Azure AI Foundry via `AIProjectClient`
- Creates and destroys versioned agents programmatically
- Uses `BrowserAutomationPreviewTool` to perform real browser interactions
- Streams response events in real time
- Automatically cleans up agents after task completion

---

## Prerequisites

- Python 3.9+
- An [Azure subscription](https://azure.microsoft.com/en-us/free/)
- An **Azure AI Foundry** project with:
  - A deployed model (e.g. `gpt-4o`)
  - A **Browser Automation** connection configured
- Azure CLI authenticated (`az login`) or a suitable credential for `DefaultAzureCredential`

---

## Installation

```bash
# Clone the repository
git clone https://github.com/praveen11singh/MSFoundryBrowserAutomation.git
cd MSFoundryBrowserAutomation

# Create and activate a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install azure-ai-projects azure-identity python-dotenv
```

---

## Configuration

Create a `.env` file in the project root (one is already included — update the values):

```env
FOUNDRY_PROJECT_ENDPOINT=https://<your-foundry-project>.cognitiveservices.azure.com/
FOUNDRY_MODEL_NAME=gpt-4o
BROWSER_AUTOMATION_PROJECT_CONNECTION_ID=<your-browser-automation-connection-id>
```

| Variable | Description |
|---|---|
| `FOUNDRY_PROJECT_ENDPOINT` | Your Azure AI Foundry project endpoint URL |
| `FOUNDRY_MODEL_NAME` | The deployed model name to use for the agent |
| `BROWSER_AUTOMATION_PROJECT_CONNECTION_ID` | The connection ID for the Browser Automation resource in your Foundry project |

> ⚠️ **Never commit your `.env` file.** Add it to `.gitignore` to avoid exposing secrets.

---

## Usage

```bash
python agent_browser_automation.py
```

The script will:
1. Create a versioned agent named `pkAgent` with browser automation capabilities
2. Issue a task to navigate Yahoo Finance and retrieve the MSFT YTD stock change
3. Stream and print events as the agent works through the task
4. Print the final result
5. Delete the agent version upon completion

### Example Output

```
Agent created (id: abc123, name: pkAgent, version: 1)
Follow-up response created with ID: resp_xyz
...
Follow-up completed!
Full response: Microsoft's YTD stock price change is +12.34%
Cleaning up...
Agent deleted
```

---

## Project Structure

```
MSFoundryBrowserAutomation/
├── agent_browser_automation.py   # Main script — agent creation and task execution
├── .env                          # Environment variables (do not commit)
└── .pkvenv/                      # Virtual environment (local only)
```

---

## How It Works

```
┌─────────────┐     Create Agent      ┌──────────────────────┐
│   Script    │ ─────────────────────▶ │  Azure AI Foundry    │
│             │                        │  (AIProjectClient)   │
│             │   Stream Response      │                      │
│             │ ◀───────────────────── │  Agent + Browser     │
│             │                        │  Automation Tool     │
└─────────────┘                        └──────────────────────┘
                                               │
                                     Navigates browser
                                               │
                                       ┌───────▼────────┐
                                       │  finance.yahoo │
                                       │      .com      │
                                       └────────────────┘
```

The agent receives a natural language instruction, uses the `BrowserAutomationPreviewTool` to open a real browser session on Azure, performs the required interactions, and streams back the result.

---

## References

- [Azure AI Foundry Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/)
- [Azure AI Projects SDK (Python)](https://pypi.org/project/azure-ai-projects/)
- [Browser Automation Tool Preview](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/tools/browser-automation)
- [DefaultAzureCredential](https://learn.microsoft.com/en-us/python/api/azure-identity/azure.identity.defaultazurecredential)

---

## License

This project is provided as-is for demonstration and learning purposes. See [LICENSE](LICENSE) for details if applicable.
