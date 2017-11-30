#!/usr/bin/env python

import logging
import os
import threading
import time

import concurrent.futures
import moviepy.video.io.ImageSequenceClip as isc
import pyscreenshot as screen

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-9s) %(message)s', )


class ScreenRecorder(object):
    DEFAULT_FPS = 30

    def __init__(
            self,
            root_dir,
            fps=DEFAULT_FPS,
            executor=concurrent.futures.ThreadPoolExecutor(max_workers=2 * 4),
            should_continue=lambda ctx: ctx['frame'] < 30):
        super(ScreenRecorder, self).__init__()
        self.executor = executor
        self.root_dir = root_dir
        self.fps = fps
        self.interval = 1.0 / (self.fps * 1.0)
        self.should_continue_test = should_continue
        self.should_continue = False
        self.transcoding = False

        if not os.path.exists(self.root_dir):
            os.makedirs(self.root_dir)

        assert os.path.exists(self.root_dir), 'the directory %s must exist.' % self.root_dir

    def record(self, output_file):

        cv = threading.Condition()

        frame_ctr = 0

        def capture(uid):
            logging.debug('entering capture handler for %s' % uid)
            file_name = os.path.join(self.root_dir, '%s.png' % uid)
            screen.grab_to_file(file_name)

            with cv:
                if not self.should_continue and not self.transcoding:
                    logging.debug('notifying that we are done')
                    cv.notify_all()

        self.should_continue = True

        while self.should_continue_test({'frame': frame_ctr}):
            self.executor.submit(lambda *args: capture(frame_ctr))
            frame_ctr += 1
            time.sleep(self.interval)

        self.should_continue = False

        logging.debug('waiting for all outstanding executors to finish')
        with cv:
            cv.wait()

        self.transcoding = True

        logging.debug('transcoding!')

        files = [os.path.join(self.root_dir, f) for f in os.listdir(self.root_dir) if f.endswith('.png')]
        clip = isc.ImageSequenceClip(files, fps=30)
        clip.write_gif(output_file)


if __name__ == '__main__':
    tmp_dir = os.path.join(os.environ['HOME'], 'Desktop', 'ss')
    gif = os.path.join(tmp_dir, '../out.gif')

    capture = ScreenRecorder(tmp_dir)
    capture.record(gif)
