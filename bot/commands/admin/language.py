import discord
from discord.ext import commands
from commands.languageservice import languageservice

def setup_language_command(bot):
    @bot.command(name="language", aliases=["idioma", "lang"])
    @commands.has_permissions(administrator=True)
    async def language(ctx, new_lang: str = None):
        responses = await languageservice(bot, ctx, "admin", "language.json")
        # Dicionário de linguagens suportadas
        available_langs = {
            "ptbr": "Português 🇧🇷",
            "en": "English 🇺🇸"
        }

        # Se não passar argumento ou o argumento for inválido, mostra as opções
        if not new_lang or new_lang.lower() not in available_langs:
            # Busca a linguagem configurada no banco (padrão EN)
            data = await bot.db.fetch_one("SELECT language FROM botsettings WHERE guild_id = %s", (ctx.guild.id,))
            current_code = data['language'].lower() if data else "en"
            current_name = available_langs.get(current_code, "English 🇺🇸")

            embed = discord.Embed(
                title=responses["title"], 
                color=discord.Color.blue()
            )
            
            description = f"{responses['current_language'].format(lang=current_name)}\n\n"
            description += responses["description"]
            for code, name in available_langs.items():
                description += f"• `{code}` - {name}\n"
            
            embed.description = description
            embed.set_footer(text=responses["footer"].format(prefix=ctx.prefix))
            return await ctx.send(embed=embed)

        lang_code = new_lang.lower()
        lang_to_save = lang_code.upper()
        
        # Salva no banco de dados mantendo o prefixo existente se houver
        await bot.db.execute("""
            INSERT INTO botsettings (guild_id, language) VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE language = %s
        """, (ctx.guild.id, lang_to_save, lang_to_save))

        msg = responses["success_ptbr"] if lang_code == "ptbr" else responses["success_en"]
        await ctx.send(f"✅ {msg}")

    @language.error
    async def language_error(ctx, error):
        responses = await languageservice(bot, ctx, "admin", "language.json")
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(responses["no_permission"], delete_after=5)