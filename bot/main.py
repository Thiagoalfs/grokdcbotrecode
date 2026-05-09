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
    # Prefixo padrão caso seja DM ou o banco ainda não esteja pronto
    if not message.guild or not hasattr(bot, 'db') or bot.db.pool is None:
        return "."
    
    data = await bot.db.fetch_one("SELECT serverprefix FROM botsettings WHERE guild_id = %s", (message.guild.id,))
    return data['serverprefix'] if data else "."

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
intents.voice_states = True

bot = commands.Bot(command_prefix=get_prefix, intents=intents, case_insensitive=True, help_command=None)

async def setup_hook():
    # Inicializa o banco de dados e anexa ao objeto bot
    bot.db = Database()
    await bot.db.setup()
    await bot.db.create_tables()

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