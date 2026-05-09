import re, random, os
from mentionTriggers import mention_triggers

try:
    from hiddentriggers.hiddenMessageTriggers import hidden_message_triggers
except (ImportError, ModuleNotFoundError):
    hidden_message_triggers = None

def message_triggers(bot):
    @bot.event
    async def on_ready():
        print(f"Loguei como {bot.user}")

    @bot.event
    async def on_message(message):
        if message.author.bot:
            return True
        
        await bot.process_commands(message)
            
        await mention_triggers(bot, message)

        if bot.user not in message.mentions:

            if hidden_message_triggers and await hidden_message_triggers(bot, message):
                return True
                        