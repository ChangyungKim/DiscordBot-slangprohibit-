import asyncio
import logging
import requests
import discord
from discord.ext import commands
from speech_recognition import RequestError, UnknownValueError

from speech.spch_snk import SpchSnk

logger = logging.getLogger("speech.spch_rcgn")
host_url="http://15.164.32.148:8000/"

class SpeechCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.connections = {}  # Cache of voice connections

    @discord.command()
    async def start(self, ctx: discord.ApplicationContext):
        # Start transcription.
        voice = ctx.author.voice
        if not voice:
            return await ctx.respond("You're not in a vc right now")

        vc = await voice.channel.connect()
        self.connections.update({ctx.guild.id: vc})
 
        # The recording takes place in the sink object.
        # SRSink will discard the audio once is transcribed.
        vc.start_recording(SpchSnk(self.speech_callback_bridge, ctx), self.stop_callback)

        await ctx.respond("The transcription has started!")

    @discord.command()
    async def stop(self, ctx: discord.ApplicationContext):
        # Stop transcription.
        if ctx.guild.id in self.connections:
            vc = self.connections[ctx.guild.id]
            vc.stop_recording()
            del self.connections[ctx.guild.id]
            await ctx.delete()
        else:
            await ctx.respond("Not recording in this guild.")

    async def stop_callback(self, sink):
        await sink.vc.disconnect()

    def speech_callback_bridge(self, recognizer, audio, ctx, user):
        asyncio.run_coroutine_threadsafe(
            self.speech_callback(recognizer, audio, ctx, user), self.bot.loop
        )

    async def speech_callback(self, recognizer, audio, ctx, user):
        try:
            text = recognizer.recognize_google(audio, language='ko-KR')
        except UnknownValueError:
            logger.debug("Google Speech Recognition could not understand audio")
        except RequestError as e:
            logger.exception(
                "Could not request results from Google Speech Recognition service",
                exc_info=e,
            )
        else:
            url_storesentence = host_url + "storesentence/"
            userid = user
            spoken_sentence = text
            serverid = ctx.guild.id  # random
            sentence_json = {"server": serverid, "user": userid, "sentence": spoken_sentence}
            request = requests.post(url_storesentence, json=sentence_json)
            count=request.json()["count"]
            if count>0:
                await ctx.send(f"<@{user}> ")


def setup(bot):
    bot.add_cog(SpeechCog(bot))
