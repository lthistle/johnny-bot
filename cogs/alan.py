import discord
from discord.ext import commands
from modules.modification import MediaScaler
import PIL

embed_template = discord.Embed(
    color = int("8f0bbf", 16),
    title = "Alanify",
)

class Alan(commands.Cog):
    """Set of commands to downscale then upscale images (inspired by Alan)"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def alanify(self, ctx, value : int):
        uid = ctx.author.id
        #make sure user is replying to a message
        replied = ctx.message.reference
        if not replied:
            return
        msg = await ctx.fetch_message(replied.message_id)

        if msg.attachments:
            image_url = msg.attachments[0].url
            print("passed")
        elif msg.embeds:
            if msg.embeds[0].video:
                image_url = msg.embeds[0].video.url
            else:
                image_url = msg.embeds[0].url
        else:
            image_url = None
        
        if image_url:
            print("IMAGE URL IS", image_url)
            ms = MediaScaler()
            media_file, filename = (await ms.download(image_url))
            rfname, ext = await ms.rewrite_media(value, filename)
            # if ext == 'mp4':
            #     embed = discord.Embed(video=)
            await ctx.send(file=discord.File(rfname))
            await ms.remove_all_local()
        print(msg.attachments)

    @alanify.error
    async def alanify_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
            response = embed_template.copy()
            response.description = "Invalid argument passed to 'alanify' command. Example: ?alanify 10"
    #msg.embeds.url has the image url
    #ctx.message.reference
    #?alan beautify 100 (fuckery factor)

def setup(bot):
    bot.add_cog(Alan(bot))