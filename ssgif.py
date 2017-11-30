#!/usr/bin/env python

import os
import time

import concurrent.futures
import moviepy.video.io.ImageSequenceClip as isc
import pyscreenshot as screen


class Capture(object):
    DEFAULT_FPS = 30

    def __init__(self, root_dir, fps=DEFAULT_FPS, executor=concurrent.futures.ThreadPoolExecutor(max_workers=60)):
        super(Capture, self).__init__()
        self.executor = executor
        self.root_dir = root_dir
        self.fps = fps
        self.interval = 1.0 / (self.fps * 1.0)

        if not os.path.exists(self.root_dir):
            os.makedirs(self.root_dir)

        assert os.path.exists(self.root_dir), 'the directory %s must exist.' % self.root_dir

    def loop(self):

        def capture(uid):
            file_name = os.path.join(self.root_dir, '%s.png' % uid)
            screen.grab_to_file(file_name)

        ctr = 0
        while ctr < (30):
            self.executor.submit(lambda *args: capture(ctr))
            ctr += 1
            time.sleep(self.interval)

    def transcode(self):
        files = [os.path.join(self.root_dir, f) for f in os.listdir(self.root_dir) if f.endswith('.png')]
        clip = isc.ImageSequenceClip(files, fps=30)
        clip.write_gif(os.path.join(self.root_dir, '../out.gif'))


if __name__ == '__main__':
    ss_dir = os.path.join(os.environ['HOME'], 'Desktop', 'ss')

    capture = Capture(ss_dir)
    capture.loop()
    capture.transcode()
