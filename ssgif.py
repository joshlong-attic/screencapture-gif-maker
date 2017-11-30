#!/usr/bin/env python

import os
import time
import threading
import concurrent.futures
import moviepy.video.io.ImageSequenceClip as isc
import pyscreenshot as screen
# TODO ensure that all threadsd finish BEFORE #transcode is called. research http://effbot.org/zone/thread-synchronization.htm and https://stackoverflow.com/questions/10236947/does-python-have-a-similar-control-mechanism-to-javas-countdownlatch/24796823#24796823

class Capture(object):
    DEFAULT_FPS = 30

    def __init__(
            self,
            root_dir,
            fps=DEFAULT_FPS,
            executor=concurrent.futures.ThreadPoolExecutor(max_workers=4),
            should_continue=lambda ctx: ctx['frame'] < 30):
        super(Capture, self).__init__()
        self.executor = executor
        self.root_dir = root_dir
        self.fps = fps
        self.interval = 1.0 / (self.fps * 1.0)
        self.should_continue = should_continue

        if not os.path.exists(self.root_dir):
            os.makedirs(self.root_dir)

        assert os.path.exists(
            self.root_dir), 'the directory %s must exist.' % self.root_dir

    def loop(self):

        frame_ctr = 0

        def capture(uid):
            file_name = os.path.join(self.root_dir, '%s.png' % uid)
            screen.grab_to_file(file_name)

        while self.should_continue({'frame': frame_ctr}):
            self.executor.submit(lambda *args: capture(frame_ctr))
            frame_ctr += 1
            time.sleep(self.interval)

    def transcode(self):
        # todo this MUST run only after all the submitted capture threads finish
        files = [os.path.join(self.root_dir, f) for f in os.listdir(self.root_dir) if f.endswith('.png')]
        clip = isc.ImageSequenceClip(files, fps=30)
        clip.write_gif(os.path.join(self.root_dir, '../out.gif'))


if __name__ == '__main__':
    ss_dir = os.path.join(os.environ['HOME'], 'Desktop', 'ss')

    capture = Capture(ss_dir)
    capture.loop()
    capture.transcode()
    print 'finished!'
