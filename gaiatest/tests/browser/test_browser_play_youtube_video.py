# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By
from gaiatest import GaiaTestCase
from gaiatest.apps.browser.app import Browser
from gaiatest.apps.browser.regions.html5_player import HTML5Player


class TestYouTube(GaiaTestCase):

    video_URL = 'http://m.youtube.com/watch?v=5MzuGWFIfio'

    # YouTube video
    _video_container_locator = (By.CSS_SELECTOR, 'div[style^="background-image"]')
    _video_element_locator = (By.TAG_NAME, 'video')

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.connect_to_network()

    def test_play_youtube_video(self):
        """Confirm YouTube video playback

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
        video = self.marionette.find_element(*self._video_element_locator)
        player = HTML5Player(self.marionette, video)

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

        # Forward
        forward_point = (player.playback_duration - player.current_timestamp) / 2
        player.seek(forward_point)
        player.wait_till_video_loaded()
        self.assertTrue(player.is_video_playing)

        # Rewind
        backward_point = player.current_timestamp / 2
        player.seek(backward_point)
        player.wait_till_video_loaded()
        self.assertTrue(player.is_video_playing)
