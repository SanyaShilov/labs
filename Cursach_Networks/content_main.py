import widgets
import view


class ContentMain(widgets.Content):
    def __init__(self):
        super().__init__()
        self.play_btn = widgets.PushButton(
            'Play', self, 400, 100, 400, 100,
        )
        self.sign_out_btn = widgets.PushButton(
            'Sign Out', self, 400, 100, 400, 300,
        )
        self.champions_btn = widgets.PushButton(
            'Champions', self, 400, 100, 400, 500, view.View().show_content_champions
        )
