class GLOBAL():
    loading_overlay      = ('id', 'loading-overlay')
    app_head_specific    = "//h1[text()='%s']"
    app_head             = ('xpath', "//h1")
    status_bar           = ('id', 'statusbar')
    status_bar_new       = ('xpath', "//*[@id='statusbar-notification'][@data-unread='true']")
    status_bar_count     = ('xpath', "//*[@id='desktop-notifications-container']/div")
    homescreen_iframe    = ('css selector', 'div.homescreen iframe')
    home_frame_locator   = ('css selector', 'iframe[src="app://homescreen.gaiamobile.org/index.html#root"]')
    app_icon_css         = 'li.icon[aria-label="%s"]'
    app_delete_icon      = ('css selector', 'span.options')
    app_confirm_delete   = ('id', 'confirm-dialog-confirm-button')

class Statusbar():
    wifi            = ('id', 'statusbar-wifi')
    dataConn        = ('id', 'statusbar-data')

class Contacts():
    frame_locator          = ('css selector', 'iframe[src="app://communications.gaiamobile.org/index.html"]')
    view_all_header        = ('xpath', GLOBAL.app_head_specific % 'Contacts')
    add_contact_button     = ('id', 'add-contact-button')
    add_contact_header     = ('xpath', GLOBAL.app_head_specific % 'Add contact')
    view_details_title     = ('id', 'contact-form-title')
    details_back_button    = ('id', 'details-back')

    edit_contact_header    = ('xpath', GLOBAL.app_head_specific % 'Edit contact')
    edit_update_button     = ('id', 'save-button')
    edit_details_button    = ('id', 'edit-contact-button')
    done_button            = ('id', 'save-button')

    given_name_field       = ('id', 'givenName')
    family_name_field      = ('id', 'familyName')
    email_field            = ('id', "email_0")
    phone_field            = ('id', "number_0")
    street_field           = ('id', "streetAddress_0")
    zip_code_field         = ('id', "postalCode_0")
    city_field             = ('id', 'locality_0')
    country_field          = ('id', 'countryName_0')
    comment_field          = ('id', 'note_0')
    sms_button             = ('id', 'send-sms-button-0')

class Messages():
    frame_locator          = ('css selector', 'iframe[src="app://sms.gaiamobile.org/index.html"]')
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

class Camera():
    capture_button           = ('id', 'capture-button')
    thumbnail                = ('class name', 'thumbnail')
    thumbnail_preview_marker = ('id', 'preview')
    switch_source_btn        = ('id', 'switch-button')
    capture_button_enabled   = ('css selector', '#capture-button:not([disabled])')
    video_timer              = ('id', 'video-timer')
    video_play_button        = ('xpath', "//button[@class='videoPlayerPlayButton']")
    video_pause_button       = ('xpath', "//button[@class='videoPlayerPauseButton']")
    
class Gallery():
    thumbnail_items         = ('css selector', 'li.thumbnail')
    thumbnail_list_section  = ('id', 'thumbnail-list-view')
    current_image_pic       = ('css selector', '#frame2 > img')
    current_image_vid       = ('xpath', "//*[@id='frame2']/div")
    video_play_button       = ('xpath', "//*[@id='frame2']/div/button")
    video_pause_button      = ('xpath', "//*[@id='frame2']/div/div/button")
    fullscreen_back_button  = ('id', 'fullscreen-back-button')

class Video():
    items                   = ('xpath', "//*[@id='thumbnails']/li/div/div[3]")
    thumb_durations         = ('xpath', "//*[@id='thumbnails']/li/div/div[3]/span[13]/span")
    video_frame             = ('id', 'videoFrame')
    video_loaded            = ('css selector', 'video[style]')

class Phone():
    frame_locator          = ('css selector', 'iframe[src="app://communications.gaiamobile.org/index.html"]')
    
class Settings():
    frame_locator          = ('css selector', 'iframe[src="app://settings.gaiamobile.org/index.html#root"]')
    settings_header        = ('xpath', GLOBAL.app_head_specific % 'Settings')
    back_button            = ('class name', 'icon icon-back')

    app_permissions        = ('id', "menuItem-appPermissions")
    app_permissions_header = ('xpath', GLOBAL.app_head_specific % 'App permissions')
    app_perm_camera        = ('xpath', './/*[@id="appPermissions"]//a[text()="Camera"]')
    app_perm_camera_geo    = ('xpath', './/*[@id="appPermissions-details"]//span[text()="Geolocation"]/select') 

    wifi                   = ('id', 'menuItem-wifi')
    wifi_header            = ('xpath', GLOBAL.app_head_specific % 'Wi-Fi')
    wifi_enabled           = ('xpath', ".//*[@id='wifi-enabled']/label")
    wifi_available_networks= ('xpath', ".//*[@id='wifi-availableNetworks']/li")
    wifi_available_status  = ".//*[@id='wifi-availableNetworks']/li[%s]//small"
    wifi_available_name    = ".//*[@id='wifi-availableNetworks']/li[%s]//a"
    wifi_name_xpath        = './/*[@id="wifi-availableNetworks"]/li//a[text()="%s"]'
    wifi_login_user        = ('name', 'identity')
    wifi_login_pass        = ('name', 'password')
    wifi_login_ok_btn      = ('xpath', ".//*[@id='wifi-joinHidden']/header/menu/button")
    wifi_connected         = ('xpath', './/*[text()="Connected"]')
    
    cellData               = ('id', 'menuItem-cellularAndData')
    celldata_header        = ('xpath', GLOBAL.app_head_specific % 'Cellular & Data')
    celldata_DataConn      = ('xpath', ".//*[@id='carrier']/ul[2]/li[1]/label")
    celldata_DataConn_ON   = ('id', 'dataConnection-expl')

class Browser():
    frame_locator           = ('css selector', 'iframe[src="app://browser.gaiamobile.org/index.html"]')
    url_input               = ('id', 'url-input')
    url_go_button           = ('id', 'url-button')
    throbber                = ("id", "throbber")
    
    browser_page_frame      = ('css selector', 'iframe[mozbrowser]')
    page_title              = ('xpath', ".//*[@id='results']/ul//h5[text()='Problemloadingpage']")

class Market():
    search_query            = ('id', 'search-q')
    featured_apps           = ('xpath', ".//*[@id='featured-home']/ul/li/a/canvas")
    install_button          = ('css selector', '.button.product.install')
    app_details_header      = ('xpath', '//h3')
    confirm_install_button  = ('id', 'app-install-install-button')
    
class Email():
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
    #settings_del_conf_btn   = ('id', 'account-delete-ok')
    settings_del_conf_btn   = ('xpath', './/*[text()="Cancel"]')
    settings_add_account_btn= ('class name', 'tng-account-add')

    goto_accounts_btn       = ('class name', 'fld-accounts-btn')    
    accounts_list_names     = ('class name', 'fld-account-name')
    
    folderList_header       = ('class name', 'fld-folders-header-account-label')
    folderList_folders      = ('class name', 'fld-folder-name')
    
    folder_message_list     = ('class name', 'msg-header-item') #'msg-header-details-section')
    folder_subject_list     = ('class name', 'msg-header-subject')
    
    open_email_from         = ('xpath', "//*[@id='cards']/div[3]/div[1]/div[1]/div[2]/div/span")
    open_email_to           = ('xpath', "//*[@id='cards']/div[3]/div[1]/div[1]/div[3]/div[1]/div/span")
    open_email_subject      = ('class name', 'msg-envelope-subject')
    
class Calculator():
    display         = ('id', 'display')
    button_mutiply  = ('id', 'multiply')
    button_divide   = ('id', 'divide')
    button_add      = ('id', 'add')
    button_subtract = ('id', 'subtract')
    button_cancel   = ('xpath', "//input[@value='C']")
    button_equals   = ('xpath', "//input[@value='=']")
    button_1        = ('xpath', "//input[@value='1']")
    button_2        = ('xpath', "//input[@value='2']")
    button_3        = ('xpath', "//input[@value='3']")
    button_4        = ('xpath', "//input[@value='4']")
    button_5        = ('xpath', "//input[@value='5']")
    button_6        = ('xpath', "//input[@value='6']")
    button_7        = ('xpath', "//input[@value='7']")
    button_8        = ('xpath', "//input[@value='8']")
    button_9        = ('xpath', "//input[@value='9']")
    button_0        = ('xpath', "//input[@value='0']")
    button_point    = ('xpath', "//input[@value='.']")

class FTU():
    language_list       = ('xpath', ".//*[@id='languages']/article/ul/li/label/p")
    language_Sel_xpath  = '//li[ starts-with( descendant-or-self::*/text(),"%s" ) ]'
    next_button         = ('id', 'forward')

    section_cell_data   = ('id', 'data_3g')
    #data_connection     = ('id', 'data-connection-switch')
    dataconn_switch     = ('xpath', '//li/aside[ starts-with( descendant-or-self::*/@id,"data-connection-switch" ) ]')

    wifi_networks_list  = ('css selector', 'ul#networks li')
    wifi_login_user     = ('id', 'wifi_user')
    wifi_login_pass     = ('id', 'wifi_password')
    wifi_login_join     = ('id', 'wifi-join-button')

    timezone            = ('id', 'date_and_time')
    timezone_continent  = ('id', 'tz-region')
    timezone_city       = ('id', 'tz-city')
    timezone_title      = ('id', 'time-zone-title')
    
    privacy_email       = ('id', 'newsletter-input')
    
    tour_start_btn      = ('id', 'lets-go-button')
    tour_skip_btn       = ('id', 'skip-tutorial-button')
    tour_next_btn       = ('id', 'forwardTutorial')
    tour_finished_btn   = ('id', 'tutorialFinished')

class EME():
    icons_groups        = ('xpath', ".//*[@id='shortcuts-items']/documentfragment/li")
    back_btn            = ('id', 'button-clear')
