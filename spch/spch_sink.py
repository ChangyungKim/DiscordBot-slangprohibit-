import threading
from discord.sinks import Sink # “stores” recorded audio data
from speech_recognition import Recognizer, WaitTimeoutError
from pcm_src import PCMSrc


class SpchSink(Sink):
    def __init__(self, callback, ctx):
        super().__init__()
        self.ctx = ctx
        self.callback = callback
        self.stoppers = {}
        self.recognizer = Recognizer

    def write(self, data, user):
        if user not in self.audio_data:
            source = PCMSrc
            self.audio_data[user] = source
            self.stoppers[user] = self.listen_in_background(
                self.callback, self.ctx, user
            )
        source = self.audio_data[user]
        source.write(data)

    def cleanup(self):
        self.finished = True
        for stopper in self.stoppers.values():
            stopper()

    def listen_in_background(self, callback, ctx, user):
        running = [True]

        def threaded_listen():
            while running[0]:
                try:
                    audio = self.recognizer.listen(self.audio_data[user])
                except WaitTimeoutError:
                    pass
                else:
                    if running[0]:
                        callback(self.recognizer, audio, ctx, user)

        def stopper():
            running[0] = False

        listener_thread = threading.Thread(target=threaded_listen())
        listener_thread.daemon = True
        listener_thread.start()
        return stopper
