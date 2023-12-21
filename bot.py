import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from lookup_el import can_construct_from_elements, find_elements

load_dotenv()

#enable message intents
intents = discord.Intents.default()
intents.message_content = True



bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print('Bot is ready to go!')

@bot.event
async def on_message(message):  
    if message.author == bot.user:
        return

    text = message.content
    #if more than 1 word, do this else pass
    if len(text.split()) > 2:
        elements = can_construct_from_elements(text)

        # Check if elements is a list or tuple and has elements to process
        if isinstance(elements, (list, tuple)) and elements:
            if elements[0]:
                elements_found = ', '.join(elements[1])
                await message.channel.send(f'Your message can be constructed from the following elements: {elements_found}')
                elements_found = find_elements(elements[1])
                await message.channel.send(', '.join(elements_found))


        await bot.process_commands(message)  # Process other commands

    else:
        await bot.process_commands(message)


#start bot
bot.run(os.getenv('TOKEN'))