import discord
from discord.ext import commands
import os
import json
import asyncio
import typing
from cogs.webhooklog import webhooklog

fNum = lambda x: "{:,}".format(float(x))

from config import TOKEN, COGS, PREFIX

intents = discord.Intents.all()

class mybot(commands.Bot):
    async def setup_hook(self):
      for cog in COGS:
        await bot.load_extension(cog)

      await bot.load_extension('jishaku')

bot = mybot(command_prefix=commands.when_mentioned_or(PREFIX),
                      intents=intents,
                      owner_ids=[494030648433049611])

import os
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"

os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True" 
os.environ["JISHAKU_HIDE"] = "True"
os.environ["JISHAKU_FORCE_PAGINATOR"] = "True"

@bot.event
async def on_ready():
    print(f"Bot online as {bot.user}")


bot.run(TOKEN)

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
