import discord, json, os

def help(bot):
    @bot.command(name="help", aliases=["ajuda"])
    async def help_command(ctx, command: str = None):
        # Caminho para o arquivo JSON na mesma pasta
        json_path = os.path.join(os.path.dirname(__file__), "help.json")
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                help_data = json.load(f)
        except Exception as e:
            return await ctx.send(f"erro ao ler o arquivo de ajuda: {e}")

        if not command:
            embed = discord.Embed(title="🔎 Lista de Comandos", color=discord.Color.blue())
            embed.set_thumbnail(url=ctx.guild.icon.url)
            embed.add_field(name="🎶 Músicas", value="play\nstop\nskip\nqueue\nnowplaying\nbaixe", inline=True)
            embed.add_field(name="👤 User", value="avatar\nuserinfo", inline=True)
            embed.add_field(name="📌 Misc", value="ping\ncoinflip", inline=True)
            embed.add_field(name="🪄 Server", value="servericon\nserverinfo", inline=True)
            embed.set_footer(text="Use .help <comando> para detalhes")
            return await ctx.send(embed=embed)

        if command:
            cmd_key = command.lower()
            found_info = None
            
            # Procura o comando dentro das categorias do JSON
            for category in help_data.values():
                if cmd_key in category:
                    found_info = category[cmd_key]
                    break
            
            if found_info:
                embed = discord.Embed(title="".join(found_info["nome"]), color=discord.Color.blue())
                embed.set_thumbnail(url=ctx.guild.icon.url)
                embed.set_author(name=f"{''.join(found_info['icon'])} {''.join(found_info['categoria'])}")
                embed.add_field(name="📃 Descrição", value="".join(found_info["descricao"]), inline=False)
                embed.add_field(name="🔗 Aliases", value=", ".join(found_info["aliases"]), inline=True)
                embed.add_field(name="🔎 Sintaxe", value=f"`{''.join(found_info['sintaxe'])}`", inline=True)
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"comando `{command}` não encontrado. use `.help` para ver a lista.")
