# Demo Instructions: Evaluate Agent Responses

Use **GitHub Copilot Agent Mode** to get evalator recommendations. Run both **manual** and **AI-assisted** evaluations for the agent output.

## Instructions

**If you've already created a `v3-manual-evaluation`:**

1. Select the agent from within **My Resources > Agents > v3-manual-evaluation**. This action opens the agent in the **Agent Builder**.
1. Confirm that the **gpt-4.1-mini** model is selected.
1. Switch to the **Evaluation** tab.
1. Proceed to **Manual Evaluation**.

**If you did not create a `v3-manual-evaluation`:**

1. In the **Agent Builder**, confirm that the **Cora** agent is still selected. If not, select the **Cora** agent from within **MLocal Resources > Agents > Local > Cora**. This action opens the agent in the **Agent Builder**/
1. Confirm that the **gpt-4.1-mini** model is selected.
1. Switch to the **Evaluation** tab.
1. Select **+ Add an Empty Row** 4 times.
1. Enter the following for the **User Query** values for each row of data:
    - What type of organic compost does Zava have?
    - Does Zava have a paint bucket? If so, how much is it?
    - What color glitter does Zava sell?
    - How much tape measure is currently in stock?
1. Select all rows and click **Run Response** (i.e. the play button icon).
1. Confirm that the agent has provided a response for each row.
1. Proceed to **Manual Evaluation**

**Manual Evaluation**

Review the responses for each row and select **thumbs up** or **thumbs down**.

**If you've already created a `v4-automated-evaluation`:**

1. Select the agent from within **My Resources > Agents > v4-automated-evaluation**. This action opens the agent in the **Agent Builder**.
1. Confirm that the **gpt-4.1-mini** model is selected.
1. Switch to the **Evaluation** tab.
1. Proceed to **AI-Assisted Evaluation**.

**If you did not create a `v4-automated-evaluation`:**

>[!Note]
> Running automated evaluations can take a significant amount of time. It is recommended to run this evaluation in advanced.

>[!Note]
> For your initial run of AI-assisted evaluations, the AI Toolkit extension will download and install the required dependencies. If the Cora agent web app is actively running, temporarily stop the agent as the port it's using will interfere with the evaluation dependency download. After your initial successful run of AI-assisted evaluations, you can subsequently have both the Cora app running as well as execute AI-assisted evaluations given that the required dependencies will have already been downloaded and installed in the container.

1. From the **Cora** agent, create a new evaluation via the **Add Evaluation** button.
1. Select the following evaluators: `relevance`, `coherence`.
1. Select the **gpt-4.1-mini**  model.
1. Select **Run Evaluation** > **Run Evaluation Only**.

**AI-Assisted Evalution**

1. For a better view of the results, select **Expand to Full Screen**.
1. Review the output from the agent. 


## Transcript

The transcript provided below is from the recorded demo video for [Evaluate Agent Responses](https://aka.ms/AAxqc9h). You can also view this transcript inside the speaker notes of the breakout slide deck.

**00:00:00:22 - 00:00:26:23**

So back here in the Agent Builder, we're going to switch over to the evaluation tab. The evaluation tab is what's going to enable us to start running evaluations against the Cora agent. The first thing I want to call out is our generate data feature. And that's going to be this star icon here. In the event you want to evaluate your agent but you don't yet have data, we can generate that data for you.

**00:00:27:05 - 00:00:54:03**

If you select it, you need to decide how many rows of data you would like generate it. And then we provide some generation logic based on the instructions that have been provided for your agent. You're more than welcome to modify this, just to ensure that you get the proper set of data that you're looking for. I happen to actually already have the data that Serena used when she was evaluating the Cora agent.

**00:00:54:05 - 00:01:00:03**

So I'm going to enter that manually. I can click add an empty row and I'll

**00:01:00:03 - 00:01:22:22**

Expand the screen so we can see that a little better here. I'll say what type of organic compost does Zava have. And you could also import this data as well if you'd like. The next row of data that I'll add in is does Zava have a paint bucket.

**00:01:23:00 - 00:01:29:17**

If so how much is it. Let's do another one.

**00:01:29:19 - 00:02:01:22**

We'll add in what color glitter does Zava sell. And then a fourth which will be how much tape measure is currently in stock. We have a little bit of variety here with respect to the sort of input that we could expect to receive from Zava customers. So from here what we'll need to do is run the agent so we can get the agent's response, and then we can start doing our evaluations.

**00:02:01:23 - 00:02:28:23**

You can run all these at once or individually. I'm going to run them all at once. And so I'll select run response. And then ideally what we should hopefully see is a couple of tool calls because the Cora agent does have access to the tools from Zava's MCP server that consists of the Zava products.

**00:02:29:01 - 00:02:54:15**

All right. And so we have a tool call that's kicking things off here for the very first line. And then we have another for the second. So this is pretty good. This is exactly what we want to see happening. And then we have a final one. All right. So if we take a look at what we have for the output here, I do see that we have product specific information and as we go through.

**00:02:54:15 - 00:03:04:04**

So for the first one, organic compost 40 pound is the type of fertilizer that Zava has in the garden and outdoor category and is a great choice.

**00:03:04:06 - 00:03:23:02**

Since at this stage I want to do manual evaluations, which involves a human assessing the output of the model, I'm going to say that this particular row of data is a thumbs up. As for the second row, I do see that there is a paint bucket

**00:03:23:04 - 00:03:30:11**

grid that was recommended, but it's a paint tray. It's not necessarily a paint bucket itself.

**00:03:30:13 - 00:03:56:16**

And so I would say, you know what? This one's going to be a thumbs down. The third row is a bit of a trick question because I know Zava does not actually sell glitter, but we still got a tool called to occur. And Cora was able to inform the customer that Zava does not have any glitter products, but alternative options are available depending on their needs.

**00:03:56:20 - 00:04:20:04**

So I will say yes, I do think that response deserves a thumbs up. And then the final one, with respect to how much tape measure is currently in stock, I can see that we have a response of 7162 units. And so I will say yes, that is a thumbs up. We can also have AI assess the agent output as well.

**00:04:20:04 - 00:04:45:18**

And that will be an AI assisted evaluation. To set that up, what we'll do is add the evaluation itself. But at this stage let's say I don't quite know which evaluators to use. And that's okay because we could use GitHub Copilot to help recommend evaluators. And to do so we're going to open back up GitHub copilot from earlier.

**00:04:45:20 - 00:05:09:10**

And we're going to pass in a new prompt that says which evaluators do you recommend that I should use to do evaluations for my agent. And so what we're going to see here is that GitHub Copilot is going to invoke another AI toolkit tool, which is the evaluation planner.

**00:05:09:12 - 00:05:29:15**

If I was working with the code files for this agent, then GitHub Copilot would take what's in the project into account as it starts working through this workflow of creating the AI assisted evaluations for my agent, but because we're still working in the toolkit, that's not available.

**00:05:29:15 - 00:06:04:20**

But that's okay, because without that, we can still get evaluator recommendations. And there's two here in particular that I do believe I want to focus on. One is the relevance evaluator as well as the coherence evaluator. This feature is very helpful if you are challenged with creating evaluations. GitHub Copilot provides some very helpful guidance and will take you through the full workflow of choosing your evaluators, creating data sets if you don't have one, and then also creating the evaluation script as well.

**00:06:04:22 - 00:06:34:14**

Our evaluations are using the Azure AI evaluation SDK and its built in evaluators. But alternatively, you could also create custom evaluators as well. For now, I'm going to use the built in evaluators that we have. So heading back to add evaluations, I'm going to use relevance and Coherence and click okay. And now I need to choose the language model that I want to use as the AI that does these AI assisted evaluations.

**00:06:34:16 - 00:06:39:23**

I want to use GPT 4.1 mini. And then from there,

**00:06:40:01 - 00:07:18:12**

what we're going to have are the relevance and coherence columns. Add it to our evaluations for our agent. You can run all evaluations at once or you can do them one at a time. I'm going to run the evaluations for the very first row. So I'll just select that one followed by run evaluation only. And what this is going to do is assess the output about the organic composts fertilizer for its relevance and coherence.

**00:07:18:14 - 00:07:52:04**

Okay. So we do have output here. And you can either view the output in this view. Alternatively you can actually open up this particular row of data. And this will bring you into viewing information by the row in particular. Not only do you have the input itself, but we have the evaluation results as well. And I can see that out of a range of 1 to 5, with five being the highest, relevance scored four, and then coherence scored four as well.

**00:07:52:05 - 00:08:17:14**

When you complete evaluations with the Azure AI evaluation SDK, you do also receive the relevance reason. You get the coherence reason, and you'll get the reasoning for the other built in evaluators as well. In addition to that, over on the right hand side, I can also see the model response, any tool response, and then the final model response, which is going to be the output that goes directly to our end user.


