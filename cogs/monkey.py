import discord
from discord.ext import commands
import random
import json
from discord.ext.commands.cooldowns import BucketType
from .donate import STAFF, SESTAFF

class Monkey(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        with open('cogs/monkey.json') as f:
            self.monkeypics = json.load(f)
        


    whitelist = STAFF + SESTAFF
    rate = 1
    per = 20

    @commands.command(name='monkey', aliases=['m'])
    @commands.cooldown(rate, per, BucketType.member)
    async def monkey(self, ctx, emoji: str):
      """m o n k e y"""
      if emoji in self.monkeypics:
        await ctx.send(self.monkeypics[emoji], reference=ctx.message.reference)
      else:
          await ctx.reply(f"no monkey emoji for {emoji} :(")


    @monkey.after_invoke
    async def reset_cooldown(self, ctx):
        for e in self.whitelist:
            #to whitelist a person:
            if e == ctx.author.id:
                self.monkey.reset_cooldown(ctx)

            #to whitelist a channel:
            if e == ctx.message.channel.id:
                self.monkey.reset_cooldown(ctx)

            #to whitelist a guild/server:
            if e == ctx.message.guild.id:
                self.monkey.reset_cooldown(ctx)

            #to whitelist a role:
            if e in [role.id for role in ctx.author.roles]:
                self.monkey.reset_cooldown(ctx)

    
    @commands.command(name='monkeyreload', aliases=['mreload', 'mr'])
    async def monkeyreload(self, ctx):
      m = await ctx.send("Reloading..")
      with open('cogs/monkey.json') as f:
          self.monkeypics = json.load(f)
      await m.edit("Reloaded monkeys")


    @commands.command(name='addmonkey', aliases=['madd'])
    async def addmonkey(self, ctx, name: str, monkey: str):
      if name in self.monkeypics.keys():
        await ctx.reply("Already exists")
      else:
        self.monkeypics[name] = monkey

        with open('cogs/monkey.json', 'w') as f:
          x = self.monkeypics
          json.dump(x, f)
    
        with open('cogs/monkey.json', 'r') as f:
          self.monkeypics = json.load(f)

        await ctx.send(f"Sucesfully added `{name}`")

    @commands.command(name='removemonkey', aliases=['removem', 'mremove'])
    @commands.is_owner()
    async def removemonkey(self, ctx, name: str):
      if name not in self.monkeypics.keys():
        await ctx.reply("Does not exist")
      else:
        del self.monkeypics[name]

        with open('cogs/monkey.json', 'w') as f:
          x = self.monkeypics
          json.dump(x, f)
    
        with open('cogs/monkey.json', 'r') as f:
          self.monkeypics = json.load(f)

        await ctx.send(f"Sucesfully removed `{name}`")



    @commands.command(name="monkeys")
    async def monkeys(self, ctx):

      desc = f"**`{len(self.monkeypics.keys())}` total monkeys**\n\n```"
      for i in self.monkeypics.keys():
        desc += f"- {i}\n"
      desc += "```"
      embed = discord.Embed(title="All monkeys", description = desc)

      await ctx.send(embed=embed)




def setup(bot):
    bot.add_cog(Monkey(bot))

# https://discord.gg/Xv83YqGKPy