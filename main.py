import nextcord
from nextcord.ext import commands
from nextcord.ext import application_checks
from nextcord import FFmpegPCMAudio
from nextcord import FFmpegOpusAudio
from youtubesearchpython import VideosSearch
from nextcord import SlashOption
from nextcord import Interaction
from nextcord.abc import GuildChannel
import yt_dlp as YoutubeDL
from gtts import gTTS
import os
import aiohttp
from cogs.getf import getf
import io
import aiosqlite

intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix=",", intents=intents)
testcommands = ['YOUR-TEST-SERVER-ID-HERE']

YoutubeDL.utils.bug_reports_message = lambda: ''

playing = {}
queue = {}
queue2 = {}
loop = {}

async def youtube(url):
  ydl_opts = {'format': 'bestaudio/audio', 'postprocessors': [{'key':'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': ''}]}
  with YoutubeDL.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download = False)
  title1 = info['title']
  thumbnails = info.get('thumbnails')
  urlimage = thumbnails[-1].get('url')
  duration = info.get('duration')
  return [title1, urlimage, duration]

async def play_next(ctx):
  if loop[ctx.guild.id] == False:
    if not queue[ctx.guild.id]:
      playing[ctx.guild.id] = False
      return
    
  if loop[ctx.guild.id] == True:
    if not queue2[ctx.guild.id]:
      playing[ctx.guild.id] = False
      return
    
  playing[ctx.guild.id] = True
  
  try:
    vc = await ctx.user.voice.channel.connect()
  except:
    vc = ctx.guild.voice_client
  
  ydl_opts = {'format': 'bestaudio/audio', 'postprocessors': [{'key':'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': ''}]}
  
  if loop[ctx.guild.id] == False:
       url = queue[ctx.guild.id].pop(0)
       
  else:
    url = queue2[ctx.guild.id].pop(0)
    queue2[ctx.guild.id].append(url)
  
  with YoutubeDL.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download = False)
  title1 = info['title']
  thumbnails = info.get('thumbnails')
  urlimage = thumbnails[-1].get('url')
  duration = info.get('duration')
  
  sembed = nextcord.Embed(title = 'Currently Playing',description=f'{title1}',  color = nextcord.Color.yellow())
  sembed.set_author(name = ctx.user.name, icon_url = ctx.user.avatar)
  sembed.set_thumbnail(url = ctx.guild.icon)
  sembed.add_field(name = 'Duration - ', value = f'{round(duration/60, 2)} minutes' if duration<= 3600 else f"{round(duration/3600)}.{round(duration%3600/60, 2)} hours")
  sembed.set_image(url = urlimage)
  sembed.set_footer(text = 'Enjoy the music!')
  await ctx.channel.send(embed = sembed)
  
  for i in info['formats']:
      if i.get('vcodec') != 'none' and i.get('acodec') != 'none':
        a = i['url']    
  vc.play(nextcord.FFmpegPCMAudio(a),after= lambda e: bot.loop.create_task(play_next(ctx)))


async def play1(ctx, url2):
  
  if ctx.guild.id not in loop:
      loop[ctx.guild.id] = False
      loop[ctx.guild.id] = False
  
  if ctx.guild.id not in queue:
    queue[ctx.guild.id] = []
    queue2[ctx.guild.id] = []
    
  if ctx.guild.id not in playing:
      playing[ctx.guild.id] = False
      
  if url2.startswith('https://'):
    if ctx.user.voice == None:
      await ctx.response.send_message('First you need to be in a voice channel!')
      return
    
    if queue[ctx.guild.id] != {}:
        ydl_opts = {'format': 'bestaudio/audio', 'postprocessors': [{'key':'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': ''}]}
        with YoutubeDL.YoutubeDL(ydl_opts) as ydl:
          info = ydl.extract_info(url2, download = False)
        title1 = info['title']
        thumbnails = info.get('thumbnails')
        urlimage = thumbnails[-1].get('url')
        duration = info.get('duration')
        
        q = nextcord.Embed(title = 'Added to Queue', description = title1, color= nextcord.Color.red())
        q.set_author(name = ctx.user.name, icon_url = ctx.user.avatar)
        q.set_thumbnail(url = urlimage)
        q.add_field(name = 'Duration - ',value = f'{round(duration/60, 2)} minutes' if duration<= 3600 else f"{round(duration/3600)}.{round(duration%3600/60, 2)} hours")
        await ctx.channel.send(embed = q)
        
    queue[ctx.guild.id].append(url2)
    queue2[ctx.guild.id].append(url2)
    
    if not playing[ctx.guild.id]:
        await play_next(ctx)
        
  else:
    search = VideosSearch(url2, limit = 1)
    result = {'source' : search.result()["result"][0]['link'], 'title' : search.result()["result"][0]["title"]}
    
    source = result["source"]
    

    #and the remaining code is save as we used in the link source the only difference is the source

    if  ctx.user.voice == None:
      await ctx.channel.send('You are not present in any voice channel')
      return
    if queue[ctx.guild.id] != {}:
      ydl_opts = {'format': 'bestaudio/audio', 'postprocessors': [{'key':'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': ''}]}
      with YoutubeDL.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(source, download = False)
      title1 = info['title']
      thumbnails = info.get('thumbnails')
      urlimage = thumbnails[-1].get('url')
      duration = info.get('duration')
      
      q = nextcord.Embed(title = 'Added to Queue', description = title1, color= nextcord.Color.red())
      q.set_author(name = ctx.user.name, icon_url = ctx.user.avatar)
      q.set_thumbnail(url = urlimage)
      q.add_field(name = 'Duration - ',value = f'{round(duration/60, 2)} minutes' if duration<= 3600 else f"{round(duration/3600)}.{round(duration%3600/60, 2)} hours")
      await ctx.channel.send(embed = q)
      
      queue[ctx.guild.id].append(source)
      queue2[ctx.guild.id].append(source)
    
    if not playing[ctx.guild.id]:
      await play_next(ctx)
      
async def queue1(ctx):
  
    if ctx.guild.id not in loop:
      loop[ctx.guild.id] = False
      loop[ctx.guild.id] = False
  
    if ctx.guild.id not in queue:
        queue[ctx.guild.id] = []
        queue2[ctx.guild.id] = []
  
    if  ctx.user.voice == None:
      await ctx.channel.send('You are not present in any voice channel')
      return
        
    ydl_opts = {'format': 'bestaudio/audio', 'postprocessors': [{'key':'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': ''}]}
    if loop[ctx.guild.id] == False:
      aembed = nextcord.Embed(title = 'Queue', description = '', color = nextcord.Color.gold())
      aembed.set_thumbnail(url = ctx.guild.icon) 
      for i in queue[ctx.guild.id]:
        with YoutubeDL.YoutubeDL(ydl_opts) as ydl:
          info = ydl.extract_info(i, download = False)
        title1 = info['title']
        aembed.add_field(name = f'{queue[ctx.guild.id].index(i)}. - ', value = f'{title1[:25]}', inline = False)
      await ctx.channel.send(embed = aembed)
      
    else:
      aembed = nextcord.Embed(title = 'Queue', description = '', color = nextcord.Color.gold())
      aembed.set_thumbnail(url = ctx.guild.icon) 
      for i in queue2[ctx.guild.id]:
        with YoutubeDL.YoutubeDL(ydl_opts) as ydl:
          info = ydl.extract_info(i, download = False)
        title1 = info['title']
        aembed.add_field(name = f'{queue2[ctx.guild.id].index(i)}. - ', value = f'{title1[:25]}', inline = False)
      await ctx.channel.send(embed = aembed)
      
async def loop1(ctx):
  
    if ctx.guild.id not in loop:
      loop[ctx.guild.id] = False
      loop[ctx.guild.id] = False
    
    if  ctx.user.voice == None:
      await ctx.channel.send('You are not present in any voice channel')
      return
    
    if loop[ctx.guild.id] == False:
      loop[ctx.guild.id] = True
      await ctx.channel.send('Now Queue is in Loop')
      
    else:
      loop[ctx.guild.id] = False
      await ctx.channel.send('Now Queue is out of Loop')
      
async def skip1(ctx):
  
    if  ctx.user.voice == None:
      await ctx.channel.send('You are not present in any voice channel')
      return
    
    if playing[ctx.guild.id] == True:
      ctx.guild.voice_client.stop()
      
    else:
      await ctx.channel.send('No song is currently playing')
      
      
async def remove1(ctx, position):
  
  if ctx.guild.id not in loop:
    loop[ctx.guild.id] = False
    
  if ctx.guild.id not in queue:
    queue[ctx.guild.id] = []
    queue2[ctx.guild.id] = []
    
  if ctx.user.voice != None:
    if loop[ctx.guild.id] == True:
      if queue2[ctx.guild.id] == []:
        await ctx.channel.send('No song is present in the queue')
        return
      else:
        try:
          url = await youtube(queue2[ctx.guild.id][position])
          queue2[ctx.guild.id].pop(position)
          await ctx.channel.send(f'{url[0]} is removed from the queue!')
        except:
          await ctx.channel.send(f'{ctx.user.mention}, Invalid Position.')
    
    else:
      if queue[ctx.guild.id] == []:
        await ctx.channel.send('No song is present in the queue')
        return
      else:
        try:
          url = await youtube(queue[ctx.guild.id][position])
          queue[ctx.guild.id].pop(position)
          await ctx.channel.send(f'{url[0]} is removed from the queue!')
        except:
          await ctx.channel.send(f'{ctx.user.mention}, Invalid Position.')
  else:
    await ctx.channel.send(f'{ctx.user.mention}You should presend in a voice channel')
    return
        
        
async def clear1(ctx):
    await ctx.channel.purge()
    await ctx.channel.send('Successfully deleted messages')
    
    
#=========================================================================================
#====================================  play playlist function ============================
#=========================================================================================
    
    
async def playlistplay1(ctx, name):
  ast = ""
  a = []
  if ctx.user.voice == None:
      await ctx.channel.send('You are not present in any voice channel')
      return
    
  try: 
    async with aiosqlite.connect('databases/main.db') as db:
      async with db.cursor() as cursor:
        await cursor.execute(f'''SELECT playlist1, playlist2, playlist3, playlist4, playlist5 FROM playlist WHERE member_id == {ctx.user.id}''')
        data = await cursor.fetchone()
        await db.commit()
        if name in data:
          await ctx.channel.send('Added playlist to queue, Enjoy The Music!')
          if name == str(data[0]):
            await cursor.execute(f'''SELECT pld1 FROM playlist WHERE member_id == {ctx.user.id}''')
            data2 = await cursor.fetchone()
            await db.commit()
            ast = str(data2[0])
            a = list(map(str, ast.split(',')))
            a.remove('None')
            
            if ctx.guild.id not in queue:
              queue[ctx.guild.id] = []
              queue2[ctx.guild.id] = []
              
            if ctx.guild.id not in playing:
              playing[ctx.guild.id] = False
              
            for i in a:
              queue[ctx.guild.id].append(i)
              queue2[ctx.guild.id].append(i)
            
            if ctx.guild.id not in loop:
              loop[ctx.guild.id] = False
            
            if not playing[ctx.guild.id]:
              await play_next(ctx)
            
          elif name == str(data[1]):
            await cursor.execute(f'''SELECT pld2 FROM playlist WHERE member_id == {ctx.user.id}''')
            data2 = await cursor.fetchone()
            await db.commit()
            ast = str(data2[0])
            a = list(map(str, ast.split(',')))
            a.remove('None')
            
            if ctx.guild.id not in queue:
              queue[ctx.guild.id] = []
              queue2[ctx.guild.id] = []
                        
            for i in a:
              queue[ctx.guild.id].append(i)
              queue2[ctx.guild.id].append(i)
            
            if ctx.guild.id not in loop:
              loop[ctx.guild.id] = False
              
            if ctx.guild.id not in playing:
              playing[ctx.guild.id] = False
              
            if not playing[ctx.guild.id]:
              await play_next(ctx)
              
            
          elif name == str(data[2]):
            await cursor.execute(f'''SELECT pld3 FROM playlist WHERE member_id == {ctx.user.id}''')
            data2 = await cursor.fetchone()
            await db.commit()
            ast = str(data2[0])
            a = list(map(str, ast.split(',')))
            a.remove('None')
            
            if ctx.guild.id not in queue:
              queue[ctx.guild.id] = []
              queue2[ctx.guild.id] = []
              
            for i in a:
              queue[ctx.guild.id].append(i)
              queue2[ctx.guild.id].append(i)
            
            if ctx.guild.id not in loop:
              loop[ctx.guild.id] = False
            
            if ctx.guild.id not in playing:
              playing[ctx.guild.id] = False
              
            if not playing[ctx.guild.id]:
              await play_next(ctx)
            
          elif name == str(data[3]):
            await cursor.execute(f'''SELECT pld4 FROM playlist WHERE member_id == {ctx.user.id}''')
            data2 = await cursor.fetchone()
            await db.commit()
            ast = str(data2[0])
            a = list(map(str, ast.split(',')))
            a.remove('None')
            
            if ctx.guild.id not in queue:
              queue[ctx.guild.id] = []
              queue2[ctx.guild.id] = []
              
            for i in a:
              queue[ctx.guild.id].append(i)
              queue2[ctx.guild.id].append(i)
            
            if ctx.guild.id not in loop:
              loop[ctx.guild.id] = False
            
            if ctx.guild.id not in playing:
              playing[ctx.guild.id] = False
              
            if not playing[ctx.guild.id]:
              await play_next(ctx)
          
          elif name == str(data[4]):
            await cursor.execute(f'''SELECT pld5 FROM playlist WHERE member_id == {ctx.user.id}''')
            data2 = await cursor.fetchone()
            await db.commit()
            ast = str(data2[0])
            a = list(map(str, ast.split(',')))
            a.remove('None')
            
            if ctx.guild.id not in queue:
              queue[ctx.guild.id] = []
              queue2[ctx.guild.id] = []
              
            for i in a:
              queue[ctx.guild.id].append(i)
              queue2[ctx.guild.id].append(i)
            
            if ctx.guild.id not in loop:
              loop[ctx.guild.id] = False
            
            if ctx.guild.id not in playing:
              playing[ctx.guild.id] = False
              
            if not playing[ctx.guild.id]:
              await play_next(ctx)      
        else:
          await ctx.channel.send(f'{ctx.user.mention} please enter a valid playlist name.')
  
  except:
    await ctx.channel.send(f'{ctx.user.mention} wait for a while, then try again :)!') 
    

    
#============================== slash-commands and events ==========================================
          
@bot.event
async def on_ready():
  tgl = []
  gli = []
  m = []
  mid = []
  for i in bot.guilds:
    tgl.append(i.id)
  print('I am ready to go')
  bot.load_extension('cogs.Speak')
  bot.load_extension('cogs.getf')
  bot.load_extension('cogs.autodelete')
  async with aiosqlite.connect('databases/main.db') as db:
    async with db.cursor() as cursor:
          await cursor.execute('SELECT * FROM guilds')
          data = await cursor.fetchall()
          await db.commit()
          for i in data:
            gli.append(i[0])
          
          for i in tgl:
            if i not in gli:
              await cursor.execute(f'''INSERT INTO guilds(guild_id , guild_name) VALUES (?, ?)''', (i, bot.get_guild(i).name,))
              await cursor.execute(f'''CREATE TABLE IF NOT EXISTS {bot.get_guild(i)} (member_id INTEGER, member_name TEXT)''')
              await db.commit()
              for p in range(0, len(bot.get_guild(i).members)):
                m.append(bot.get_guild(i).members[p].name)
                mid.append(bot.get_guild(i).members[p].id)
              for k, j in zip(mid, m):
                await cursor.execute(f'''INSERT INTO {bot.get_guild(i)}(member_id, member_name) VALUES (?, ?)''', (k, j,))
              await db.commit()
          
          for i in gli:
            if i not in tgl:
              await cursor.execute(f'''SELECT guild_name FROM guilds WHERE guild_id == {i}''')
              data = await cursor.fetchone()
              await cursor.execute(f'''DELETE FROM guilds WHERE guild_id == {i}''')
              await cursor.execute(f'''DROP TABLE IF EXISTS {str(data[0])}''')
              await db.commit()

      
@bot.event
async def on_guild_join(ctx):
  m = []
  mid = []
  async with aiosqlite.connect('databases/main.db') as db:
    async with db.cursor() as cursor:
      for member in ctx.members:
        m.append(member.name)
        mid.append(member.id)
      await cursor.execute(f'''CREATE TABLE IF NOT EXISTS {ctx.name} (member_id INTEGER, member_name TEXT)''')
      await db.commit()
      for i,j in zip(mid, m):
        await cursor.execute(f'''INSERT INTO {ctx.name}(member_id, member_name) VALUES (?, ?)''', (i, j,))
      await db.commit()
      await cursor.execute('CREATE TABLE IF NOT EXISTS guilds (guild_id INTEGER, guild_name TEXT)')
      await cursor.execute('INSERT INTO guilds(guild_id, guild_name) VALUES (?, ?)', (ctx.id, ctx.name,))
    await db.commit()
    
@bot.event
async def on_guild_remove(ctx):
  async with aiosqlite.connect('databases/main.db') as db:
    async with db.cursor() as cursor:
      await cursor.execute('DELETE FROM guilds WHERE guild_id = ?', (ctx.id,))
      await cursor.execute(f'''DROP TABLE IF EXISTS {ctx.name}''')
    await db.commit()
    
@bot.event
async def on_member_join(member):
  if member.name == 'PyBot':
    return
  async with aiosqlite.connect('databases/main.db') as db:
    async with db.cursor() as cursor:
      await cursor.execute(f'''INSERT INTO {bot.get_guild(member.guild.id)}(member_id, member_name) VALUES (?, ?)''', (member.id, member.name,))
    await db.commit()
    
@bot.event
async def on_member_remove(member):
  if member.name == 'PyBot':
    return
  async with aiosqlite.connect('databases/main.db') as db:
    async with db.cursor() as cursor:
      await cursor.execute(f'''DELETE FROM {bot.get_guild(member.guild.id)} WHERE member_id == {member.id}''')
    await db.commit()
    
    
#=========================================================================================
#=============================  remove a song from the playlist ==========================
#=========================================================================================
    
 
@bot.slash_command(name = 'playlistremove', description='remove a song from the playlist',)
async def playlistremove(ctx: Interaction, playlist_name: str, serial_number: int, confirm_yes_or_no: str):
  a = []
  b = []
  c = []
  nlist = []
  lili = []
  if confirm_yes_or_no == 'yes':
    async with aiosqlite.connect('databases/main.db') as db:
      async with db.cursor() as cursor:
        await cursor.execute(f'''SELECT playlist1, playlist2, playlist3, playlist4, playlist5 FROM playlist WHERE member_id == {ctx.user.id}''')
        data = await cursor.fetchone()
        await db.commit()
        await cursor.execute(f'''SELECT pld1, pld2, pld3, pld4, pld5 FROM playlist WHERE member_id == {ctx.user.id} ''')
        data2 = await cursor.fetchone()
        await db.commit()
        await cursor.execute(f'''SELECT pldn1, pldn2, pldn3, pldn4, pldn5 FROM playlist WHERE member_id == {ctx.user.id} ''')
        data3 = await cursor.fetchone()
        await db.commit()
        
        for i in data:
          a.append(i)
        for j in data2:
          b.append(j)
        for k in data3:
          c.append(k)
        
        if playlist_name in a:
          
              if playlist_name == a[0]:
                pstr = list(map(str, str(data2[0]).split(',')))
                nstr = list(map(str, str(data3[0]).split(',')))
                dp = pstr.pop(serial_number+1)
                dn = nstr.pop(serial_number+1)
                await ctx.response.send_message(f'successfully removed {dn} from playlist {playlist_name}', ephemeral=True)
                fl = pstr + lili
                nl = nstr + nlist
                fs = ','.join(map(str, fl))
                ns = ','.join(map(str, nl))
                await cursor.execute(f'''UPDATE playlist SET pld1 = "{fs}" WHERE member_id == {ctx.user.id}''')
                await cursor.execute(f'''UPDATE playlist SET pldn1 = "{ns}" WHERE member_id == {ctx.user.id}''')
                await db.commit()
                return
                
              elif playlist_name == a[1]:
                pstr = list(map(str, str(data2[1]).split(',')))
                nstr = list(map(str, str(data3[1]).split(',')))
                dp = pstr.pop(serial_number+1)
                dn = nstr.pop(serial_number+1)
                await ctx.response.send_message(f'successfully removed {dn} from playlist {playlist_name}', ephemeral=True)
                fl = pstr + lili
                nl = nstr + nlist
                fs = ','.join(map(str, fl))
                ns = ','.join(map(str, nl))
                await cursor.execute(f'''UPDATE playlist SET pld2 = "{fs}" WHERE member_id == {ctx.user.id}''')
                await cursor.execute(f'''UPDATE playlist SET pldn2 = "{ns}" WHERE member_id == {ctx.user.id}''')
                await db.commit()
                return
                
              elif playlist_name == a[2]:
                pstr = list(map(str, str(data2[2]).split(',')))
                nstr = list(map(str, str(data3[2]).split(',')))
                dp = pstr.pop(serial_number+1)
                dn = nstr.pop(serial_number+1)
                await ctx.response.send_message(f'successfully removed {dn} from playlist {playlist_name}', ephemeral=True)
                fl = pstr + lili
                nl = nstr + nlist
                fs = ','.join(map(str, fl))
                ns = ','.join(map(str, nl))
                await cursor.execute(f'''UPDATE playlist SET pld3 = "{fs}" WHERE member_id == {ctx.user.id}''')
                await cursor.execute(f'''UPDATE playlist SET pldn3 = "{ns}" WHERE member_id == {ctx.user.id}''')
                await db.commit()
                return
                
              elif playlist_name == a[3]:
                pstr = list(map(str, str(data2[3]).split(',')))
                nstr = list(map(str, str(data3[3]).split(',')))
                dp = pstr.pop(serial_number+1)
                dn = nstr.pop(serial_number+1)
                await ctx.response.send_message(f'successfully removed {dn} from playlist {playlist_name}', ephemeral=True)
                fl = pstr + lili
                nl = nstr + nlist
                fs = ','.join(map(str, fl))
                ns = ','.join(map(str, nl))
                await cursor.execute(f'''UPDATE playlist SET pld4 = "{fs}" WHERE member_id == {ctx.user.id}''')
                await cursor.execute(f'''UPDATE playlist SET pldn4 = "{ns}" WHERE member_id == {ctx.user.id}''')
                await db.commit()
                return
                
              elif playlist_name == a[4]:
                pstr = list(map(str, str(data2[4]).split(',')))
                nstr = list(map(str, str(data3[4]).split(',')))
                dp = pstr.pop(serial_number+1)
                dn = nstr.pop(serial_number+1)
                await ctx.response.send_message(f'successfully removed {dn} from playlist {playlist_name}', ephemeral=True)
                fl = pstr + lili
                nl = nstr + nlist
                fs = ','.join(map(str, fl))
                ns = ','.join(map(str, nl))
                await cursor.execute(f'''UPDATE playlist SET pld5 = "{fs}" WHERE member_id == {ctx.user.id}''')
                await cursor.execute(f'''UPDATE playlist SET pldn5 = "{ns}" WHERE member_id == {ctx.user.id}''')
                await db.commit()
                return
                
              else:
                await ctx.response.send_message('Please try again! :)', ephemeral=True)
                
  elif confirm_yes_or_no == 'no':
    await ctx.response.send_message('Ok no problem, stay tuned :)', ephemeral= True)
   
  else: 
    await ctx.response.send_message('be carefull!, please be aware of misclicks.:)', ephemeral= True)
    
    
#=========================================================================================
#====================================  delete playlist ===================================
#=========================================================================================

    
@bot.slash_command(name = 'playlistdelete', description='delete any playlist you want')
async def playlistdelete(ctx: Interaction, name: str, confirm_yes_or_no: str):
  async with aiosqlite.connect('databases/main.db') as db:
    async with db.cursor() as cursor:
      await cursor.execute(f'SELECT playlist1, playlist2, playlist3, playlist4, playlist5 FROM playlist WHERE member_id == {ctx.user.id}')
      data = await cursor.fetchone()
      if confirm_yes_or_no == 'yes':
        if str(set(data)) == '{None}':
          await ctx.response.send_message("You don't have any playlist created, create one to do that :)", ephemeral=True)
          
        if name in data:
          await ctx.response.send_message(f"Successfully deleted playlist named {name}")
          if name == data[0]:
            await cursor.execute(f'''UPDATE playlist SET playlist1 = NULL WHERE member_id == {ctx.user.id}''')
            await cursor.execute(f'''UPDATE playlist SET pld1 = NULL WHERE member_id == {ctx.user.id}''')
            await cursor.execute(f'''UPDATE playlist SET pldn1 = NULL WHERE member_id == {ctx.user.id}''')
            await cursor.execute(f'''UPDATE playlist SET noplaylistcreated = noplaylistcreated-1 WHERE member_id == {ctx.user.id}''')
            await db.commit()          
          elif name == data[1]:
            await cursor.execute(f'''UPDATE playlist SET playlist2 = NULL WHERE member_id == {ctx.user.id}''')
            await cursor.execute(f'''UPDATE playlist SET pld2 = NULL WHERE member_id == {ctx.user.id}''')
            await cursor.execute(f'''UPDATE playlist SET pldn2 = NULL WHERE member_id == {ctx.user.id}''')
            await cursor.execute(f'''UPDATE playlist SET noplaylistcreated = noplaylistcreated-1 WHERE member_id == {ctx.user.id}''')
            await db.commit()
          elif name == data[2]:
            await cursor.execute(f'''UPDATE playlist SET playlist3 = NULL WHERE member_id == {ctx.user.id}''')
            await cursor.execute(f'''UPDATE playlist SET pld3 = NULL WHERE member_id == {ctx.user.id}''')
            await cursor.execute(f'''UPDATE playlist SET pldn3 = NULL WHERE member_id == {ctx.user.id}''')
            await cursor.execute(f'''UPDATE playlist SET noplaylistcreated = noplaylistcreated-1 WHERE member_id == {ctx.user.id}''')
            await db.commit()
          elif name == data[3]:
            await cursor.execute(f'''UPDATE playlist SET playlist4 = NULL WHERE member_id == {ctx.user.id}''')
            await cursor.execute(f'''UPDATE playlist SET pld4 = NULL WHERE member_id == {ctx.user.id}''')
            await cursor.execute(f'''UPDATE playlist SET pldn4 = NULL WHERE member_id == {ctx.user.id}''')
            await cursor.execute(f'''UPDATE playlist SET noplaylistcreated = noplaylistcreated-1 WHERE member_id == {ctx.user.id}''')
            await db.commit()
          elif name == data[4]:
            await cursor.execute(f'''UPDATE playlist SET playlist5 = NULL WHERE member_id == {ctx.user.id}''')
            await cursor.execute(f'''UPDATE playlist SET pld5 = NULL WHERE member_id == {ctx.user.id}''')
            await cursor.execute(f'''UPDATE playlist SET pldn5 = NULL WHERE member_id == {ctx.user.id}''')
            await cursor.execute(f'''UPDATE playlist SET noplaylistcreated = noplaylistcreated-1 WHERE member_id == {ctx.user.id}''')
            await db.commit()
          else:
            await ctx.channel.send(f'{ctx.user.mention} Please try that again :) ')
            
        else:
          await ctx.response.send_message("Please note the name you have entered is same as the playlist you want to delete", ephemeral=True)
      else:
        await ctx.response.send_message("Please enter your confirmation(yes/no)", ephemeral=True)
        
        
#=========================================================================================
#==================================== view playlist ======================================
#=========================================================================================
        
@bot.slash_command(name = 'playlistview', description = 'view your playlists')
async def playlistview(ctx: Interaction, name: str):
  a = []
  b = []
  c = []
  async with aiosqlite.connect('databases/main.db') as db:
    async with db.cursor() as cursor:
      await cursor.execute(f'''SELECT playlist1, playlist2, playlist3, playlist4, playlist5 FROM playlist WHERE member_id == {ctx.user.id}''')
      data = await cursor.fetchone()
      await db.commit()
      await cursor.execute(f'''SELECT pld1, pld2, pld3, pld4, pld5 FROM playlist WHERE member_id == {ctx.user.id} ''')
      data2 = await cursor.fetchone()
      await db.commit()
      await cursor.execute(f'''SELECT pldn1, pldn2, pldn3, pldn4, pldn5 FROM playlist WHERE member_id == {ctx.user.id} ''')
      data3 = await cursor.fetchone()
      await db.commit()
      
      for i in data:
        a.append(i)
      for j in data2:
        b.append(j)
      for k in data3:
        c.append(k)
      
      if name in a:
        await ctx.response.send_message(f'Loading {name} playlist...', ephemeral = True)
        
        pembed = nextcord.Embed(title = name)
        pembed.set_author(name=ctx.user.name, icon_url=ctx.user.avatar)
        
        if name == a[0]:
          pld = list(map(str, b[0].split(',')))
          pld.remove('None')
          pldn = list(map(str, c[0].split(',')))
          pldn.remove('None')
          for i,j in zip(pld, pldn):
            pembed.add_field(name= f'{pld.index(i)}. {j}', value= i, inline= True)
          await ctx.channel.send(embed = pembed)
          
        elif name == a[1]:
          pld = list(map(str, b[1].split(',')))
          pld.remove('None')
          pldn = list(map(str, c[1].split(',')))
          pldn.remove('None')
          for i,j in zip(pld, pldn):
            pembed.add_field(name= f'{pld.index(i)}. {j}', value= i, inline= True)
          await ctx.channel.send(embed = pembed)
        
        elif name == a[2]:
          pld = list(map(str, b[2].split(',')))
          pld.remove('None')
          pldn = list(map(str, c[2].split(',')))
          pldn.remove('None')
          for i,j in zip(pld, pldn):
            pembed.add_field(name= f'{pld.index(i)}. {j}', value= i, inline= True)
          await ctx.channel.send(embed = pembed)
          
        elif name == a[3]:
          pld = list(map(str, b[3].split(',')))
          pld.remove('None')
          pldn = list(map(str, c[3].split(',')))
          pldn.remove('None')
          for i,j in zip(pld, pldn):
            pembed.add_field(name= f'{pld.index(i)}. {j}', value= i, inline= True)
          await ctx.channel.send(embed = pembed)
          
        elif name == a[4]:
          pld = list(map(str, b[4].split(',')))
          pld.remove('None')
          pldn = list(map(str, c[4].split(',')))
          pldn.remove('None')
          for i,j in zip(pld, pldn):
            pembed.add_field(name= f'{pld.index(i)}. {j}', value= i, inline= True)
          await ctx.channel.send(embed = pembed)
      
      else:
       await ctx.response.send_message('Please enter a valid name of playlist', ephemeral=True) 
       
       
#=========================================================================================
#==================================== create playlist ====================================
#=========================================================================================
      
@bot.slash_command(name = 'playlist-create', description= 'create playlist and access anytime')
async def createplaylist(ctx: Interaction, name: str):
  async with aiosqlite.connect('databases/main.db') as db:
    async with db.cursor() as cursor:
      
      await cursor.execute(f'''SELECT * FROM playlist WHERE member_id == {ctx.user.id}''')
      pdata = await cursor.fetchone()
      if not pdata:
        await cursor.execute(f'''INSERT INTO playlist(member_id, member_name) VALUES (?, ?)''', (ctx.user.id, ctx.user.name,))
        await db.commit()
        
      await cursor.execute(f'''SELECT playlist1, playlist2, playlist3, playlist4, playlist5 FROM playlist WHERE member_id == {ctx.user.id}''')
      ch = await cursor.fetchone()
      await db.commit()
      if name in ch:
        await ctx.response.send_message('You have already created the playlist with that name', ephemeral=True)
        return
      
      await cursor.execute(f'''SELECT noplaylistcreated FROM playlist WHERE member_id == {ctx.user.id}''')
      data = await cursor.fetchone()
      await db.commit()
      
      if str(ch[0]) == 'None':
        await ctx.response.send_message(f'Created Playlist named {name}', ephemeral=True)
        await cursor.execute(f'''UPDATE playlist SET playlist1 = "{name}" WHERE member_id == {ctx.user.id}''')
        await cursor.execute(f'''UPDATE playlist SET noplaylistcreated = noplaylistcreated+1 WHERE member_id == {ctx.user.id}''')
        await db.commit()
        return
        
      if str(ch[1]) == 'None':
        await ctx.response.send_message(f'Created Playlist named {name}', ephemeral=True)
        await cursor.execute(f'''UPDATE playlist SET playlist2 = "{name}" WHERE member_id == {ctx.user.id}''')
        await cursor.execute(f'''UPDATE playlist SET noplaylistcreated = noplaylistcreated+1 WHERE member_id == {ctx.user.id}''')
        await db.commit()
        return
      
      if str(ch[2]) == 'None':
        await ctx.response.send_message(f'Created Playlist named {name}', ephemeral=True)
        await cursor.execute(f'''UPDATE playlist SET playlist3 = "{name}" WHERE member_id == {ctx.user.id}''')
        await cursor.execute(f'''UPDATE playlist SET noplaylistcreated = noplaylistcreated+1 WHERE member_id == {ctx.user.id}''')
        await db.commit()
        return
        
      if str(ch[3]) == 'None':
        await ctx.response.send_message(f'Created Playlist named {name}', ephemeral=True)
        await cursor.execute(f'''UPDATE playlist SET playlist4 = "{name}" WHERE member_id == {ctx.user.id}''')
        await cursor.execute(f'''UPDATE playlist SET noplaylistcreated = noplaylistcreated+1 WHERE member_id == {ctx.user.id}''')
        await db.commit()
        return
        
      if str(ch[4]) == 'None':
        await ctx.response.send_message(f'Created Playlist named {name}', ephemeral=True)
        await cursor.execute(f'''UPDATE playlist SET playlist5 = "{name}" WHERE member_id == {ctx.user.id}''')
        await cursor.execute(f'''UPDATE playlist SET noplaylistcreated = noplaylistcreated+1 WHERE member_id == {ctx.user.id}''')
        await db.commit()
        return
    
      else:
        await ctx.response.send_message(f'{ctx.user.mention} you have used all of your 5 playlist slots', ephemeral=True)
        return
      
      

#=========================================================================================
#====================================  playlistadd =======================================
#=========================================================================================


@bot.slash_command(name = 'playlistadd', description= 'Add a song to the playlist')
async def playlistadd(ctx: Interaction, input: str, name: str):
  if input.startswith('https://youtu.be/') or input.startswith('https://www.youtube.com/') or input.startswith('youtube.com/'):
    plist = []
    nlist = []
    lili = []
    fl = []
    fs = ""
    nl = []
    ns = ""
    pstr = ""
    nstr = ""

    async with aiosqlite.connect('databases/main.db') as db:
      async with db.cursor() as cursor:
        try:
          await cursor.execute(f'''SELECT playlist1, playlist2, playlist3, playlist4, playlist5 FROM playlist WHERE member_id == {ctx.user.id}''')
          data = await cursor.fetchone()
          await db.commit()
          for i in data:
            plist.append(i)
            
          if name in plist:
            await ctx.response.send_message(f'Playlist {name} updated', ephemeral=True)
            ydl_opts = {'format': 'bestaudio/audio', 'postprocessors': [{'key':'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': ''}]}
            with YoutubeDL.YoutubeDL(ydl_opts) as ydl:
              info = ydl.extract_info(input, download = False)
            title1 = info['title']
            thumbnails = info.get('thumbnails')
            urlimage = thumbnails[-1].get('url')
            duration = info.get('duration')
            
            if name == plist[0]:
              await cursor.execute(f'''SELECT pld1 FROM playlist WHERE member_id == {ctx.user.id}''')
              data2 = await cursor.fetchone()
              await db.commit()
              await cursor.execute(f'''SELECT pldn1 FROM playlist WHERE member_id == {ctx.user.id}''')
              data3 = await cursor.fetchone()
              await db.commit()
              pstr = list(map(str, str(data2[0]).split(',')))
              nstr = list(map(str, str(data3[0]).split(',')))
              lili.append(input)
              nlist.append(title1[:25])
              fl = pstr + lili
              nl = nstr + nlist
              fs = ','.join(map(str, fl))
              ns = ','.join(map(str, nl))
              await cursor.execute(f'''UPDATE playlist SET pld1 = "{fs}" WHERE member_id == {ctx.user.id}''')
              await cursor.execute(f'''UPDATE playlist SET pldn1 = "{ns}" WHERE member_id == {ctx.user.id}''')
              await db.commit()
              
            elif name == plist[1]:
              await cursor.execute(f'''SELECT pld2 FROM playlist WHERE member_id == {ctx.user.id}''')
              data2 = await cursor.fetchone()
              await db.commit()
              await cursor.execute(f'''SELECT pldn2 FROM playlist WHERE member_id == {ctx.user.id}''')
              data3 = await cursor.fetchone()
              await db.commit()
              pstr = list(map(str, str(data2[0]).split(',')))
              nstr = list(map(str, str(data3[0]).split(',')))
              lili.append(input)
              nlist.append(title1[:25])
              fl = pstr + lili
              nl = nstr + nlist
              fs = ','.join(map(str, fl))
              ns = ','.join(map(str, nl))
              await cursor.execute(f'''UPDATE playlist SET pld2 = "{fs}" WHERE member_id == {ctx.user.id}''')
              await cursor.execute(f'''UPDATE playlist SET pldn2 = "{ns}" WHERE member_id == {ctx.user.id}''')
              await db.commit()
              
            elif name == plist[2]:
              await cursor.execute(f'''SELECT pld3 FROM playlist WHERE member_id == {ctx.user.id}''')
              data2 = await cursor.fetchone()
              await db.commit()
              await cursor.execute(f'''SELECT pldn3 FROM playlist WHERE member_id == {ctx.user.id}''')
              data3 = await cursor.fetchone()
              await db.commit()
              pstr = list(map(str, str(data2[0]).split(',')))
              nstr = list(map(str, str(data3[0]).split(',')))
              lili.append(input)
              nlist.append(title1[:25])
              fl = pstr + lili
              nl = nstr + nlist
              fs = ','.join(map(str, fl))
              ns = ','.join(map(str, nl))
              await cursor.execute(f'''UPDATE playlist SET pld3 = "{fs}" WHERE member_id == {ctx.user.id}''')
              await cursor.execute(f'''UPDATE playlist SET pldn3 = "{ns}" WHERE member_id == {ctx.user.id}''')
              await db.commit()
              
            elif name == plist[3]:
              await cursor.execute(f'''SELECT pld4 FROM playlist WHERE member_id == {ctx.user.id}''')
              data2 = await cursor.fetchone()
              await db.commit()
              await cursor.execute(f'''SELECT pldn4 FROM playlist WHERE member_id == {ctx.user.id}''')
              data3 = await cursor.fetchone()
              await db.commit()
              pstr = list(map(str, str(data2[0]).split(',')))
              nstr = list(map(str, str(data3[0]).split(',')))
              lili.append(input)
              nlist.append(title1[:25])
              fl = pstr + lili
              nl = nstr + nlist
              fs = ','.join(map(str, fl))
              ns = ','.join(map(str, nl))
              await cursor.execute(f'''UPDATE playlist SET pld4 = "{fs}" WHERE member_id == {ctx.user.id}''')
              await cursor.execute(f'''UPDATE playlist SET pldn4 = "{ns}" WHERE member_id == {ctx.user.id}''')
              await db.commit()
              
            elif name == plist[4]:
              await cursor.execute(f'''SELECT pld5 FROM playlist WHERE member_id == {ctx.user.id}''')
              data2 = await cursor.fetchone()
              await db.commit()
              await cursor.execute(f'''SELECT pldn5 FROM playlist WHERE member_id == {ctx.user.id}''')
              data3 = await cursor.fetchone()
              await db.commit()
              pstr = list(map(str, str(data2[0]).split(',')))
              nstr = list(map(str, str(data3[0]).split(',')))
              lili.append(input)
              nlist.append(title1[:25])
              fl = pstr + lili
              nl = nstr + nlist
              fs = ','.join(map(str, fl))
              ns = ','.join(map(str, nl))
              await cursor.execute(f'''UPDATE playlist SET pld5 = "{fs}" WHERE member_id == {ctx.user.id}''')
              await cursor.execute(f'''UPDATE playlist SET pldn5 = "{ns}" WHERE member_id == {ctx.user.id}''')
              await db.commit()
            
            else:
              await ctx.response.send_message('You have to create a playlist first')
        except:
          await ctx.response.send_message('An error occured please try again!')  
  else:
    await ctx.response.send_message('Please enter a valid youtube video link only', ephemeral=True)
      
@bot.slash_command(name = 'text-voice-channel', description = 'sets this channel as default for the text-voice translation.')
async def textvoice(ctx: Interaction):
  await ctx.response.send_message(f'Now the text to voice translation will only work on {ctx.channel.name}')
  async with aiosqlite.connect('databases/main.db') as db:
    async with db.cursor() as cursor:
      await cursor.execute(f'''UPDATE guilds SET textvoice = {ctx.channel.id} WHERE guild_id == {ctx.guild.id}''')
    await db.commit()
      
@bot.slash_command(name = 'play', description= 'enjoy the music')
async def play(ctx: Interaction, input: str):
  await ctx.response.send_message('Loading......!', ephemeral= True)
  await play1(ctx= ctx,url2= input)
  
@bot.slash_command(name = 'playlistplay', description= 'enjoy the music')
async def playlistplay(ctx: Interaction, name: str):
  await ctx.response.send_message('Loading......!', ephemeral= True)
  await playlistplay1(ctx= ctx,name = name)
  
@bot.slash_command(name = 'queue', description='shows the currently playing queue')
async def queuec(ctx: Interaction):
  await ctx.response.send_message('Queue......', ephemeral=True)
  await queue1(ctx)

@bot.slash_command(name = 'loop', description= 'loop the currently playing queue')
async def loopc(ctx: Interaction):
  await ctx.response.send_message('Looping.......', ephemeral=True)
  await loop1(ctx)
  
@bot.slash_command(name = 'skip', description= 'skips one song from the queue')
async def skip(ctx: Interaction):
  await ctx.response.send_message('Skipping....', ephemeral=True)
  await skip1(ctx)
  
@bot.slash_command(name = 'remove', description = 'Remove any music from the queue')
async def remove(ctx: Interaction, position: int):
  await ctx.response.send_message('Removing.........', ephemeral=True)
  await remove1(ctx, position)
  
@bot.slash_command(name = 'transandsave', description='translates the text to voice and sends its audio file')
async def transandsave(ctx: Interaction, text: str):
  sound = gTTS(text = text, lang = 'hi', slow=False)
  mp3_fp = io.BytesIO()
  sound.write_to_fp(fp = mp3_fp)
  mp3_fp.seek(0)
  await ctx.response.send_message(file=nextcord.File(mp3_fp, filename=f"{text[:15]}.mp3"), ephemeral= True)
  
@bot.slash_command(name = 'get', description= 'Get a youtube video downlaod link')
async def get(ctx: Interaction, input: str):
  await ctx.response.send_message('Wait for a while, getting the link.....', ephemeral=True)
  await getf.get1(ctx, input)
  
@bot.slash_command(name = 'clear', description= 'delete out messgaes')
@application_checks.has_permissions(manage_messages=True)
async def clear(ctx = Interaction):
  await ctx.response.send_message(f'Deleting messages....', ephemeral = True)
  await clear1(ctx)
  
#@bot.command()
#async def add(ctx):
#  async with aiosqlite.connect('databases/main.db') as db:
#    async with db.cursor() as cursor:
#      await cursor.execute(f'DELETE FROM playlist WHERE member_id == '')
#    await db.commit()


#=========================================================================================
#====================================Translator===========================================
#=========================================================================================

@bot.slash_command(name = 'speak', description = 'text to speech', guild_ids= testcommands)
async def speak(ctx: Interaction, msg: str):
  user = ctx.user
  if user.voice != None:
    await ctx.response.send_message('Translating..........', ephemeral= True)
    try:
      vc = await user.voice.channel.connect()
    except:
      guild = ctx.guild
      vc = guild.voice_client
      
    try:  
      if ctx.guild.voice_client.is_playing():
        await ctx.response.send_message(f'{ctx.user.mention}The bot is currently in use.')
        return
    except:
      pass
  
    sound = gTTS(text= msg, lang='hi', slow=False)
    sound.save('tts.audio.mp3')
                
    source = await FFmpegOpusAudio.from_probe('tts.audio.mp3', method='fallback')
    vc.play(source)

  else:
    await ctx.response.send_message('You need to first join a voice channel!', ephemeral= True )
    return
      
bot.run("YOUR-BOT-TOKEN-HERE")