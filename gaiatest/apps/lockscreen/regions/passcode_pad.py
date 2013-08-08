# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By
from gaiatest.apps.base import PageRegion


class PasscodePad(PageRegion):

    _numeric_button_locator = (By.CSS_SELECTOR, 'a[data-key="%s"]')
    _emergency_button_locator = (By.CSS_SELECTOR, 'a[data-key="e"]')
    _emergency_frame_locator = (By.CSS_SELECTOR, 'iframe[src*="/emergency-call/"]')

    def type_passcode(self, passcode):
        for digit in passcode:
            button_locator = (self._numeric_button_locator[0],
                              self._numeric_button_locator[1] % digit)
            self.root_element.find_element(*button_locator).tap()

    def tap_emergency_call(self):
        self.root_element.find_element(*self._emergency_button_locator).tap()
        emergency_frame = self.marionette.find_element(*self._emergency_frame_locator)
        self.marionette.switch_to_frame(emergency_frame)
        self.wait_for_condition(
            lambda m: m.execute_script('return document.title') == 'Emergency Call Dialer')
