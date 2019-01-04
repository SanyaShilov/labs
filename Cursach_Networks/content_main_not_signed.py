import widgets


class ContentMainNotSigned(widgets.Content):
    def __init__(self, app):
        super().__init__(app)
        self.sign_in_btn = widgets.PushButton(
            'Sign In', self, 400, 100, 400, 100,
            app.go(app.show_content_sign_in, app.show_content_main_not_signed)
        )
        self.register_btn = widgets.PushButton(
            'Register', self, 400, 100, 400, 250,
            app.go(app.show_content_register, app.show_content_main_not_signed)
        )
        self.champions_btn = widgets.PushButton(
            'Champions', self, 400, 100, 400, 400,
            app.go(app.show_content_champions, app.show_content_main_not_signed)
        )
