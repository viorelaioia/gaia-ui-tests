# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By
from gaiatest.apps.base import Base


class Actions(Base):

    _gallery_button_locator = (By.XPATH, "//a[text()='Gallery']")

    def __init__(self, marionette):
        Base.__init__(self, marionette)
        self.marionette.switch_to_frame()

    def tap_gallery(self):
        self.wait_for_element_displayed(*self._gallery_button_locator)
        self.marionette.find_element(*self._gallery_button_locator).tap()
        from gaiatest.apps.gallery.app import Gallery
        return Gallery(self.marionette)
