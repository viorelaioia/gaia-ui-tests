# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.keys import Keys

from gaiatest import GaiaTestCase
from gaiatest.apps.everythingme.app import EverythingMe


class TestEverythingMeSearchAccented(GaiaTestCase):

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.apps.set_permission('Homescreen', 'geolocation', 'deny')
        self.connect_to_network()
        self.everythingme = EverythingMe(self.marionette)

    def test_launch_everything_me_search(self):
        self.everythingme.go_to_everything_me()

        self.everythingme.wait_for_search_box_displayed()
        self.everythingme.type_into_search_box(u'Özdemir Erdoğan')
        self.everythingme.wait_for_search_tips_displayed()
        self.everythingme.tap_search_tip()

        self.everythingme.wait_for_categories_present()
        self.assertGreater(self.everythingme.categories_count, 0, 'No shortcut categories found')
        self.keyboard.tap_enter()
