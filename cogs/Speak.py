import nextcord
from nextcord.ext import commands
from nextcord import FFmpegAudio
from nextcord import FFmpegOpusAudio
from nextcord import FFmpegPCMAudio
from gtts import gTTS
import io
import aiosqlite

class Speak(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = {}
        self.queue2 = {}
        
    @commands.Cog.listener()
    async def on_message(self, ctx):
        async with aiosqlite.connect('databases/main.db') as db:
            async with db.cursor() as cursor:
                await cursor.execute(f'''SELECT textvoice FROM guilds WHERE guild_id == {ctx.guild.id}''')
                data = await cursor.fetchone()
            await db.commit()

            
            if str(data[0]) == "None":
                
                try:
                    
                    if ctx.author == self.bot.user:
                        return
                    
                    try:
                        
                        if ctx.guild.voice_client.is_playing():
                            return
                        
                    except:
                        
                        await ctx.channel.send('bot is currently in use')

                    try:
                        vc = await ctx.author.voice.channel.connect()
                    except:
                        vc= ctx.guild.voice_client
                        
                    sound = gTTS(text = ctx.content, lang = 'hi', slow=False)
                    sound.save('AI.mp3')
                    source = await FFmpegOpusAudio.from_probe('AI.mp3', method='fallback')
                    vc.play(source)
                    
                    return
                    
                except:
                    return
            
            
            elif int(str(data[0])) != ctx.channel.id:
                return
            
            elif int(str(data[0])) == ctx.channel.id:
        
                try:
                    
                    if ctx.author == self.bot.user:
                        return
                    
                    try:
                        
                        if ctx.guild.voice_client.is_playing():
                            return
                        
                    except:
                        
                        await ctx.channel.send('bot is currently in use')

                    try:
                        vc = await ctx.author.voice.channel.connect()
                    except:
                        vc= ctx.guild.voice_client
                        
                    sound = gTTS(text = ctx.content, lang = 'hi', slow=False)
                    sound.save('AI.mp3')
                    source = await FFmpegOpusAudio.from_probe('AI.mp3', method='fallback')
                    vc.play(source)
                    
                except:
                    pass
        
async def setup(bot: commands.Bot):
    bot.add_cog(Speak(bot))