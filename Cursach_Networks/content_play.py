import widgets


class ContentPlay(widgets.Content):
    def __init__(self, app):
        super().__init__(app)
        self.waiting_lbl = widgets.Label(
            'Play!', self, 400, 100, 400, 100, alignment='center'
        )
        self.give_up_btn = widgets.PushButton(
            'Go Back', self, 400, 100, 400, 250,
            app.send_give_up
        )
