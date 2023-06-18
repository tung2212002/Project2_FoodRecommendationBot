from rasa.core.agent import Agent
import os
import discord

MODEL_NAME = "20230618-130528-novel-curry.tar.gz"
with open("secret.txt", "r") as f:
    TOKEN = f.readline()

cur_path = os.getcwd()

model_path = os.path.join(cur_path, "models", MODEL_NAME)

agent = Agent()
model = agent.load_model(model_path=model_path)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Get the user's message
    user_message = message.content

    # Get the Rasa agent's response
    rasa_response = await agent.handle_text(user_message)

    # Extract the text from the Rasa response
    response_text = rasa_response[0]["text"]

    # Send the response to the Discord channel
    await message.channel.send(response_text)

client.run(TOKEN)