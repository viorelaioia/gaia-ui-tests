# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By
from gaiatest import GaiaTestCase
from gaiatest.apps.lockscreen.app import LockScreen


class TestLockScreen(GaiaTestCase):

    _input_passcode = '7931'
    _emergency_dialer_keypad_locator = (By.ID, 'keypad')

    def setUp(self):
        GaiaTestCase.setUp(self)

        #set passcode-lock
        self.data_layer.set_setting('lockscreen.passcode-lock.code', self._input_passcode)
        self.data_layer.set_setting('lockscreen.passcode-lock.enabled', True)

        # this time we need it locked!
        self.lockscreen.lock()
        self.lock_screen = LockScreen(self.marionette)
        self.lock_screen.wait_for_lockscreen_handle_visible()

    def test_lockscreen_open_to_emergency_call_screen(self):
        """Test that emergency call screen can open

        https://github.com/mozilla/gaia-ui-tests/issues/762
        """
        self.lock_screen.swipe_to_unlock()
        self.lock_screen.tap_unlock_button()
        self.lock_screen.passcode_pad.tap_emergency_call()

        self.assertTrue(self.is_element_displayed(*self._emergency_dialer_keypad_locator))
