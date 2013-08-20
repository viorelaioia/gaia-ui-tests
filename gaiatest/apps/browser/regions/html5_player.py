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

    @property
    def has_enough_data(self):
        return int(self.root_element.get_attribute('readyState')) == 4

    def wait_till_video_loaded(self):
        self.wait_for_condition(lambda m: self.has_enough_data)

    @property
    def is_paused(self):
        value = self.root_element.get_attribute('paused')
        return value == 'true' and True or False

    def invoke_controls(self):
        self.root_element.tap()
        time.sleep(.25)

    def play(self):
        self.invoke_controls()
        self.root_element.tap()
        self.wait_for_condition(lambda m: not self.is_paused)
        return self.current_timestamp

    def pause(self):
        self.invoke_controls()
        self.root_element.tap()
        self.wait_for_condition(lambda m: self.is_paused)
        return self.current_timestamp

    def seek(self, timestamp):
        t = float(timestamp)
        if 0 <= t <= self.playback_duration:
            self.marionette.execute_script('arguments[0].currentTime = arguments[1]',
                                           script_args=[self.root_element, t])
        else:
            raise Exception('Provided value is not in range [0; %s]' % self.playback_duration)

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

    @property
    def playback_duration(self):
        return float(self.root_element.get_attribute('duration'))
