frame_locator           = ('css selector', 'iframe[src="app://email.gaiamobile.org/index.html"]')
username                = ('class name', 'sup-info-name')
email_addr              = ('class name', 'sup-info-email')
password                = ('class name', 'sup-info-password')
login_next_btn          = ('class name', 'sup-info-next-btn')
sup_header              = ('class name', 'sup-account-header-label')
sup_continue_btn        = ('class name', 'sup-show-mail-btn sup-form-btn recommend')

compose_msg_btn         = ('class name', 'msg-compose-btn')
compose_to              = ('class name', 'cmp-to-text cmp-addr-text')
compose_cc              = ('class name', 'cmp-cc-text cmp-addr-text')
compose_bcc             = ('class name', 'cmp-bcc-text cmp-addr-text')
compose_subject         = ('class name', 'cmp-subject-text')
compose_msg             = ('class name', 'cmp-body-text')
compose_send_btn        = ('class name', 'icon icon-send')
compose_send_failed_msg = ('xpath', './/*[text()="Sending email failed"]')

settings_menu_btn       = ('class name', 'icon icon-menu')
settings_set_btn        = ('class name', 'fld-nav-settings-btn bottom-btn')
settings_del_acc_btn    = ('class name', 'tng-account-delete')
settings_del_conf_btn   = ('xpath', './/*[text()="Cancel"]')
settings_add_account_btn= ('class name', 'tng-account-add')

goto_accounts_btn       = ('class name', 'fld-accounts-btn')    
accounts_list_names     = ('class name', 'fld-account-name')

folderList_header       = ('class name', 'fld-folders-header-account-label')
folderList_name_xpath   = '//*[text()="%s"]'

folder_message_list     = ('class name', 'msg-header-item')
folder_subject_list     = ('class name', 'msg-header-subject')
folder_refresh_button   = ("class name", "msg-refresh-btn bottom-btn msg-nonsearch-only")

open_email_from         = ('xpath', "//div[@class='msg-envelope-from-line']//span[@class='msg-peep-content msg-peep-address']")
open_email_to           = ('xpath', "//div[@class='msg-envelope-to-line']//span[@class='msg-peep-content msg-peep-address']")
open_email_subject      = ('class name', 'msg-envelope-subject')
