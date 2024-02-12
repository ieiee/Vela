import nextcord
from nextcord.ext import commands
from nextcord import FFmpegPCMAudio
from nextcord import FFmpegOpusAudio
from youtubesearchpython import VideosSearch
from nextcord import SlashOption
from nextcord import Interaction
from nextcord.abc import GuildChannel
import yt_dlp as YoutubeDL
from gtts import gTTS
import os
import pyshorteners
import aiohttp

class getf(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    async def get1(ctx, url):
        if url.startswith('https://'):
            ydl_opts = {'format': 'bestaudio/audio', 'postprocessors': [{'key':'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': ''}]}
            with YoutubeDL.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download = False)
            title1 = info['title']
            thumbnails = info.get('thumbnails')
            urlimage = thumbnails[-1].get('url')
            duration = info.get('duration')
            
            for i in info['formats']:
                if i.get('vcodec') != 'none' and i.get('acodec') != 'none':
                    a = i['url']
            dembed = nextcord.Embed(title = 'Click Here', url=a, description= 'Download Now!')
            dembed.add_field(name = title1, value=' ')
            dembed.set_image(url = urlimage)
            await ctx.channel.send(embed = dembed)
            

        else:
            search = VideosSearch(url, limit = 1)
            result = {'source' : search.result()["result"][0]['link'], 'title' : search.result()["result"][0]["title"]}
        
            ydl_opts = {'format': 'bestaudio/audio', 'postprocessors': [{'key':'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': ''}]}
            with YoutubeDL.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(result['source'], download = False)
            title1 = info['title']
            thumbnails = info.get('thumbnails')
            urlimage = thumbnails[-1].get('url')
            duration = info.get('duration')
            for i in info['formats']:
                if i.get('vcodec') != 'none' and i.get('acodec') != 'none':
                    a = i['url']
            dembed = nextcord.Embed(title = 'Click Here', url=a, description= 'Download Now!')
            dembed.add_field(name = title1, value=' ')
            dembed.set_image(url = urlimage)
            await ctx.channel.send(embed = dembed)
        
async def setup(bot: commands.Bot):
    bot.add_cog(getf(bot))