import discord
import os
import json
from discord.ext import commands

# Token for your discord bot here
TOKEN = 'NzAzNzI1MjIwMjc5NzQ2NzQx.XqSxsg.klZf1fBvAfNoOR6rc_yua3cJ148'


def get_prefix(client, message):
    with open('./Files/prefixes.json','r') as file:
        prefixes = json.load(file)

    return prefixes[str(message.guild.id)]


client = commands.Bot(command_prefix = get_prefix)


@client.event
async def on_ready():
    print("Bot is Ready")

#This function is called when a bot has been added to a server
@client.event
async def on_guild_join(guild):

    #Initialise default prefix here
    with open('./Files/prefixes.json','r') as file:
        prefixes = json.load(file)
    #Setting new guild to default prefix of '.'
    prefixes[str(guild.id)] = '.'

    with open('./Files/prefixes.json','w') as file:
        json.dump(prefixes,file)

    '''------------SCRIBE COG INITIALISING----------------'''

    # making a quotesheet for the new server
    g_id = str(guild.id)
    file = open(f'./QuoteSheets/{g_id}.txt', 'w')
    file.close()

    '''------------POSTURE COG INITIALISING---------------'''

    # making posture permissions entry for the server
    with open('./Files/posturePermissions.json','r',) as file:
        permissions = json.load(file)
    #Initialises as no first
    permissions[g_id] = 'n'
    with open('./Files/posturePermissions.json', 'w') as file:
        json.dump(permissions,file)

    # making posture timer entry
    with open('.Files/postureTimers.json', 'r', ) as file:
        timers = json.load(file)
    # Initialises as 45 minutes
    timers[g_id] = '45'
    with open('./Files/postureTimers.json', 'w') as file:
        json.dump(timers, file)


#Called when a Server wants to remove the bot.
@client.event
async def on_guild_remove(guild):
    with open('./Files/prefixes.json','r') as file:
        prefixes = json.load(file)
    #Removes server prefix
    prefixes.pop(str(guild.id))

    with open('./Files/prefixes.json','w') as file:
        json.dump(prefixes,file)

    #Removing QuoteSheet
    g_id = str(guild.id)
    os.remove(f'./QuoteSheets/{g_id}.txt')

    #Removing posture data
    with open('.Files/posturePermissions.json', 'r', ) as file:
        permissions = json.load(file)

    permissions.pop(g_id)
    with open('./Files/posturePermissions.json', 'w') as file:
        json.dump(permissions, file)

    # Removing Timer data
    with open('.Files/postureTimers.json', 'r', ) as file:
        timers = json.load(file)

    timers.pop(g_id)
    with open('./Files/postureTimers.json', 'w') as file:
        json.dump(timers, file)

#Commands by default are called in discord using the "." prefix. You can change that here
@client.command(aliases = ['changeP'], brief='Changes the prefixes for the server')
async def change_prefix(ctx, prefix):
    with open('./Files/prefixes.json','r') as file:
        prefixes = json.load(file)
    prefixes[str(ctx.guild.id)] = prefix

    with open('./Files/prefixes.json','w') as file:
        json.dump(prefixes,file)


@client.command()
async def get_id(ctx):
    await ctx.send(str(ctx.message.author.id))


@client.command(brief ='returns latency of bot', description='returns latency of bot')
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency*1000)}ms')


# Cog commands

@client.command(brief='Dev command: loads Cogs for development', description = 'Dev command: loads Cogs for development')
async def load(ctx, extension):
    with open('./Files/Developers.txt','r') as file:
        lines = file.readlines()
    if str(ctx.message.author.id) in lines:
        client.load_extension(f'Cogs.{extension}')
    else:
        await ctx.send('You are not permitted to do that')


@client.command(brief= 'Dev command: unloads Cogs for development', description = 'Dev command: unloads Cogs for development' )
async def unload(ctx, extension):
    with open('./Files/Developers.txt','r') as file:
        lines = file.readlines()
    if str(ctx.message.author.id) in lines:
        client.unload_extension(f'Cogs.{extension}')
    else:
        await ctx.send('You are not permitted to do that')

@client.command(brief= 'Dev command: basically a refresh button', description = 'Dev command: Reloads cogs so that updates go through to an already working bot')
async def reload(ctx, extension):
    with open('./Files/Developers.txt','r') as file:
        lines = file.readlines()
    if str(ctx.message.author.id) in lines:
        client.unload_extension(f'Cogs.{extension}')
        client.load_extension(f'Cogs.{extension}')
    else:
        await ctx.send('You are not permitted to do that')


for filename in os.listdir('./Cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'Cogs.{filename[:-3]}')


client.run(TOKEN)
