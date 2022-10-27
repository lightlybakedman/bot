import discord
from discord.ext import commands
from googlesearch import search

from discord import ui
from discord import utils

class resultsview(ui.View):
    def __init__(self, results, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.results = results
        self.page = 0

    async def updatebuttons(self, interaction):
        prev = utils.get(self.children, custom_id='prev')
        pagenum = utils.get(self.children, custom_id='pagenum')
        next = utils.get(self.children, custom_id='next')

        if self.page == 0:
            prev.disabled = True
        else:
            prev.disabled = False

        if self.page == len(self.results) - 1:
            next.disabled = True
        else:
            next.disabled = False

        pagenum.label = f'{self.page + 1}/{len(self.results)}'

        await interaction.edit_original_message(view=self)


    @ui.button(label = "⮜", custom_id="prev", style = discord.ButtonStyle.blurple, disabled = True)
    async def previous(self, interaction, button):
        await interaction.response.defer()
        self.page -= 1
        await interaction.edit_original_message(content = self.results[self.page])
        await self.updatebuttons(interaction)

    @ui.button(label = '1', custom_id="pagenum", disabled = True)
    async def pagecounter(self, interaction, button):
        await interaction.response.defer()

    @ui.button(label = "⮞", custom_id="next", style = discord.ButtonStyle.blurple)
    async def next(self, interaction, button):
        await interaction.response.defer()
        self.page += 1
        await interaction.edit_original_message(content = self.results[self.page])
        await self.updatebuttons(interaction)

    @ui.button(label = "⠀", style = discord.ButtonStyle.red)
    async def stop(self, interaction, button):
        await interaction.response.defer()
        await self.stop()

class Google(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def getgoogleresults(self, query):
        results = []
        for j in search(query, tld="com", num=20, stop=20, pause=1):
            results.append(j)
        return results

    @commands.command(name="google", aliases=["g"])
    async def google(self, ctx, *, query):
        async with ctx.typing():
            searches = self.getgoogleresults(query)

        if len(searches) == 0: 
            await ctx.send("No results found.")
            return

        msg = await ctx.send(searches[0], view=resultsview(searches))


async def setup(bot):
    await bot.add_cog(Google(bot))