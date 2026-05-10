import discord
from discord.ext import commands
from messageTriggers import message_triggers
from dotenv import load_dotenv
from commands.commandshandler import setup_commands
from database import Database
import os
import shutil
load_dotenv()

async def get_prefix(bot, message):
    if not message.guild:
        return "."
    # Retorna do cache; se não houver, usa o padrão "."
    return bot.prefix_cache.get(message.guild.id, ".")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
intents.voice_states = True

bot = commands.Bot(command_prefix=get_prefix, intents=intents, case_insensitive=True, help_command=None)
bot.prefix_cache = {} # Inicializa o cache de prefixos
bot.lang_cache = {}   # Inicializa o cache de idiomas

async def setup_hook():
    # Inicializa o banco de dados e anexa ao objeto bot
    bot.db = Database()
    await bot.db.setup()
    await bot.db.create_tables()
    
    # Popula os caches ao iniciar o bot
    try:
        rows = await bot.db.fetch("SELECT guild_id, serverprefix, language FROM botsettings")
        for row in rows:
            bot.prefix_cache[row['guild_id']] = row['serverprefix']
            bot.lang_cache[row['guild_id']] = row['language']
        print(f"✅ Cache carregado: {len(bot.prefix_cache)} servidores configurados.")
    except Exception as e:
        print(f"❌ Erro ao carregar caches no startup: {e}")

bot.setup_hook = setup_hook

@bot.event
async def on_ready():
    print(f"Loguei como {bot.user}")
    downloads_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "downloadedsongs")
    try:
        if os.path.exists(downloads_folder):
            shutil.rmtree(downloads_folder)
        os.makedirs(downloads_folder)
        print(f"Pasta '{downloads_folder}' reiniciada com sucesso ao iniciar.")
    except Exception as e:
        print(f"Erro ao limpar a pasta de downloads no on_ready: {e}")

setup_commands(bot)
message_triggers(bot)
bot.run(os.getenv("TOKEN"))