from royTools import DOMS
import time

class main():
    
    #
    # When you create your instance of this class, include the
    # "self" object so we can access the calling class' objects.
    #
    def __init__(self, p_parentSelf, p_testUtils):
        self.testUtils  = p_testUtils
        self.marionette = p_parentSelf.marionette
        self.parent     = p_parentSelf

    def launch(self):
        self.app = self.parent.apps.launch('Gallery')
        self.parent.wait_for_element_not_displayed(*DOMS.GLOBAL.loading_overlay)

    def clickThumb(self, p_num, p_type):
        self.parent.wait_for_element_displayed(*DOMS.Gallery.items)
        all_items = self.marionette.find_elements(*DOMS.Gallery.items)
        my_item = all_items[p_num]
        self.marionette.tap(my_item)
        
        if p_type.lower() == "vid":
            self.parent.wait_for_element_displayed(*DOMS.Gallery.current_image_vid)
        else:
            self.parent.wait_for_element_displayed(*DOMS.Gallery.current_image_pic)

    def playCurrentVideo(self):
        self.parent.wait_for_element_displayed(*DOMS.Gallery.video_play_button)
        playBTN = self.marionette.find_element(*DOMS.Gallery.video_play_button)
        playBTN.click()
        self.marionette.tap(playBTN)
        self.parent.wait_for_element_not_displayed(*DOMS.Gallery.video_pause_button)
