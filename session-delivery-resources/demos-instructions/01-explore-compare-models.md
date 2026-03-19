# Explore and Compare Models

Use **GitHub Copilot Agent Mode** to get model recommendations. Browse the **Model Catalog** in the AI Toolkit and compare 2 models within the **Model Playground**.

## Instructions

1. Open **GitHub Copilot** and select **Agent Mode** and one of the **Claude** models (ex: **Claude Sonnet 4.5**). 
1. Ask GitHub Copilot:
    ```I'm creating an agent for a home improvement company. The agent uses the company's product catalog via a MCP server to recommend the right products for customers based on their DIY project. Which language model should I use?```
1. Under **Discover** open the **Model Catalog** and provide a high-level overview of it's features. Search for **gpt-4.1-nano** (or whichever alternate model GitHub Copilot recommends) and select **Add model** for the **GitHub** hosted version of the model.
1. Open the **Model Playground** and select **Compare**. Choose to compare the **gpt-4.1-mini** model and the alternate aforementioned model (ex: **gpt-4.1-nano**).
1. Attach the image located at `img/demo-living-room.png`. Enter the prompt: `Describe what’s in the image, including colors of the objects`. 
1. Submit and review the output from the models.

## Transcript

The transcript provided below is from the recorded demo video for [Explore and Compare Models](https://aka.ms/AAxqj4z). You can also view this transcript inside the speaker notes of the breakout slide deck.

**00:00:00:10 - 00:00:22:15**

So here within Visual Studio Code, I'm going to open up GitHub Copilot chat. Once this is open I can expand this. So that way I can see a bit more on the screen. Now, right now what we're going to need is a recommendation of model or models to help run the Cora agent. And so I'm passing in a prompt that says I'm creating an agent for a home improvement company.

**00:00:22:17 - 00:00:47:07**

The agent uses a company's product catalog via a MCP server to recommend the right products for customers based on their DIY project. Which language model should I use? Now that that's been sent, what's going to happen is that GitHub Copilot is going to leverage one of the AI toolkit tools that it has access to. And in this case, it's using the get AI model guidance tool.

**00:00:47:09 - 00:01:12:01**

This particular tool is going to assist GitHub Copilot with understanding the best practices around model recommendation. And we do seem to have an answer here. So if I scroll up I can see that the overall choice in model is GPT 4.1 mini. It takes things into consideration, such as the quality score. So that's taking things like benchmarks into account.

**00:01:12:03 - 00:01:35:22**

Then there's costs. And this is going to be very helpful because Zava would like to have a better understanding of how much these models are going to cost when they're being used in production, or at least to have an estimate of what their total cost will be as customers are using the Cora agent. We also have additional information here with respect to latency.

**00:01:36:02 - 00:02:05:14**

We really want to ensure that the Cora agent doesn't necessarily take too long to provide a response to customers. And then we also have information here about the context window. There's information here about coding. That's not as necessary for this agent, but it does call out that it does excel in instruction following. Just below that, GitHub copilot recommended a budget friendly alternative, which is going to be GPT 4.1 nano.

**00:02:05:16 - 00:02:32:09**

And also it does note here that if we just want to get started with trying something free, we could try the GPT 4.1 mini model using one of the GitHub hosted models. And so from here, the next thing that we would need to do is actually go test out this model and let's assess how well it performs against our given scenario.

**00:02:32:11 - 00:02:37:16**

So to do that we're going to open up the model catalog in the AI toolkit.

**00:02:37:18 - 00:03:02:23**

Within the model catalog. We're able to see a variety of models that are going to be available for use. And as we scroll down we can apply different filters such as who's the model hosted by the model publisher. Features as well. So knowing that we want to use a model that supports image attachments, that will be a really good feature to apply here.

**00:03:03:01 - 00:03:21:05**

And we can also look at model types. And then also if we need fine tuning support, I already know that I want to give the GPT 4.1 mini model a try, and so I can search for that one directly.

**00:03:21:07 - 00:03:31:12**

And here I see that we have a couple of options available. There's one from GitHub. There's one from Microsoft Foundry as well. And then there's also one from open AI.

**00:03:31:14 - 00:03:43:00**

Since Zava would like to develop agents for Microsoft Foundry, we're going to use a Microsoft Foundry model. So from here what we would do is deploy that model.

**00:03:43:00 - 00:04:10:06**

I happen to already have it deployed, so I won't redeploy it. In addition to that, there was another model that was mentioned by GitHub copilot, and that's going to be GPT 4.1 nano. Let's see where that model may be. We do have that one available as a GitHub hosted model. So we'll go ahead and add that model as well.

**00:04:10:08 - 00:04:15:01**

What we'll want to do now is test out these models in the model playground.

**00:04:15:02 - 00:04:40:12**

So I'll open back up the AI toolkit here, and I'll go to the model playground within the model playground. This is where we can come and compare two models at a time. If you want to just test out one model, you would stay right here within this area. But I want to compare. And so I want to start off with the GPT 4.1 mini model.

**00:04:40:12 - 00:04:53:00**

And that's going to be the Foundry model. And I can also select the GPT 4.1 nano model. That's going to be the GitHub hosted model.

**00:04:53:02 - 00:05:15:13**

What will want to do now is pass in a prompt that's going to be suitable for a given scenario. And so I have a prompt which is describe what's in the image, including colors of the objects. I happen to have that same image of Bruno's living room available. So we're going to pass that one in. These are the sort of conversations that we can expect for the customers to have with the Cora agent.

**00:05:15:15 - 00:05:43:07**

I'll go ahead and submit that. Notice that we submit the prompt once and it will populate on the other side for the other model that we're comparing with. And we do have responses as well. I do believe 4.1 many, was a hair bit faster. But what we would do now at this step if we were in Serena shoes is just review the output, determine which of the two we like most, and then that's what we would move forward with.


