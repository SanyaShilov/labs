import widgets


class ContentWaiting(widgets.Content):
    def __init__(self, app):
        super().__init__(app)
        self.waiting_lbl = widgets.Label(
            'Please, wait...', self, 400, 100, 400, 100, alignment='center'
        )
        self.go_back_btn = widgets.PushButton(
            'Go Back', self, 400, 100, 400, 250,
            app.go_back
        )
