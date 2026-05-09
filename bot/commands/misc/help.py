import discord, json, os
from commands.languageservice import languageservice

def help(bot):
    @bot.command(name="help", aliases=["ajuda"])
    async def help_command(ctx, command: str = None):
        help_data = await languageservice(bot, ctx, "misc", "help.json")
        if not help_data: return

        ui = help_data["ui"]

        if not command:
            embed = discord.Embed(title=ui["menu_title"], color=discord.Color.blue())
            if ctx.guild.icon:
                embed.set_thumbnail(url=ctx.guild.icon.url)
                
            embed.add_field(name=ui["category_songs"], value="play\nstop\nskip\nqueue\nnowplaying\ndownload", inline=True)
            embed.add_field(name=ui["category_user"], value="avatar\nuserinfo", inline=True)
            embed.add_field(name=ui["category_misc"], value="ping", inline=True)
            embed.add_field(name=ui["category_server"], value="servericon\nserverinfo", inline=True)
            embed.add_field(name=ui["category_fun"], value="coinflip\nlolgen\nleaguelink\nleagueinfo", inline=True)
            
            if ctx.author.guild_permissions.administrator:
                embed.add_field(name=ui["category_admin"], value="prefix\nlanguage\nconfig\nclear\nban\nkick\nunban", inline=True)

            embed.set_footer(text=ui["menu_footer"].format(prefix=ctx.prefix))
            return await ctx.send(embed=embed)

        if command:
            cmd_key = command.lower()
            found_info = None
            
            # Procura o comando dentro das categorias do JSON
            for key, category in help_data.items():
                if key == "ui": continue # Pula a seção de UI na busca de comandos
                if cmd_key in category:
                    found_info = category[cmd_key]
                    break
            
            if found_info:
                embed = discord.Embed(title="".join(found_info["nome"]), color=discord.Color.blue())
                if ctx.guild.icon:
                    embed.set_thumbnail(url=ctx.guild.icon.url)
                embed.set_author(name=f"{''.join(found_info['icon'])} {''.join(found_info['categoria'])}")
                
                # Formata os aliases com o prefixo atual, ignorando se for "Nenhum"
                aliases_list = found_info["aliases"]
                formatted_aliases = ", ".join([f"{ctx.prefix}{a}" for a in aliases_list]) if aliases_list[0] != "Nenhum" else "Nenhum"
                
                embed.add_field(name=ui["desc_title"], value="".join(found_info["descricao"]), inline=False)
                embed.add_field(name=ui["aliases_title"], value=formatted_aliases, inline=True)
                embed.add_field(name=ui["syntax_title"], value=f"`{ctx.prefix}{''.join(found_info['sintaxe'])}`", inline=True)
                
                await ctx.send(embed=embed)
            else:
                await ctx.send(ui["cmd_not_found"].format(command=command, prefix=ctx.prefix))
