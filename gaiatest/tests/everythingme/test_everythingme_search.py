# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.keys import Keys

from gaiatest import GaiaTestCase


class TestEverythingMeSearch(GaiaTestCase):

    # Everything.Me locators
    _shortcut_items_locator = ('css selector', '#shortcuts-items li')
    _search_box_locator = ('id', 'search-q')
    _search_title_locator = ('id', 'search-title')
    _loading_apps_locator = ('css selector', 'div.loading-apps')

    # Homescreen locators
    _homescreen_frame_locator = ('css selector', 'div.homescreen > iframe')

    # Search string
    _test_string = "skyfall"

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.apps.set_permission('Homescreen', 'geolocation', 'deny')
        self.connect_to_network()

    def test_launch_everything_me_search(self):
        # This test does a search with a common string and asserts
        # that the title and shortcuts are listed

        # swipe to Everything.Me
        hs_frame = self.marionette.find_element(*self._homescreen_frame_locator)
        self.marionette.switch_to_frame(hs_frame)

        # We'll use js to flick pages for reliability/Touch is unreliable
        self.marionette.execute_script("window.wrappedJSObject.GridManager.goToPreviousPage();")
        self.wait_for_condition(lambda m: m.find_element('tag name', 'body')
            .get_attribute('data-transitioning') != 'true')

        # Find the search box and clear it
        self.wait_for_element_displayed(*self._search_box_locator)
        search_input = self.marionette.find_element(*self._search_box_locator)
        search_input.clear()

        # Enter the string to search
        search_input.send_keys(self._test_string)
        search_input.send_keys(Keys.RETURN)

        # Wait for the title to appear and assert it
        self.wait_for_element_displayed(*self._search_title_locator)
        title_text = self.marionette.find_element(*self._search_title_locator).text
        self.assertIn(self._test_string, title_text)

        # Check that shortcuts are present. Loading spinner may still be showing
        self.wait_for_element_not_displayed(*self._loading_apps_locator)

        shortcuts = self.marionette.find_elements(*self._shortcut_items_locator)
        self.assertGreater(len(shortcuts), 0, 'No shortcut categories found')
