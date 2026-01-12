## How to deliver this session

🥇 Thanks for delivering this session!

Prior to delivering the workshop please:

1.  Read this document and all included resources included in their entirety.
2.  Watch the video presentation
3.  Ask questions of the content leads! We're here to help!


## 📁 File Summary

| Resources          | Links                            | Description |
|-------------------|----------------------------------|-------------------|
| Session Delivery Deck     |  [Deck](https://aka.ms/AAxryus) | The session delivery slides |
| Full Session | [Recording Link](https://youtu.be/3fFXFpAYC4M) | The full session presentation |

## 🕐Timing

The breakout is divided into multiple sections including 31 slides and 5 demos.

| Time        | Description 
--------------|-------------
0:00 - 3:04   | Intro and overview
3:05 - 4:19   | GenAI ops
4:20 - 12:20  | Meet the models
12:21 - 19:52 | Design your agent
19:53 - 31:15 | Evaluate your agent responses
31:16 - 38:35 | From prototype to production
38:36 - 40:15 | Wrap up and Q&A

## 🖥️Demo Videos

Select the demo name to view instructions for how to deliver the demo. A full transcript with timing is included for each demo. You can also find a copy of the full transcript within the speaker notes of the breakout slide deck.

| Demo        | Description | Video 
--------------|-------------|-------------
[Explore and Compare Models](/01-session-delivery-resources/demos-instructions/explore-compare-models.md)   | Use **GitHub Copilot Agent Mode** to get model recommendations. Browse the **Model Catalog** in the AI Toolkit and compare 2 models within the **Model Playground**. | [Demo video](https://aka.ms/AAxqj4z)
[Create Agents with Agent Builder](/02-session-delivery-resources/demos-instructions/create-agents.md)   | Create the Cora agent in the **Agent Builder** and define it's system prompt. |  [Demo video](https://aka.ms/AAxq4rm)
[Add Tools to an Agent in Agent Builder](/03-session-delivery-resources/demos-instructions/add-tools.md)   | Connect the Cora agent to the **Zava MCP server** and add the **get_products_by_name** tool. | [Demo video](https://aka.ms/AAxqc9k)
[Evaluate Agent Responses](/04-session-delivery-resources/demos-instructions/evaluate-agent-responses.md)   |  Use **GitHub Copilot Agent Mode** to get evalator recommendations. Run both **manual** and **AI-assisted** evaluations for the agent output. | [Demo video](https://aka.ms/AAxqc9h)
[Export Agent Code](/05-session-delivery-resources/demos-instructions/export-agent-code.md)   | Export the code from the **Agent Builder** for the Cora agent. Chat with the Cora agent live via the ageng UI. | [Demo video](https://aka.ms/AAxq4rl)

## 🏋️Prepare Your Environment

The demos for this breakout are designed to be run in a development container for easy setup. The container includes the following:
- PostgresSQL dataset for Zava
- **Customer Sales Server** that does basic product search using traditional name-based matching
- A web app of the Cora agent app

### Prerequisites

#### Required Accounts

- [Azure](https://signup.azure.com/) subscription
- [GitHub](https://www.github.com) with a [GitHub Copilot](https://github.com/github-copilot/signup) subscription

#### Development Environment

- [Python 3.10](https://www.python.org/downloads/) (or higher)
- [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli-windows?view=azure-cli-latest&pivots=winget) - Used for Azure authentication and resource management
- [Visual Studio Code](https://code.visualstudio.com/download)
  - [AI Toolkit](https://aka.ms/AIToolkit) extension
  - [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) extension
  - [Azure Resources](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azureresourcegroups) extension
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed
- [Microsoft Foundry](https://ai.azure.com) project (created with the **new** Foundry experience)
  - **GPT-4.1-mini** model deployment

### Setup the Demo

**Open the repository in the dev container**

1. Open **Docker Desktop**.
1. Fork and clone this repository in Visual Studio Code.
1. When prompted by Visual Studio Code, select to "Reopen in Container". Alternatively, open the **Command Palette** (i.e. CTRL/CMD+Shift+P) and enter **Dev Containers: Reopen in Container**.
1. Wait for the setup to complete. The dev container will build automatically with all dependencies pre-installed. This includes PostgresSQL with pgvector extension, a Python environment, and all required packages.

**Confirm extensions are installed**

Confirm that the dev container has installed the following extensions:
- [Azure Resources](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azureresourcegroups)
- [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- [AI Toolkit](https://aka.ms/AIToolkit)

If any extension is missing, install before moving forward.

> [!NOTE]
> The [Microsoft Foundry](https://marketplace.visualstudio.com/items?itemName=TeamsDevApp.vscode-ai-foundry) extension is installed as a bundle with the [AI Toolkit](https://aka.ms/AIToolkit). The [Azure Resources](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azureresourcegroups) extension is installed as a bundle with the [Microsoft Foundry](https://marketplace.visualstudio.com/items?itemName=TeamsDevApp.vscode-ai-foundry) extension.*

**Sign-in to the Azure Resources extension and set your default project.**

1. In the **Azure Resources** extension, select **Sign in to Azure**.
1. Sign-in to the account that has your Microsoft Foundry project and GPT-4.1-mini deployed model.
1. Once signed in, expand your subscription in the **Azure Resources** extension and then expand **Microsoft Foundry**.
1. Right click your Microsoft Foundry project name and selct **Open in Microsoft Foundry Extension**. This action sets the default project.
1. If your project is **not** set as the default project, hover over the project name in the **Microsoft Foundry** extension and click the **Switch Default Project in Azure Extension** icon (*note: the icon looks like 3 lines and is only visble when hovering over the project name*).
1. In the **Pick a project** window, select the subscription that has your Microsoft Foundry project.
1. In the **Pick a project** window, select your Microsoft Foundry project.

**Authenticate via the Azure CLI**

1. Open the terminal in Visual Studio Code.
1. Run the command `az login` or `az login --tenant {your tenant} --use-device-code`.
1. Copy the code the terminate and navigate to the URL provided.
1. Enter the code.
1. Sign-in to the same tenant used to create your Microsoft Foundry project.
1. In the Visual Studio Code terminal, select your subscription.

**Setup environment variables**
1. In the terminal, run the command: `cp .env.example .env`
1. Open your new `.env` file.
1. Update the placeholder for `AZURE_AI_FOUNDRY_ENDPOINT="<your_Microsoft_Foundry_endpoint>"` (*note: you can locate the **project endpoint** on the welcome screen of the new Microsoft Foundry experience; ex: https://{foundry-resource-name}.services.ai.azure.com/api/projects/{project-name}*)

**Start the Customer Sales Server**

1. Navigate to the **.vscode/mcp.json** file.
1. Click **Start** above the **zava-customer-sales-stdio** server.

**Start the Cora web app**

1. In the terminal, run the command `python src/python/web_app/web_app.py`.
1. In the browser, navigate to [https://localhost:8000](http://localhost:8000).
1. Confirm that the green **Connected** label displays in the top-right of the UI.

**Create 4 iterations of the Cora agent within the AI Toolkit**

Although you can create the agent live during the demo, it's recommend to already have saved verisons of the Cora agent prepared to mitigate latency or errors with setup.

**V1 Agent - Basic**

1. In the AI Toolkit, navigate to the **Agent Builder**.
1. Create a new agent named **Cora**.
1. For the **Model** field, select **gpt-4.1-mini (Remote via Microsoft Foundry)**.
1. For the **Instructions** field, enter the following:

  ```
  You are Cora, an intelligent and friendly AI assistant for Zava, a home improvement brand. You help customers with their DIY projects by understanding their needs and recommending the most suitable products from Zava’s catalog.​
  
  Your role is to:​
  
  - Engage with the customer in natural conversation to understand their DIY goals.​
  - Ask thoughtful questions to gather relevant project details.
  - Be brief in your responses.​
  - Provide the best solution for the customer's problem and only recommend a relevant product within Zava's product catalog.​
  - Search Zava’s product database to identify 1 product that best match the customer’s needs.​
  - Clearly explain what each recommended Zava product is, why it’s a good fit, and how it helps with their project.​
  ​
  Your personality is:​
  
  - Warm and welcoming, like a helpful store associate​
  - Professional and knowledgeable, like a seasoned DIY expert​
  - Curious and conversational—never assume, always clarify​
  - Transparent and honest—if something isn’t available, offer support anyway​
  
  If no matching products are found in Zava’s catalog, say:​
  “Thanks for sharing those details! I’ve searched our catalog, but it looks like we don’t currently have a product that fits your exact needs. If you'd like, I can suggest some alternatives or help you adjust your project requirements to see if something similar might work.”​
  ```
1. Scroll to the bottom of the Agent Builder and select **Save Version**. Name the version **v1-basic-agent**.

**V2 Agent - Tools**

1. From the **v1-basic-agent**, clear the chat window.
2. Scroll to the bottom of the Agent Builder and select **Save Version**. Name the version **v2-tools-agent**. 

**V3 Agent - Manual Evaluation**

1. From the **v2-tools-agent** agent, switch to the **Evaluation** tab.
1. Select **+ Add an Empty Row** 4 times.
1. Enter the following for the **User Query** values for each row of data:
    - What type of organic compost does Zava have?
    - Does Zava have a paint bucket? If so, how much is it?
    - What color glitter does Zava sell?
    - How much tape measure is currently in stock?
1. Select all rows and click **Run Response** (i.e. the play button icon).
1. Confirm that the agent has provided a response for each row.
1. Scroll down to the bottom of the Agent Builder and select **Save Version**. Name the version **v3-manual-evaluation**.

**V4 Agent - Automated Evaluation**

>[!Note]
> Running automated evaluations can take a significant amount of time. It is recommended to run this evaluation in advanced.

>[!Note]
> For your initial run of AI-assisted evaluations, the AI Toolkit extension will download and install the required dependencies. If the Cora agent web app is actively running, temporarily stop the agent as the port it's using will interfere with the evaluation dependency download. After your initial successful run of AI-assisted evaluations, you can subsequently have both the Cora app running as well as execute AI-assisted evaluations given that the required dependencies will have already been downloaded and installed in the container.

1. From the **v3-manual-evaluation** agent, create a new evaluation via the **Add Evaluation** button.
1. Select the following evaluators: `relevance`, `coherence`.
1. Select the **gpt-4.1-mini**  model.
1. Select **Run Evaluation** > **Run Evaluation Only**.
1. Scroll down to the bottom of the Agent Builder and select **Save Version**. Name the version **v4-automated-evaluation**.
