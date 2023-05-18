import asyncio
import discord
import os
from discord.ext import commands

from spch_sink import SpchSink

class SpchRcgn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.connections = {} #Voice connections
        os.mkdir("../stt")
        self.f = open('stt/stt_result.txt', 'w')

    @discord.command()
    async def start(self, ctx: discord.ApplicationContext):
        voice = ctx.author.voice
        if not voice:
            return await ctx.respond("Not in vc")

        vc = await voice.channel.connect()
        self.connections.update({ctx.guild: vc})

        vc.start_recording(SpchSink(self.speech_callback_bridge, ctx), self.stop_callback)

        await ctx.respond("Transcription start")

    @discord.command()
    async def stop(self, ctx: discord.ApplicationContext):
        if ctx.guild_id in self.connections:
            vc = self.connections[ctx.guild_id]
            vc.stop_recording()
            del self.connections[ctx.guild_id]
            await ctx.delete()

    async def stop_callback(self, sink):
        await sink.vc.disconnect()

    def speech_callback_bridge(self, recognizer, audio, ctx, user):
        asyncio.run_coroutine_threadsafe(self.speech_callback(recognizer, audio, ctx, user), self.bot.loop)

    async def speech_callback(self, recognizer, audio, ctx, user):
        text = recognizer.recognize_google(audio)
        await ctx.send(f"<@{user}> said: {text}")
        self.f.write("<@" + user + "> said: " + text)

    def setup(bot):
        bot.add_cog(SpchRcgn(bot))