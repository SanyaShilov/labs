import widgets


class ContentMain(widgets.Content):
    def __init__(self, app):
        super().__init__(app)
        self.play_btn = widgets.PushButton(
            'Play', self, 400, 100, 400, 100,
            app.go(app.send_want_to_play, app.send_dont_want_to_play)
        )
        self.sign_out_btn = widgets.PushButton(
            'Sign Out', self, 400, 100, 400, 250,
            app.send_sign_out
        )
        self.champions_btn = widgets.PushButton(
            'Champions', self, 400, 100, 400, 400,
            self.show_champions
        )

    def show_champions(self):
        self.app.send_show_champions(self.app.show_content_main)
