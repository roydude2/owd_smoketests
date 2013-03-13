loading_overlay      = ('id', 'loading-overlay')
app_head_specific    = "//h1[text()='%s']"
app_head             = ('tag name', "h1")
status_bar           = ('id', 'statusbar')
status_bar_new       = ('xpath', "//*[@id='statusbar-notification'][@data-unread='true']")
status_bar_count     = ('xpath', "//*[@id='desktop-notifications-container']/div")
homescreen_iframe    = ('css selector', 'div.homescreen iframe')
home_frame_locator   = ('css selector', 'iframe[src="app://homescreen.gaiamobile.org/index.html#root"]')
app_icon_css         = 'li.icon[aria-label="%s"]'
app_delete_icon      = ('css selector', 'span.options')
#app_delete_icon      = ('xpath', './/span[@class="options"]')
app_confirm_delete   = ('id', 'confirm-dialog-confirm-button')
app_titlebar_name    = ('class name', 'titlebarIcon')