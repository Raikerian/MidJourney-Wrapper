import discord
import Globals
from keep_alive import keep_alive
from Salai import PassPromptToSelfBot, Upscale, MaxUpscale, Variation

bot = discord.Bot(intents=discord.Intents.all())
#client = discord.Client(intents = discord.Intents.all())


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command(description="Says hello (creative, isn't it?).")
async def hello(ctx):
    await ctx.respond("Hello!")


@bot.command(description="This command is a wrapper of MidJourneyAI")
async def mj_imagine(ctx, prompt: discord.Option(str)):
    response = PassPromptToSelfBot(prompt)
    if response.status_code >= 400:
        await ctx.respond("Request has failed; please try later")
    else:
        await ctx.respond(
            "Your image is being prepared, please wait a moment...")


@bot.command(description="Upscale one of images generated by MidJourney")
async def mj_upscale(ctx, index: discord.Option(int), reset_target : discord.Option(bool) =True):
    if (index <= 0 or index > 4):
        await ctx.respond("Invalid argument, pick from 1 to 4")
        return

    if Globals.targetID == "":
        await ctx.respond(
            'You did not set target. To do so reply to targeted message with "$mj_target"'
        )
        return

    response = Upscale(index, Globals.targetID)
    if reset_target:
        Globals.targetID = ""
    if response.status_code >= 400:
        await ctx.respond("Request has failed; please try later")
        return

    await ctx.respond("Your image is being prepared, please wait a moment...")

@bot.command(description="Upscale to max targetted image (should be already upscaled using mj_upscale)")
async def mj_upscale_to_max(ctx):
    if Globals.targetID == "":
        await ctx.respond(
            'You did not set target. To do so reply to targeted message with "$mj_target"'
        )
        return

    response = MaxUpscale(Globals.targetID)
    Globals.targetID = ""
    if response.status_code >= 400:
        await ctx.respond("Request has failed; please try later")
        return

    await ctx.respond("Your image is being prepared, please wait a moment...")

@bot.command(description = "Make variation given index after target has been set")
async def mj_variation(ctx, index: discord.Option(int), reset_target : discord.Option(bool) =True):
    if (index <= 0 or index > 4):
        await ctx.respond("Invalid argument, pick from 1 to 4")
        return

    if Globals.targetID == "":
        await ctx.respond(
            'You did not set target. To do so reply to targeted message with "$mj_target"'
        )
        return

    response = Variation(index, Globals.targetID)
    if reset_target:
        Globals.targetID = ""
    if response.status_code >= 400:
        await ctx.respond("Request has failed; please try later")
        return

    await ctx.respond("Your image is being prepared, please wait a moment...")



@bot.event
async def on_message(message):
    if message.content == "": return
    if "$mj_target" in message.content and message.content[0] == '$':
        try:
            Globals.targetID = str(message.reference.message_id)
        except:
            await message.channel.send(
                "Exception has occured, maybe you didn't reply to MidJourney message"
            )
            await message.delete()
            return
        if str(message.reference.resolved.author.id) != Globals.MID_JOURNEY_ID:
            await message.channel.send(
                "Use the command only when you reply to MidJourney")
            await message.delete()
            return
        await message.channel.send("Done")
        await message.delete()


keep_alive()
bot.run(Globals.DAVINCI_TOKEN)