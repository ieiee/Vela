import nextcord
from nextcord.ext import commands

class autodelete(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.count = 0
        
    @commands.Cog.listener()
    async def on_message(self, ctx: commands.Context):
        self.count += 1
        if ctx.author == self.bot.user:
            return
        if self.count >= 10:
            await ctx.channel.purge()
            await ctx.channel.send('Done')
            self.count = 0
        else:
            return
        
async def setup(bot: commands.Bot):
    bot.add_cog(autodelete(bot))