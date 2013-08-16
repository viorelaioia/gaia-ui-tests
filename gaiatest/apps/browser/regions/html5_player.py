# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from gaiatest.apps.base import PageRegion


class HTML5Player(PageRegion):
    """Represents HTML5 Player

    Reference:
    http://www.w3.org/TR/2012/WD-html5-20121025/media-elements.html#media-element
    """

    script_template = 'return document.getElementsByTagName("video")[0]'

    def wait_till_video_loaded(self):
        # wait till player HAVE_ENOUGH_DATA
        self.wait_for_condition(lambda m: m.execute_script('%s.readyState == 4' % self.script_template))

    def invoke_controls(self):
        # there is no way to verify that they're present
        self.root_element.tap()
        time.sleep(.25)

    def play(self):
        self.invoke_controls()
        self.root_element.tap()
        self.wait_for_condition(lambda m: not m.execute_script('%s.paused' % self.script_template))
        return self.current_timestamp

    def pause(self):
        self.invoke_controls()
        self.root_element.tap()
        self.wait_for_condition(lambda m: m.execute_script('%s.paused' % self.script_template))
        return self.current_timestamp

    def seek(self, timestamp):
        t = float(timestamp)
        if 0 <= t <= self.duration:
            self.marionette.execute_script('%s.currentTime = %s' % (self.script_template, t))
        else:
            raise Exception('Provided value is not in range [0; %s]' % self.duration)

    def is_video_playing(self):
        # get 4 timestamps during approx. 1 sec
        # ensure that newer timestamp has bigger value than previous one
        timestamps = []
        for i in range(4):
            timestamps.append(self.current_timestamp)
            time.sleep(.25)
        return all([timestamps[i - 1] < timestamps[i] for i in range(1, 3)])

    @property
    def current_timestamp(self):
        return self.marionette.execute_script('%s.currentTime' % self.script_template)

    @property
    def duration(self):
        return self.marionette.execute_script('%s.duration' % self.script_template)
