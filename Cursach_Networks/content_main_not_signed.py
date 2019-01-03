import widgets


class ContentMainNotSigned(widgets.Content):
    def __init__(self, view):
        super().__init__()
        self.sign_in_btn = widgets.PushButton(
            'Sign In', self, 400, 100, 400, 100,
            view.go(view.show_content_sign_in, view.show_content_main_not_signed)
        )
        self.register_btn = widgets.PushButton(
            'Register', self, 400, 100, 400, 300,
            view.go(view.show_content_register, view.show_content_main_not_signed)
        )
        self.champions_btn = widgets.PushButton(
            'Champions', self, 400, 100, 400, 500,
            view.go(view.show_content_champions, view.show_content_main_not_signed)
        )
