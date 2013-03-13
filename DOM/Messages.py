frame_locator          = ('src', 'app://sms.gaiamobile.org/index.html')
statusbar_new_sms      = ('xpath', './/*[@id="desktop-notifications-container"]//div[contains(text(), "%s")]')
statusbar_all_notifs   = ".//*[@id='desktop-notifications-container']/div[%s]"
create_new_message_btn = ('id', 'icon-add')
target_number          = ('id', 'receiver-input')
input_message_area     = ('id', 'message-to-send')
send_message_button    = ('id', 'send-message')
message_sending_spinner= ('css selector', "img[src='style/images/spinningwheel_small_animation.gif']")
header_back_button     = ('xpath', '//header/a[1]')
unread_message         = ('css selector', 'li > a.unread')
messages_from_num      = "//*[contains(@id, '%s')]"
received_messages      = ('xpath', "//li[@class='bubble'][a[@class='received']]")
