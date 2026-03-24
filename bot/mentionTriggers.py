async def mention_triggers(bot, message):
    if bot.user in message.mentions:
        if message.content == "<@1312115157589037066>":
            await message.channel.send("oi fi po fala")
            return