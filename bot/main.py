import discord
from discord.ext import commands
from messageTriggers import message_triggers
from variables import botToken
from mentionTriggers import mention_triggers

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents, case_insensitive=True)

message_triggers(bot)


bot.run(botToken)