import discord
from datetime import *
from random import *
from discord.ext import commands

class Scribe(commands.Cog):

    #TODO: Error checking.

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener() #What we type for an event decorator
    async def on_ready(self):
        print('Scribe is ready')

    @commands.command(aliases =['quote','q'], description = 'Note down a quote in the format: "quote" -author', brief= 'make a quote in the format: "quote" -author'  ) #What we type for a command decorator
    async def scribe(self, ctx, *, quote):

        quote = quote.replace(',','')
        quote = quote.replace('"','')
        quoteSides = quote.split("-")
        for sides in quoteSides:
            sides = sides.strip()
        author = "Unknown"

        #Sorting out time things
        now = datetime.today()
        day = now.day
        month = now.month
        year = now.year
        date = f'{day}/{month}/{year}'

        quote = quoteSides[0]
        if len(quoteSides) > 1:
            author = quoteSides[1]
        if len(quoteSides) > 2:
            date = quoteSides[2]
        await ctx.send(f'{author} said: "{quote}" recorded on: {date}')

        g_id = ctx.guild.id

        file = open(f'./QuoteSheets/{g_id}.txt','a')
        file.write(f'{author},{quote},{date}\n')
        file.close()

    @commands.command(aliases = ['display','show'], description = 'Shows all quotes and their indexes', brief = 'Shows all the quotes and their indexes.')
    async def show_all(self, ctx):
        g_id = ctx.guild.id

        with open(f'./QuoteSheets/{g_id}.txt', 'r') as file:
            count = 1
            for line in file:
                p_line = pretty_print(line)
                string = f'{count}: {p_line}'
                count += 1
                await ctx.send(string)


    @commands.command(brief = 'Says a random quote.' )
    async def speak(self, ctx, *, person=None):
        g_id = ctx.guild.id
        with open(f'./QuoteSheets/{g_id}.txt', 'r') as file:
            lines = file.readlines()
            if person is None:
                size = len(lines)
                if size != 0:
                    number = randint(0, size - 1)
                    line = pretty_print(lines[number])
                    number += 1
                    await ctx.send(f'{number}: {line}',tts=True)
                else:
                    await ctx.send('There are no quotes at the moment')
            else:
                p_quotes = []
                for line in lines:
                    sections = line.split(',')
                    author = sections[0].strip()
                    if author.upper().strip() == person.upper().strip():
                        p_quotes.append(line)
                if p_quotes == []:
                    await ctx.send(f"Sorry we don't seem to have any quotes by {person}\n Perhaps you could add one?")
                else:
                    size = len(p_quotes)
                    number = randint(0, size - 1)
                    line = pretty_print(p_quotes[number])
                    await ctx.send(f'{line}',tts=True)



    @commands.command(aliases = ['delete','del'], description = 'Deletes a quote by it\'s Index number. To find an index use the show_all command.' , brief = 'Deletes a quote by it\'s Index number.')
    async def delete_quote(self, ctx, number):
        g_id = ctx.guild.id
        try:
            number = int(number)
            deleted = ''
            await ctx.send(f"Deleting... quote number: {number}")
            with open(f'./QuoteSheets/{g_id}.txt', "r") as f:
                lines = f.readlines()
                if (number > len(lines)) or (number < 1):
                    raise ValueError("nah fam that ain't a valid number")
            with open(f'./QuoteSheets/{g_id}.txt', "w") as f:
                for count, line in enumerate(lines,1):
                    if number != count:
                        f.write(f'{line}\n')
                    else:
                        deleted = pretty_print(line)

            await ctx.send(f"Deleted {deleted} Successfully")
        except ValueError as msg:
            print(msg)
            await ctx.send(f"Entered value: '{number}' is either too big or too small or is not a number. Please try again.")

    @commands.command(aliases = ['random', 'rand'], brief = 'Shows a random quote or one by a particular author if used like: show_random (author) '
        , description = 'shows a random quote or one by a particular author if used like: show_random (author) ' )
    async def show_random(self, ctx,person=None):
        g_id = ctx.guild.id
        with open(f'./QuoteSheets/{g_id}.txt','r') as file:
            lines = file.readlines()
            if person is None:
                size = len(lines)
                if size != 0:
                    number = randint(0, size-1)
                    line = pretty_print(lines[number])
                    number += 1
                    await ctx.send(f'{number}: {line}')
                else:
                    await ctx.send('There are no quotes at the moment')
            else:
                p_quotes = []
                for line in lines:
                    sections = line.split(',')
                    author = sections[0]
                    if author.upper() == person.upper():
                        p_quotes.append(line)
                if p_quotes == []:
                    await ctx.send(f"Sorry we don't seem to have any quotes by {person}\n Perhaps you could add one?")
                else:
                    size = len(p_quotes)
                    number = randint(0, size-1)
                    line = pretty_print(p_quotes[number])
                    await ctx.send(f'{line}')

    @commands.command(aliases = ['undo'], brief = 'deletes the last quote made.', description= 'deletes the last quote made, this cannot be undone.')
    async def oops(self, ctx):
        g_id = ctx.guild.id
        with open(f'./QuoteSheets/{g_id}.txt',"r") as file:
            lines = file.readlines()
        with open(f'./QuoteSheets/{g_id}.txt','w') as file:
            for count,line in enumerate(lines, 1):
                if count == len(lines):
                    string = pretty_print(line)
                    await ctx.send(f'Deleted: {string}')
                else:
                    file.write(line)


def setup(client):
    client.add_cog(Scribe(client))

def pretty_print(string):
    sections = string.split(',')
    quote = sections[1]
    author = sections[0]
    date = sections[2]
    return_string = f'"{quote}" -{author}, {date}'
    return return_string