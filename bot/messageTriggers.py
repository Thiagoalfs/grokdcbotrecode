import re, random
from variables import gif_atual
from mentionTriggers import mention_triggers

def message_triggers(bot):
    @bot.event
    async def on_ready():
        print(f"Loguei como {bot.user}")

    @bot.event
    async def on_message(message):
        if message.author.bot:
            return
        
        await bot.process_commands(message)
            
        await mention_triggers(bot, message)

        if bot.user not in message.mentions:
            
            if re.search(r'(?<!\w)(:3)(?!\w)', message.content.lower()):
                await message.channel.send("https://cdn.discordapp.com/attachments/435174265516458024/1357417638338236567/pellegrini7_-_1906183618713493636.gif?ex=69b1b0b0&is=69b05f30&hm=0daf26fd8cbbf09308a9dab5bf0f3350b67fe5b2e7b808c26ffb0aa42610194a&", reference=message)
            
            elif re.search(r'(?<!\w)(goberto)(?!\w)', message.content.lower()):
                await message.channel.send("até eu não gosto desse cara", reference=message)
                return
                        
            elif re.search(r'(?<!\w)(ué|ue)(?!\w)', message.content.lower()):
                await message.channel.send("ué o que?", reference=message)
                return
                       
            elif re.search(r'(?<!\w)(ijo)(?!\w)', message.content.lower()):
                await message.channel.send("tu se acha o engraçadao ne pnc", reference=message)
                return
                        
            elif re.search(r'(?<!\w)(israel)(?!\w)', message.content.lower()):
                global gif_atual
                gifs_israelitas = ["https://klipy.com/gifs/israel-israel-superhero",
                               "https://klipy.com/gifs/israel-god-bless-israel",
                               "https://klipy.com/gifs/israel-israel-jumpscare-1",
                               "https://klipy.com/gifs/israel-israel-flag-8",
                               "https://tenor.com/view/israel-another-20-trillion-money-isreal-billion-isreal-million-isreal-gif-14749225861519006261",
                               "https://images-ext-1.discordapp.net/external/ATm2xnQ6R1S10tsL9I6lwmOa8_j-flcRj8r21k5w35A/https/media.tenor.com/P4RUJrTp7dcAAAPo/flag-israel.mp4",
                               "https://klipy.com/gifs/sylveon-pokemon-31"]
                escolha_gif_israel = random.randint(0, (len(gifs_israelitas) - 1))
                if gif_atual == escolha_gif_israel:
                    escolha_gif_israel
                else:
                    gif_atual = escolha_gif_israel

                await message.channel.send(gifs_israelitas[gif_atual], reference=message)
                return

        
    