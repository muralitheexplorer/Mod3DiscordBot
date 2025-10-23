from dotenv import load_dotenv
from openai import OpenAI
import discord
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
oa_client = OpenAI(api_key=OPENAI_API_KEY)

def call_openai(question):
    completion = oa_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": f"Respond like a pirate to the following question: {question}"
            }
        ]
    )

    response = completion.choices[0].message.content
    print(response)
    return response

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

    if message.content.startswith('$hi'):
        await message.channel.send('Hi!, I am your bot')

    if message.content.startswith('$question'):
        print(f"Message received: {message.content}")
        message_content = message.content.split()
        question = message_content[1]
        print(f"Question: {question}")
        response = call_openai(question)
        print(f"Response: {response}")
        await message.channel.send(response)

client.run(os.getenv('TOKEN'))