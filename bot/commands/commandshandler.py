from commands.songs.songsdownload import setup_songs_commands
from commands.songs.vcplay import setup_vc_commands
from commands.songs.skip import setup_skip_command
from commands.songs.queue import setup_queue_command
from commands.songs.stop import setup_stop_command
from commands.songs.nowplaying import setup_nowplaying_command

def setup_commands(bot):
    setup_vc_commands(bot)
    setup_songs_commands(bot)
    setup_skip_command(bot)
    setup_stop_command(bot)
    setup_queue_command(bot)
    setup_nowplaying_command(bot)