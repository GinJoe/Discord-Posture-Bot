import discord
from discord.ext import commands, tasks
from discord.utils import get
import json
from random import *
import asyncio
import os


class Posture(commands.Cog):

    def __init__(self, client):
        self.client = client

        #Values are for reminder loop
        self.reminder.start()
        self.loop_count = 0


    @commands.Cog.listener()
    async def on_ready(self):
        print('Posture is ready')


    @commands.command()
    async def force_start_loop(self, ctx):
        with open('./Files/Developers.txt', 'r') as file:
            lines = file.readlines()
        if str(ctx.message.author.id) in lines:
            self.reminder.stop()
            self.reminder.start()
            self.loop_count = 0
            await ctx.send('loop reset')
        else:
            await ctx.send('You are not permitted to do that')

    #Kicks the bot from the voice channel if needed
    @commands.command()
    async def kick(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()

    #This is a function that is called every minute
    @tasks.loop(minutes = 1)
    async def reminder(self):
        print('Loop activated')
        print(f'{self.loop_count}')
        guilds = self.client.guilds

        if guilds != []:
            #open our files to read from
            with open('./Files/posturePermissions.json','r',) as file:
                permissions = json.load(file)
            with open('./Files/postureTimers.json','r') as file:
                timers = json.load(file)

            # Iterates through guilds checking if they need a posture reminder or not
            for guild in guilds:
                print(f'checking {guild.id}')
                if permissions[str(guild.id)] == 'y':
                    if self.loop_count % int(timers[str(guild.id)]) == 0 :
                        #Aims to put the bot in the channel with the most people
                        voice_channel = (max(guild.voice_channels, key=lambda k: len(k.members)))
                        if voice_channel.members != []:
                            voice = get(self.client.voice_clients, guild=guild) #Should be none initially
                            if voice and voice.is_connected():
                                await voice.move_to(voice_channel) #Voice is somewhere so we'll move it
                            else:
                                voice = await voice_channel.connect()

                            DIR = './PostureSounds'
                            dir_size = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
                            if dir_size > 0:
                                number = randint(1,1 + dir_size)

                                voice.play(discord.FFmpegPCMAudio(executable='./ffmpeg',
                                                                  source=f'./PostureSounds/PostureCheck{number}.mp3'),
                                                                  after= lambda _: self.end_of_recording(v = voice))

                                voice.source = discord.PCMVolumeTransformer(voice.source)
                                voice.source.volume = 0.50
                                print('Loop Finished')
                        else:
                            print(f'No members in voice channel: {voice_channel}')
        self.loop_count += 1

    @commands.command(aliases = ['postureON'], brief='Turns posture reminders on for your server.')
    async def enable_reminder(self,ctx):
        guild = ctx.guild.id
        with open('./Files/posturePermissions.json','r') as file:
            permissions = json.load(file)
            if permissions[str(guild)] == 'y':
                await ctx.send('Posture Check already enabled.')
            else:
                with open('./Files/posturePermissions.json', 'w') as file:
                    permissions[str(guild)] = 'y'
                    json.dump(permissions, file)
                await ctx.send('Posture Check enabled.')

    @commands.command(aliases = ['postureOFF'], brief='Turns posture reminders off for your server.')
    async def disable_reminder(self,ctx):
        guild = ctx.guild.id
        with open('./Files/posturePermissions.json','r') as file:
            permissions = json.load(file)
            if permissions[str(guild)] == 'n':
                await ctx.send('Posture Check already disabled.')
            else:
                with open('./Files/posturePermissions.json', 'w') as file:
                    permissions[str(guild)] = 'n'
                    json.dump(permissions, file)
                await ctx.send('Posture Check disabled.')

    @commands.command(aliases = ['cTimer'], brief='changes posture notifications to x minutes')
    async def change_reminder_timer(self, ctx, *, new_time):
        try:
            time = int(new_time)
            if time >= 1:
                if time <=1440: #This is longer than 24hrs so not useful for what we are doing
                    with open('./Files/postureTimers.json','r') as file:
                        timers = json.load(file)
                        timers[str(ctx.guild.id)] = time
                    with open('./Files/postureTimers.json','w') as file:
                        json.dump(timers, file)

                    await ctx.send(f'Time between checks has been changed to {time} minutes')
                else:
                    await ctx.send(f"Time can't be changed to longer to a day.\nIf you would like to disable the check use the command 'disable_reminder' with your command prefix.  ")
            else:
                await ctx.send("Number is too small, sorry.")
        except:
            await ctx.send('Incorrect input, please just enter a number')

    #Helper function for the play function in the main loop
    def end_of_recording(self, v):
        if v and v.is_connected:
            coroutine = v.disconnect()
            future = asyncio.run_coroutine_threadsafe(coroutine, self.reminder.loop )
        else:
            print('Voice was not connected')
        try:
            future.result()
        except:
            print('Error with the coroutine part')


def setup(client):
    client.add_cog(Posture(client))