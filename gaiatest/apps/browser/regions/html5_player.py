# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from gaiatest.apps.base import PageRegion


class HTML5Player(PageRegion):
    """Represents HTML5 Player.

    Reference:
    http://www.w3.org/TR/2012/WD-html5-20121025/media-elements.html#media-element
    """

    def wait_for_video_loaded(self):
        self.wait_for_condition(
            lambda m:
            int(self.root_element.get_attribute('readyState')) == 4)

    @property
    def is_paused(self):
        return self.root_element.get_attribute('paused') == 'true'

    def invoke_controls(self):
        self.root_element.tap()
        time.sleep(.25)

    def play(self):
        self.invoke_controls()
        self.root_element.tap()
        self.wait_for_condition(lambda m: not self.is_paused)

    def pause(self):
        self.invoke_controls()
        self.root_element.tap()
        self.wait_for_condition(lambda m: self.is_paused)

    def is_video_playing(self):
        # get 4 timestamps during approx. 1 sec
        # ensure that newer timestamp has greater value than previous one
        timestamps = []
        for i in range(4):
            timestamps.append(self.current_timestamp)
            time.sleep(.25)
        return all([timestamps[i - 1] < timestamps[i] for i in range(1, 3)])

    @property
    def current_timestamp(self):
        return float(self.root_element.get_attribute('currentTime'))
