from transitions.extensions import GraphMachine

import utils


class TocMachine(GraphMachine):

    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_create_db(self, event):
        return True
    def is_going_to_image_choose(self, event):
        text = event.message.text
        return text == "我現在想吃..."
    def is_going_to_image_watch(self, event):
        return True
    def is_going_to_recommand(self, event):
        text = event.message.text
        return text == "小幫手推薦..."
    def is_going_to_record_choose(self, event):
        text = event.message.text
        return text == "紀錄一下我吃了什麼"
    def is_going_to_record(self, event):
        return True
    def is_going_to_record_watch(self, event):
        text = event.message.text
        return text == "看看過去我吃了什麼"


    def on_enter_create_db(self, event):
        print("I'm entering create_db")
        #utils.create_table()
        if ( utils.send_guide_flex(event.reply_token) ) == False :
            utils.send_text_message(event.reply_token, "ＱＱ請輸入任意鍵繼續")
        self.go_to_ready()
    def on_enter_image_choose(self, event):
        print("I'm entering image_choose")
        if ( utils.send_ask_image_flex(event.reply_token) ) == False :
            utils.send_text_message(event.reply_token, "ＱＱ請輸入任意鍵繼續")
        self.go_to_image()
    def on_enter_image_watch(self, event):
        print("I'm entering image_watch")
        target = event.message.text
        if ( utils.send_image_flex(event.reply_token, target) ) == False :
            utils.send_text_message(event.reply_token, "沒有找到圖片ＱＱ")
        self.go_back()
    def on_enter_recommand(self, event):
        print("I'm entering recommand")
        utils.send_and_recommand(event)
        self.go_back()
    def on_enter_record_choose(self, event):
        print("I'm entering record_choose")
        if ( utils.send_ask_record_flex(event.reply_token) ) == False :
            utils.send_text_message(event.reply_token, "ＱＱ請輸入任意鍵繼續")
        self.go_to_record()
    def on_enter_record(self, event):
        print("I'm entering record")
        utils.send_and_record(event)
        self.go_back()
    def on_enter_record_watch(self, event):
        print("I'm entering record_watch")
        utils.send_and_watch_record(event)
        self.go_back()

    def on_exit_create_db(self):
        print("Leaving create_db")
    def on_exit_image_choose(self):
        print("Leaving image_choose")
    def on_exit_image_watch(self):
        print("Leaving image_watch")
    def on_exit_recommand(self):
        print("Leaving recommand")
    def on_exit_record_choose(self):
        print("Leaving record_choose")
    def on_exit_record(self):
        print("Leaving record")
    def on_exit_record_watch(self):
        print("Leaving record_watch")
