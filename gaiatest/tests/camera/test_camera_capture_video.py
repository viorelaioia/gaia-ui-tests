# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re
import time

from gaiatest import GaiaTestCase
from gaiatest.apps.camera.app import Camera


class TestCamera(GaiaTestCase):

    videos_dir = '/sdcard/DCIM/100MZLLA'

    def setUp(self):
        GaiaTestCase.setUp(self)

        # Turn off geolocation prompt
        self.apps.set_permission('Camera', 'geolocation', 'deny')

    def test_capture_a_video(self):
        # https://moztrap.mozilla.org/manage/case/2477/

        self.camera = Camera(self.marionette)
        self.camera.launch()

        videos_before_test = self.get_sdcard_video_list()

        self.camera.tap_switch_source()

        self.camera.tap_capture()
        self.camera.wait_for_video_capturing()

        # Wait for 3 seconds of recording
        self.wait_for_condition(lambda m: self.camera.video_timer >= time.strptime('00:03', '%M:%S'))

        # Stop recording
        self.camera.tap_capture()
        self.camera.wait_for_video_timer_not_visible()

        # Wait for image to be added in to filmstrip
        self.camera.wait_for_filmstrip_visible()

        # Find the new film thumbnail in the film strip
        self.assertTrue(self.camera.is_filmstrip_visible)

        # Check that video saved to sdcard
        videos_after_test = self.get_sdcard_video_list()
        self.assertGreater(len(videos_after_test), len(videos_before_test))

    def get_sdcard_video_list(self):
        files = self.device.manager.listFiles(self.videos_dir)
        videos = []
        for f in files:
            try:
                name = re.search('(?P<name>.*)[.]3gp', f).groupdict()['name']
                videos.append(name)
            except AttributeError:
                pass
        return videos
