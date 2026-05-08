from commands.songs.songsdownload import setup_songs_commands
from commands.songs.vcplay import setup_vc_commands
from commands.songs.skip import setup_skip_command
from commands.songs.queue import setup_queue_command
from commands.songs.stop import setup_stop_command
from commands.songs.nowplaying import setup_nowplaying_command
from commands.user.useravatar import useravatar
from commands.user.userinfo import userinfo
from commands.misc.ping import ping
from commands.misc.help import help
from commands.server.servericon import server_icon
from commands.server.serverinfo import server_info
from commands.misc.coinflip import coin_flip




def setup_commands(bot):

    #songs related commands
    setup_vc_commands(bot)
    setup_songs_commands(bot)
    setup_skip_command(bot)
    setup_stop_command(bot)
    setup_queue_command(bot)
    setup_nowplaying_command(bot)

    #user commands
    useravatar(bot)
    userinfo(bot)

    #misc
    ping(bot)
    help(bot)
    coin_flip(bot)


    #server
    server_icon(bot)
    server_info(bot)