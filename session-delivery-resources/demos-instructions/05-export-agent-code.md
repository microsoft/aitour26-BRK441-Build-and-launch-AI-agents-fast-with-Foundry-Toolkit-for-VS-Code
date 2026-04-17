# Demo Instructions: Export Agent Code

Export the code from the **Agent Builder** for the Cora agent. Chat with the Cora agent live via the ageng UI.

## Instructions

1. At the top right of the **Agent Builder**, select **View Code**.
1. For the **SDK** window, select **Microsoft Agent Framework**.
1. For the **Programming Language** window, select **Python**.
1. Briefly review the code.
1. Open the Cora web app window.
1. Upload the living room photo located at `img/demo-living-room.png`.
1. Enter the prompt: `Here’s a photo of my living room. I’m not sure whether I should go with eggshell or semi-gloss. Can you tell which would work better based on the lighting and layout?`
1. Submit and review the agent output. ​If the agent **does not** invoke a tool call, follow-up with another prompt asking the agent: `How much is Zava eggshell interior paint?`.
1. Review the output from the agent.

## Transcript

The transcript provided below is from the recorded demo video for [Export Agent Code](https://aka.ms/AAxq4rl). You can also view this transcript inside the speaker notes of the breakout slide deck.

**00:00:00:20 - 00:00:22:16**

For now, let's focus on getting the agent into a real world product. One of Serena's colleagues created the UI for the Cora app and passed along the project files. Therefore, the front end is complete. But what's missing is the brain behind it, the agent logic, the call to the MCP server, and the model responses within the Microsoft Foundry toolkit.

**00:00:22:21 - 00:00:47:14**

Serena can export the agent code via her preferred SDK. And so as we scroll down at the bottom, we want to have an option to view the code. And then from here we have three options available. Either the Azure AI inference SDK, semantic Kernel SDK, and then we also have the Microsoft Agent framework. Serena chose to go with the Microsoft Agent framework, in which Python was her chosen language.

**00:00:47:16 - 00:00:54:16**

And now we have the code file for the agent that was created within the agent builder.

**00:00:54:18 - 00:01:19:17**

But after getting the code for the agent, Serena still needs to merge her agent code with the existing app code. So rather than spend cycles going through her colleague’s project, she could instead leverage GitHub Copilot again to merge the agent logic with the front end logic as well, and have a fully functional app.

**00:01:19:19 - 00:01:41:13**

And I actually happen to have that app here all put together. So remember Bruno? Let's pretend we're Bruno for a second. And what we're going to need is a recommendation for painting the living room. I'll pass in that prompt from earlier which states, here's a picture of my living room. I'm not sure whether I should go with eggshell or semi-gloss.

**00:01:41:16 - 00:01:49:01**

Can you tell me which would work better based on the lighting and layout? We're going to pass in that image of Bruno's living room,

**00:01:49:05 - 00:01:53:01**

And let's see how the agent does.

**00:01:53:03 - 00:02:17:03**

So Cora's working on it. And then soon here, we should get a response from Cora based on what's been processed in that image. So, Cora has taken the image into account based on the soft, natural light, with a clean and cozy esthetic. We have the things to consider if we want to go the eggshell route or the semi-gloss route.

**00:02:17:03 - 00:02:52:06**

And in this case, Cora is recommending the eggshell paint. And we do want recommendations for the Zava eggshell paint. So let's ask Cora recommend a Zaha eggshell paint. Cora's working on it again. Somewhere behind the scenes Cora is doing a tool call. And in doing that tool call, Cora is able to find the interior eggshell paint from Zava and Cora follows up to ask would we like more details on this product or assistance with purchasing?

**00:02:52:08 - 00:03:20:18**

Naturally, I want to know how much is the product. And in asking that question, Cora is able to inform me that the eggshell paint from Zava is priced at $65.67. What you've just seen here is that the Cora agent has done two tool calls successfully and very quickly. We have gone from prototyping this Cora agent

**00:03:21:00 - 00:03:32:18**

And adding that logic into an existing app. So that way Zava can place their Cora agent into production for their customers.
