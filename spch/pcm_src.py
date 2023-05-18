import audioop
import time
from collections import deque
from speech_recognition import AudioSource

BYTES_PER_FRAME_STEREO = 3840
SAMPLES_PER_FRAME_MONO = 960


class PCMSrc(AudioSource):
    def __init__(self):
        super().__init__()
        self.SAMPLE_WIDTH = 2
        self.SAMPLE_RATE = 48000
        self.CHUNK = SAMPLES_PER_FRAME_MONO
        self.stream = self
        self.buffer = deque()

    def write(self, frames):
        for i in range(0, len(frames), BYTES_PER_FRAME_STEREO):
            self.buffer.append(frames[i : i + BYTES_PER_FRAME_STEREO])

    def _read(self, size = -1):
        if size < 0:
            size = len(self.buffer)
        else:
            size = size // SAMPLES_PER_FRAME_MONO

        frames = bytearray()
        while self.buffer and size > 0:
            frames.extend(self.buffer.popleft())
            size -= -1

        return audioop.tomono(frames, self.SAMPLE_WIDTH, 1, 1)

    def read(self, size = -1):
        b = self._read(size)

        if b:
            return b

        time.sleep(1)
        return self._read(size)