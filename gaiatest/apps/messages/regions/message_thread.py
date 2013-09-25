# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By
from gaiatest.apps.base import Base
from gaiatest.apps.base import PageRegion


class MessageThread(Base):

    _all_messages_locator = (By.CSS_SELECTOR, '#messages-container li.message')
    _received_message_content_locator = (By.CSS_SELECTOR, "#messages-container li.message.received")
    _edit_message_locator = (By.ID, 'messages-edit-icon')

    def wait_for_received_messages(self, timeout=180):
        self.wait_for_element_displayed(*self._received_message_content_locator, timeout=timeout)

    @property
    def received_messages(self):
        return [Message(self.marionette, message) for message in self.marionette.find_elements(*self._received_message_content_locator)]

    @property
    def all_messages(self):
        return [Message(self.marionette, message) for message in self.marionette.find_elements(*self._all_messages_locator)]

    def edit_message(self):
        self.marionette.find_element(*self._edit_message_locator).tap()
        return EditMessages(self.marionette)

    @property
    def editmessage(self):
        return EditMessages(self.marionette)


class EditMessages(Base):

    _select_all_messages_button_locator = (By.ID, 'messages-check-all-button')
    _delete_button_locator = (By.ID, 'messages-delete-button')

    def select_all_messages(self):
        self.marionette.find_element(*self._select_all_messages_button_locator).tap()

    def delete_selected_messages(self):
        self.marionette.find_element(*self._delete_button_locator).tap()
        return DeleteConfirmation(self.marionette)


class DeleteConfirmation(Base):

    _message_locator = (By.CSS_SELECTOR, '#modal-dialog-confirm.visible')
    _confirm_delete_locator = (By.CSS_SELECTOR, '#modal-dialog-confirm-ok')

    def __init__(self, marionette):
        Base.__init__(self, marionette)

        self.marionette.switch_to_frame()
        self.wait_for_element_displayed(*self._message_locator)

    def delete_confirmation(self):
        self.marionette.find_element(*self._confirm_delete_locator).tap()


class Message(PageRegion):

    _text_locator = (By.CSS_SELECTOR, '.bubble > p')
    _attachments_locator = (By.CSS_SELECTOR, '.bubble .attachment-container.preview')

    @property
    def text(self):
        return self.root_element.find_element(*self._text_locator).text

    @property
    def has_attachments(self):
        try:
            self.root_element.find_element(*self._attachments_locator)
        except:
            return False

        return True

    @property
    def id(self):
        return self.root_element.get_attribute('id')
