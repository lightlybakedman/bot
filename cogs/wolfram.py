import discord
from discord.ext import commands
import aiohttp
import urllib

url = lambda query: f"https://api.wolframalpha.com/v1/result?i={urllib.parse.quote(query)}&appid=QYHWEJ-UHR5P6383W"


class Wolfram(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="wolfram", aliases = ["solve", "s"])
    async def wolfram(self, ctx, *, q):
        async with ctx.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get(url(q)) as r:
                    ans = await r.text()
        failmsg = ["Wolfram|Alpha did not understand your input", "No short answer available"]


        c = discord.Colour.blurple()
        if ans.rstrip() in failmsg: 
          c = discord.Colour.red()

        emb = discord.Embed(description=f"```\n{ans}```", color = c)
        await ctx.reply(embed=emb)
    

def setup(bot):
    bot.add_cog(Wolfram(bot))