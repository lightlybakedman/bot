import discord
from discord.ext import commands
import os
from replit import db
import json
import asyncio
import typing
from cogs.webhooklog import webhooklog
from keep_alive import keep_alive

token = os.environ['token']

fNum = lambda x: "{:,}".format(float(x))

with open('config.json') as f:
    config = json.load(f)
    cogs = config.get("cogs")
    prefix = config.get("prefix")



class hexcolour():
    red = 0xff3838
    orange = 0xffb302
    yellow = 0xfce83a
    green = 0x56f000
    blue = 0x2dccff
    gray = 0x9ea7ad



intents = discord.Intents.all()

bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix),
                      intents=intents,
                      owner_ids=[494030648433049611])


# @bot.command(name='info', aliases=['stats'])
# async def info(ctx):
#     """Bot info"""
#     embed = discord.Embed(title="SHC Donations Bot Stats",
#                           color=hexcolour.blue)
#     embed.add_field(name="Ping", value=f"`{round(bot.latency * 1000)}ms`")
#     embed.add_field(name="Donations",
#                     value=f"`{len(db.keys())}` people have donated")
#     await ctx.send(embed=embed)





import os
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"

os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True" 
os.environ["JISHAKU_HIDE"] = "True"
os.environ["JISHAKU_FORCE_PAGINATOR"] = "True"

@bot.event
async def on_ready():
    print(f"Bot online as {bot.user}")
    keep_alive()
    for cog in cogs:
        await bot.load_extension(cog)

    await bot.load_extension('jishaku')


def startup():
    try:
        bot.run(token)
    except Exception as e:
        print(f"> Invalid Token")
        print(e)
        input()
        os._exit(0)


if __name__ == "__main__":
    startup()

# Commands:
# Stats - list info, number of donations, total
# Ping
# Settings:
#   Prefix
#   Staff roles
# Add donation
# Donation History

# @commands.has_any_role(SENIOR_STAFF_ROLE, STAFF_ROLE)
# @commands.has_permissions(administrator = True)
# allowed_mentions = discord.AllowedMentions(roles=False)
