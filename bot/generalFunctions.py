import discord, random, yt_dlp, asyncio, os, aiohttp
def respostas():
    dado = ["sim", "não", "talvez"]
    valor = random.randint(0, (len(dado)-1))
    easter_egg = random.randint(0, 100)
    if easter_egg == 100:
        return "smt"
    else:
        return dado[valor]
    
def convert_mp3_ytdlp(ydl_opts):
    ydl_opts.update({
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    })

async def ytdlp(videourl, ydl_opts):
    folder = "songs"
    os.makedirs(folder, exist_ok=True)

    ydl_opts['outtmpl'] = f'{folder}/%(title)s.%(ext)s'

    loop = asyncio.get_event_loop()
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = await loop.run_in_executor(None, lambda: ydl.extract_info(videourl, download=True))
        return ydl.prepare_filename(info)

async def upload_to_catbox(file_path):
    url = "https://catbox.moe/user/api.php"
    if not os.path.exists(file_path):
        return None

    try:
        async with aiohttp.ClientSession() as session:
            with open(file_path, 'rb') as f:
                data = aiohttp.FormData()
                data.add_field('reqtype', 'fileupload')
                data.add_field('fileToUpload', f, filename=os.path.basename(file_path))
                
                async with session.post(url, data=data) as response:
                    if response.status == 200:
                        return await response.text()
    except Exception as e:
        print(f"Erro no upload para o Catbox: {e}")
    return None
