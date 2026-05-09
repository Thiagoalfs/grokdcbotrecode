import discord
from discord.ext import commands
from commands.languageservice import languageservice

def setup_unban_command(bot):
    @bot.command(name="unban", aliases=["desbanir"])
    @commands.has_permissions(ban_members=True)
    async def unban(ctx, user_id: int, *, reason: str = None):
        responses = await languageservice(bot, ctx, "admin", "unban.json")
        reason = reason or responses["default_reason"]

        try:
            user = await bot.fetch_user(user_id)
            await ctx.guild.unban(user, reason=reason)
            await ctx.send(responses["success"].format(user=user.name, reason=reason), delete_after=10)
        except discord.NotFound:
            await ctx.send(responses["not_found"].format(id=user_id), delete_after=5)
        except Exception as e:
            await ctx.send(responses["error"].format(error=e), delete_after=5)

    @unban.error
    async def unban_error(ctx, error):
        responses = await languageservice(bot, ctx, "admin", "unban.json")
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(responses["no_permission"], delete_after=5)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(responses["missing_arg"].format(prefix=ctx.prefix), delete_after=5)