import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import json
from lookup_el import can_construct_from_elements, find_elements

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

if not os.path.exists('stats.json'):
    stats = {
        'messages': 0,
        'success': 0,
        'longest': 0
    }
    with open('stats.json', 'w') as f:
        json.dump(stats, f)
else:
    with open('stats.json', 'r') as f:
        stats = json.load(f)

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('Bot is ready to go!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    text = message.content
    if len(text.split()) > 2:
        stats['messages'] += 1
        elements = can_construct_from_elements(text)

        if isinstance(elements, (list, tuple)) and elements:
            if elements[0]:
                stats['success'] += 1
                elements_found = ', '.join(elements[1])
                await message.channel.send(f'Your message can be constructed from the following elements: {elements_found}')
                elements_found = find_elements(elements[1])
                await message.channel.send(', '.join(elements_found))
                await message.channel.send(f'I have scanned {stats["messages"]} messages and {stats["success"]} could be made from only elements.')
                if stats['longest'] < len(text):
                    stats['longest'] = len(text)
                    await message.channel.send(f'New longest message: {text} at {len(text)} characters')
        with open('stats.json', 'w') as f:
            json.dump(stats, f)
        await bot.process_commands(message)

    else:
        await bot.process_commands(message)

@commands.command(name="stats", description="Display stats")
async def _stats(ctx):
    await ctx.send(f'I have scanned {stats["messages"]} messages and {stats["success"]} could be made from only elements.')
    await ctx.send(f'Longest message: {stats["longest"]} characters')

bot.add_command(_stats)

bot.run(os.getenv('TOKEN'))
