# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from marionette.by import By
from gaiatest import GaiaTestCase
from gaiatest.apps.browser.app import Browser
from gaiatest.apps.base import PageRegion


class TestYouTube(GaiaTestCase):

    video_URL = 'http://m.youtube.com/watch?v=5MzuGWFIfio'

    # YouTube video
    _video_container_locator = (By.CSS_SELECTOR, 'div._mjs')
    _video_element_locator = (By.TAG_NAME, 'video')

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.connect_to_network()

    def test_play_youtube_video(self):
        """ Confirm YouTube video playback

        https://moztrap.mozilla.org/manage/case/6073/
        """
        browser = Browser(self.marionette)
        browser.launch()
        browser.go_to_url(self.video_URL)
        browser.switch_to_content()

        # Tap the video container
        self.wait_for_element_present(*self._video_container_locator)
        self.marionette.find_element(*self._video_container_locator).tap()

        # Wait HTML5 player to appear
        self.wait_for_element_present(*self._video_element_locator)
        video_tag = self.marionette.find_element(*self._video_element_locator)
        player = YoutubePlayer(self.marionette, video_tag)

        # Check that video is playing
        player.wait_till_video_loaded()
        self.assertTrue(player.is_video_playing())

        # Pause playback
        stopped_at = player.pause()
        self.assertFalse(player.is_video_playing())

        # Resume playback
        resumed_at = player.play()
        self.assertTrue(resumed_at - stopped_at < 1)
        self.assertTrue(player.is_video_playing())


class YoutubePlayer(PageRegion):

    script_template = 'return document.getElementsByTagName("video")[0]'

    def wait_till_video_loaded(self):
        self.wait_for_condition(lambda m: m.execute_script('%s.readyState == 4' % self.script_template))

    def play(self):
        # first tap - pops up controls
        # second tap - resumes playback
        for i in range(2):
            self.root_element.tap()
            time.sleep(0.25)
        self.wait_for_condition(lambda m: not m.execute_script('%s.paused' % self.script_template))
        return self.get_video_timestamp()

    def pause(self):
        # first tap - pops up controls
        # second tap - pauses playback
        for i in range(2):
            self.root_element.tap()
            time.sleep(0.25)
        self.wait_for_condition(lambda m: m.execute_script('%s.paused' % self.script_template))
        return self.get_video_timestamp()

    def is_video_playing(self):
        # get 4 timestamps during approx. 1 sec
        # ensure that newer timestamp has bigger value than previous one
        timestamps = []
        for i in range(4):
            timestamps.append(self.get_video_timestamp())
            time.sleep(0.25)
        return all([timestamps[i - 1] < timestamps[i] for i in range(1, 3)])

    def get_video_timestamp(self):
        return self.marionette.execute_script('%s.currentTime' % self.script_template)
