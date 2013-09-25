# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
import time
from gaiatest.apps.messages.app import Messages


class TestDeleteMessage(GaiaTestCase):

    def test_delete_message(self):
        """
        This test sends a text message to itself. It waits for a reply message.
        https://moztrap.mozilla.org/manage/case/1322/
        """

        _text_message_content = "Automated Test %s" % str(time.time())

        # launch the app
        self.messages = Messages(self.marionette)
        self.messages.launch()

        # click new message
        new_message = self.messages.tap_create_new_message()
        new_message.type_phone_number(self.testvars['carrier']['phone_number'])

        new_message.type_message(_text_message_content)

        #click send
        message_thread = new_message.tap_send()
        message_thread.wait_for_received_messages()
        message_thread.edit_message()
        message_thread.editmessage.select_all_messages()
        confirm = message_thread.editmessage.delete_selected_messages()
        confirm.delete_confirmation()
