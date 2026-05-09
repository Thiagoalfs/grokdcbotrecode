import discord, os, json

async def languageservice(bot, ctx, commandpath, jsonfile):
    # Define a linguagem padrão
    lang_code = "en"

    # Busca a linguagem salva no banco de dados para este servidor
    if ctx.guild:
        data = await bot.db.fetch_one("SELECT language FROM botsettings WHERE guild_id = %s", (ctx.guild.id,))
        if data and data.get('language'):
            lang_code = data['language'].lower()
    
    json_path = os.path.join(os.path.dirname(__file__), "..", "languages", lang_code, commandpath, jsonfile)
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            responses = json.load(f)
            return responses
    except Exception as e:
        print(f"❌ Erro ao carregar traduções ({lang_code}/{jsonfile}): {e}")
        return None