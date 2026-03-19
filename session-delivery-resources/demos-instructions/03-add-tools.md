# Demo Instructions: Add tools to an agent in Agent Builder

Connect the Cora agent to the **Zava MCP server** and add the **get_products_by_name** tool. 

Create the Cora agent in the **Agent Builder** and define it's system prompt.

## Instructions

**If you've already created a `v2-tools-agent`:**

1. Select the agent from within **Local Resources > Agents > v2-tools-agent**. This action opens the agent in the **Agent Builder**.
1. Confirm that the **gpt-4.1-mini** model is selected.
1. Proceed to **Add tool**.

**If you did not create a `v2-tools-agent`:**

1. In the **Agent Builder**, confirm that the **Cora** agent is still selected. If not, select the **Cora** agent from within **Local Resources > Agents > Local > Cora**. This action opens the agent in the **Agent Builder**
1. Confirm that the **gpt-4.1-mini** model is selected.
1. Proceed to **Add tool**

**Add tool**

1. In the **Tool** section of the **Agent Builder**, select **+ > MCP Server**.
1. In the **Add MCP Server to Agent** window, select **Use Tools Added in Visual Studio Code**.
1. In the pop up, select, **Could not find one? Browse more MCP servers** 
1. In the new window, select the **Custom** tab then under mcp.json, select the **edit button**, it will open up a new mcp.json file.
1. Go back to the **.vscode/mcp.json** file, copy the contents then paste to the new mcp.json file.
1. Go back to the Agent Builder, under tools select **+ > MCP Server**, you will find **zava-customer-sales-stdio**. Select the tool and it will be successfully added to your agent.
1. In the **User Prompt** field, enter the prompt: `Here’s a photo of my living room. I’m not sure whether I should go with eggshell or semi-gloss. Can you tell which would work better based on the lighting and layout?`​
1. Upload the living room photo located at `img/demo-living-room.png`.
1. Submit and review the output from the agent. If the agent **does not** invoke a tool call, follow-up with another prompt asking the agent: `How much is Zava eggshell interior paint?`.
1. Review the output from the agent.

## Transcript

The transcript provided below is from the recorded demo video for [Add tools to an agent in Agent Builder](https://aka.ms/AAxqc9k). You can also view this transcript inside the speaker notes of the breakout slide deck.

**00:00:00:22 - 00:00:30:21**

So back here in the Agent Builder, I can connect to Zava's custom MCP server and add whichever tools will be relevant for Cora. Zava's basic customer sales server enables Cora to do product searches by name with fuzzy matching to get store specific product availability through row level security and get real time inventory levels and stock information. I happen to already have the server running here in the background within VS code, and I can access it here via the Agent Builder. 

**00:00:30:23 - 00:00:54:13**

To connect this server and provide its tools to Cora, what I will do is scroll down here to this tool section and I can add the tools via the MCP server option, and I can use tools that are already added in VS code. Of course, however, if you would like to use a different server, you could also browse servers that are available and you can also manually add servers.

**00:00:54:13 - 00:01:22:22**

And you can also create your own servers with the AI toolkit. But I already have one running, so I'm going to select one of the ones that's running in VS code. I only need, in this case the "get products by name". So I'll just select that one and then I'll click okay. And now that tool has been added, we're going to use that same prompt from earlier with Cora to see which product Cora can recommend.

**00:01:22:22 - 00:01:51:11**

Now that Cora has access to that database of products, I'm going to start a new chat here, and then I'll go ahead and submit that prompt, as well as the image of Bruno's living room, and then we'll see what the agent does in response. Okay, we have another recommendation for Eggshell Paint. And Cora does ask would I like the agent to recommend an actual paint finish product.

**00:01:51:11 - 00:02:21:09**

I want to say yes, recommend an eggshell paint from Zava and let's see if we get a tool call. If we do get a tool call, it will display directly in the UI. And so I can see that we have one tool call that occurred for "get products by name". That is the tool that was added. And we have the actual product recommendation for the interior eggshell paint from Zava. 

**00:02:21:11 - 00:02:26:22**

We also have the price and it's readily available in stock. 

**00:02:26:22 - 00:02:48:14**

So now that Cora is up and running and connected to Zava's product catalog using MCP, Serena has a working prototype. But before she ships it, she needs to know: Is Cora actually doing what Cora is supposed to do? And are the responses clear? Are they trustworthy? And are they actually helpful for Zava's customers? Essentially, 

**00:02:48:14 - 00:02:55:19**

Serena wants to know can she trust this Cora agent to interact with real customers like Bruno? 
