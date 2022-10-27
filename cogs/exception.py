import discord
from discord.ext import commands
import traceback

class hexcolour():
    red = 0xff3838
    orange = 0xffb302
    yellow = 0xfce83a
    green = 0x56f000
    blue = 0x2dccff
    gray = 0x9ea7ad


class CommandErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(error, "original"): 
            error = error.original
        message = None
        if isinstance(error, commands.CommandOnCooldown):
            message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
        elif isinstance(error, commands.MissingPermissions):
            message = f"You are missing the required permissions to run this command! `{error.missing_perms}`"
        elif isinstance(error, commands.MissingRequiredArgument):
            message = f"Missing a required argument: `{error.param}`"
        elif isinstance(error, commands.ConversionError):
            message = str(error)

        elif isinstance(error, commands.MissingAnyRole):
            message = f"You do not have the role required for this command: "
            for role in error.missing_roles:
              message += f"<@&{role}> "

        elif isinstance(error, commands.CommandNotFound):
            pass

        else:
            tb=''.join(traceback.format_exception(etype=type(error), value=error, tb=error.__traceback__))  
            print(tb)
            emb = discord.Embed(title="Something went wrong", color=discord.Colour.red())
            emb.add_field(name='**Command**', value=f"`{ctx.message.content}`", inline=False)
            emb.add_field(name='**Error**', value=f"```py\n{str(error)[:1000]}```", inline=False)
            emb.add_field(name='**Traceback**', value=f"```py\n{tb[:1000]}```", inline=False)
            await ctx.reply(embed=emb)
            


        if message: 
            await ctx.reply(message, delete_after=10, allowed_mentions = discord.AllowedMentions(roles=False))

async def setup(bot):
    await bot.add_cog(CommandErrorHandler(bot))