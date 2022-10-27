import discord
from discord.ext import commands
from replit import db
import asyncio
from .webhooklog import webhooklog
import json
import typing
from typing import Optional, Union

fNum = lambda x: "{:,}".format(x)

SENIOR_STAFF_ROLE = 909624295125299280
STAFF_ROLE = 904695662938050632
SHC_SENIOR_ADMIN = 837970266155778058
SHC_STAFF = 832571429861326888

STAFF = [STAFF_ROLE, SHC_STAFF]
SESTAFF = [SENIOR_STAFF_ROLE, SHC_SENIOR_ADMIN]


def getBal(id):
    try:
        return db[str(id)]
    except KeyError:

        db[str(id)] = 0
        return 0


def setBal(id, bal: int):
    db[str(id)] = bal


def addBal(id, bal: float):
    db[str(id)] = float(getBal(id)) + float(bal)


with open('config.json') as f:
    config = json.load(f)

    prefix = config.get("prefix")
    cogs = config.get("cogs")


class hexcolour():
    red = 0xff3838
    orange = 0xffb302
    yellow = 0xfce83a
    green = 0x56f000
    blue = 0x2dccff
    gray = 0x9ea7ad


class Donate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def updateconfig(self, ctx):
        """Reload config"""
        global SENIOR_STAFF_ROLE, STAFF_ROLE, prefix
        with open('config.json') as f:
            config = json.load(f)

            prefix = config.get("prefix")
            await ctx.reply("> Updated config.json")

    @commands.command(name='balance', aliases=['bal'])
    async def balance(self, ctx, user: Optional[Union[discord.Member,
                                                      discord.User]]):
        """Get balance of a user or author"""
        if not user: user = ctx.author
        await ctx.send(f"{user.mention}'s balance is `{fNum(getBal(user.id))}`"
                       )

    @commands.has_any_role(*STAFF, *SESTAFF)
    @commands.command(name="donate", aliases=['d', 'dn'])
    async def donate(self, ctx, user: Union[discord.Member, discord.User],
                     amount):
        """Log donations"""
        amount = amount.rstrip().replace(',', '')
        try:
            float(amount)
        except ValueError:
            await ctx.reply(embed=discord.Embed(
                description="Invalid amount\n Must be a number",
                color=hexcolour.red))
        else:
            amount = float(amount)
            embed = discord.Embed(
                title="Confirm donation",
                description=f"Member: {user.mention}\nAmount: {fNum(amount)}")
            msg = await ctx.send(embed=embed)
            await msg.add_reaction("✅")
            await msg.add_reaction("❌")

            def check(reaction, u):
                return u.id == ctx.author.id and str(
                    reaction.emoji) in ['✅', '❌']

            try:
                reaction, u = await self.bot.wait_for('reaction_add',
                                                      timeout=10,
                                                      check=check)
            except asyncio.TimeoutError:
                await ctx.send("timeout")
            else:

                if str(reaction.emoji) == "✅":
                    addBal(user.id, amount)
                    await ctx.send(
                        embed=discord.Embed(description="Succesfully donated",
                                            color=hexcolour.green))
                    await webhooklog(f"""```yaml
Staff   : {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})
User    : {user.name}#{user.discriminator} ({user.id})
Added   : {fNum(amount)}
New Bal : {fNum(getBal(user.id))}
```""")

                elif str(reaction.emoji) == "❌":
                    await ctx.send(embed=discord.Embed(description="Cancelled",
                                                       color=hexcolour.gray))

    @commands.has_any_role(*SESTAFF, *STAFF)
    @commands.command(name="setbal", aliases=['set', 'sb'])
    async def setbal(self, ctx, user: Union[discord.Member, discord.User],
                     amount):
        """Set donation balance"""
        amount = amount.rstrip().replace(',', '')
        try:
            float(amount)
        except ValueError:
            await ctx.reply(embed=discord.Embed(
                description="Invalid amount\n Must be a number",
                color=hexcolour.red))
        else:
            amount = float(amount)
            embed = discord.Embed(
                title="Confirm set bal",
                description=f"Member: {user.mention}\nAmount: {fNum(amount)}")
            msg = await ctx.send(embed=embed)
            await msg.add_reaction("✅")
            await msg.add_reaction("❌")

            def check(reaction, u):
                return u.id == ctx.author.id and str(
                    reaction.emoji) in ['✅', '❌']

            try:
                reaction, u = await self.bot.wait_for('reaction_add',
                                                      timeout=10,
                                                      check=check)
            except asyncio.TimeoutError:
                await ctx.send("timeout")
            else:

                if str(reaction.emoji) == "✅":
                    setBal(user.id, amount)
                    await ctx.send(
                        embed=discord.Embed(description="Succesfully set bal",
                                            color=hexcolour.green))
                    await webhooklog(f"""```yaml
Staff   : {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})
User    : {user.name}#{user.discriminator} ({user.id})
Set bal : {amount}
```""")

                elif str(reaction.emoji) == "❌":
                    await ctx.send(embed=discord.Embed(description="Cancelled",
                                                       color=hexcolour.gray))

    @commands.command()
    @commands.has_any_role(SESTAFF)
    async def imp(self, ctx, id, amount: float):
        """Import donations"""
        try:
            setBal(id, amount)
        except Exception as e:
            await ctx.send(embed=discord.Embed(description=f"```py\n{e}```",
                                               color=hexcolour.red))
        else:
            await ctx.send(f"Set {id} to {fNum(amount)}")

    @commands.command()
    async def allbal(self, ctx):
        """View all balances"""
        msg = ''
        if db.keys():
            for id in db.keys():
                msg += f"{id}: {db[str(id)]}\n"

        else:
            msg = 'No donations'
        await ctx.send(embed=discord.Embed(
            description="```yaml\n" + msg + "```", color=hexcolour.blue))

    @commands.command()
    @commands.is_owner()
    async def delall(self, ctx):
        """Delete all donations"""
        embed = discord.Embed(description=f"Delete all?")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")

        def check(reaction, user):
            return user.id == ctx.author.id and str(
                reaction.emoji) in ['✅', '❌']

        try:
            reaction, user = await self.bot.wait_for('reaction_add',
                                                     timeout=10,
                                                     check=check)
        except asyncio.TimeoutError:
            await ctx.send("timeout")
        else:

            if str(reaction.emoji) == "✅":
                for key in db.keys():
                    del db[key]
                await ctx.reply("> Deleted all")
                await ctx.send(
                    embed=discord.Embed(description="Succesfully deleted all",
                                        color=hexcolour.green))
                await webhooklog("```diff\n- DELETED ALL```")

            elif str(reaction.emoji) == "❌":
                await ctx.send(embed=discord.Embed(description="Cancelled",
                                                   color=hexcolour.gray))


def setup(bot):
    bot.add_cog(Donate(bot))
