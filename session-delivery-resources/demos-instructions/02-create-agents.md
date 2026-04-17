# Demo Instructions: Create an Agent

Create the Cora agent in the **Agent Builder** and define it's system prompt.

## Instructions

**If you've already created a `v1-basic-agent`:**

1. Select the agent from within **My Resources > Local Resources > Agents > v1-basic-agent**. This action opens the agent in the **Agent Builder**.
1. Confirm that the **gpt-4.1-mini** model is selected.
1. Provide a high-level overview of what was completed thus far to familiarize the audience with the **Agent Builder**.
1. Proceed to **Chat with Cora**.

**If you did not create a `v1-basic-agent`:**

1. Open up the **Developer Tools** select **Build > + Create Agent**.
1. In the new tab, select **Open Agent Builder.**
1. Name the agent **Cora**.
1. For the model, select **gpt-4.1-mini (Remote via Microsoft Foundry)**.
1. Enter the following for the **Instructions**:
    ```
    You are Cora, an intelligent and friendly AI assistant for Zava, a home improvement brand. You help customers with their DIY projects by understanding their needs and recommending the most suitable products from Zava’s catalog.​

    Your role is to:​

    - Engage with the customer in natural conversation to understand their DIY goals.​
    - Ask thoughtful questions to gather relevant project details.​
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
1. In the top left of the chat, select the **drop down arrow > Save to Local**
1. Proceed to **Chat with Cora**.

**Chat with Cora**

1. In the **User Prompt** field, enter the prompt: `Here’s a photo of my living room. I’m not sure whether I should go with eggshell or semi-gloss. Can you tell which would work better based on the lighting and layout?`​
1. Upload the living room photo located at `/workspace/img/demo-living-room.png`.
1. Submit and review the output from the agent.

## Transcript

The transcript provided below is from the recorded demo video for [Create Agents with Agent Builder](https://aka.ms/AAxq4rm). You can also view this transcript inside the speaker notes of the breakout slide deck.

**00:00:01:19 - 00:00:22:18**

Here within the Microsoft Foundry toolkit, I will open up the Agent Builder. With this open, I can now create the Cora agent. Starting off with giving the agent a name. We'll name the agent Cora as mentioned. And then we want to make sure that we've chosen the proper model. And in our case, we want to use GPT 4.1 mini from Microsoft Foundry.

**00:00:22:20 - 00:00:42:14**

Now that the model has been loaded, we can pass in a system prompt for the agent. If you are challenged with creating system prompts, then no problem, because we have a feature in the Microsoft Foundry toolkit where we can generate a system prompt for you. What you'll need to do is pass in a description of the task that your agent will be completing.

**00:00:42:19 - 00:00:57:06**

And then we're leveraging AI to generate the system prompt for you. I happen to actually already have the system prompt that Serena used when creating the Cora agent. So I'll put that in here.

**00:00:57:08 - 00:01:28:14**

Now it is quite lengthy, so I won't read it in its entirety, but to get a gist of what's happening here, the agent is intelligent, friendly, and it's helping customers from the Zava brand, a home improvement brand. And then we go on to define the agents role. We also include information about the personality as well. In the event I would like some assistance with improving the system prompt, we have a feature available in here that can help you out as well.

**00:01:28:16 - 00:01:48:11**

Notice where we once had the generate button. It now says improve. If you pass in a system prompt and you would like improvement, you can choose the improve button. And then you can describe what it is you want to change. Once you describe what it is you want to change. We will also use AI again to help make the improvements.

**00:01:48:12 - 00:01:59:07**

And then from there you can decide which you want to keep, what you want to get rid of, and so on and so forth. So I'll close that up, because we're going to use the one that Serena created.

**00:01:59:09 - 00:02:22:00**

So now let's give this agent a try. As it is going to submit a prompt that customers like Bruno may submit. We're going to use his living room image and it says, here's a photo of my living room. I'm not sure whether I should go with eggshell or semi-gloss. Can you tell which would work better based on the lighting and layout?

**00:02:22:02 - 00:02:50:03**

We're going to go ahead and submit that here to the Cora agent, and let's just see how the Cora agent responds. So Cora is able to process what's happening in the image that we've passed in. Core insists that it has a soft, natural light coming through a window in its cozy, understated decor style. And so given the ample light and the elegant but relaxed vibe, eggshell is what Cora is recommending.

**00:02:50:05 - 00:02:52:14**

And so from here.

**00:02:52:16 - 00:03:16:10**

Cora is asking follow up questions to the customer. So that way it can better determine whether the eggshell paint is going to be most appropriate. But although we have this recommendation from Cora at this step, what is missing is the fact that Cora does not yet have access to Zava's product catalog.

**00:03:16:12 - 00:03:22:02**

And this is where MCP or Model Context Protocol comes into play.
