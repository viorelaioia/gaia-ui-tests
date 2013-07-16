# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# NOTE: Requires the 'PyBluez' host-side Bluetooth python module
# See: http://code.google.com/p/pybluez/wiki/Documentation

import time

from gaiatest.tests.bluetooth.bluetooth_host import BluetoothHost
from gaiatest import GaiaTestCase


class TestBluetoothDiscoverable(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)

        # Bluetooth host object
        self.bt_host = BluetoothHost()

        # If bluetooth is enabled on the device turn it off to ensure no existing connections
        # Use common methods once https://github.com/mozilla/gaia-ui-tests/pull/600 is merged
        # self.data_layer.disable_bluetooth(self)
        self.data_layer.set_setting('bluetooth.enabled', False)
        time.sleep(5)

        # Enable device-side bluetooth
        # Use common method once https://github.com/mozilla/gaia-ui-tests/pull/600 is merged
        # self.data_layer.enable_bluetooth(self)
        self.data_layer.set_setting('bluetooth.enabled', True)
        time.sleep(5)

        # Add once https://github.com/mozilla/gaia-ui-tests/pull/600 is merged
        # Remove any existing device pairings so we are starting clean
        # self.data_layer.unpair_all_bluetooth_devices(self)

    def test_discoverable(self):
        # Set our device's bluetooth name uniquely so we can identify it
        device_name = str(time.time())
        self.marionette.log("Setting device's bluetooth name to '%s'" % device_name)
        self.data_layer.bt_set_device_name(device_name)

        # Place our device in discoverable mode so it can be found by host machine
        self.marionette.log("Setting device discoverable mode ON")
        self.data_layer.bt_set_device_discoverable(True)

        # Have host machine perform inquiry and look for our device
        device_found = self.bt_host.is_device_visible(self, device_name)
        self.assertTrue(device_found, "Host should see our device (device discoverable mode is ON)")

        # Take the device out of discoverable mode
        self.marionette.log("Setting device discoverable mode OFF")
        self.data_layer.bt_set_device_discoverable(False)

        # Now have host machine inquire and shouldn't find our device
        device_found = self.bt_host.is_device_visible(self, device_name)
        self.assertFalse(device_found, "Host shouldn't see our device (device discoverable mode is OFF)")

        # Disable device-side bluetooth
        # Use common method once https://github.com/mozilla/gaia-ui-tests/pull/600 is merged
        # self.data_layer.disable_bluetooth(self)
        self.data_layer.set_setting('bluetooth.enabled', False)
        time.sleep(5)
