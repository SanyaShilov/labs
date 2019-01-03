import widgets


class ContentSignIn(widgets.Content):
    def __init__(self, view):
        super().__init__()
        self.login_lineedit = widgets.LineEdit(
            '', self, 400, 100, 400, 100,
        )
        self.login_lineedit.setPlaceholderText('Login')
        self.password_lineedit = widgets.LineEdit(
            '', self, 400, 100, 400, 300,
        )
        self.password_lineedit.setEchoMode(self.password_lineedit.Password)
        self.password_lineedit.setPlaceholderText('Password')
        self.sign_in_btn = widgets.PushButton(
            'Sign In', self, 400, 100, 400, 500,
            view.show_content_main
        )
        self.go_back_btn = widgets.PushButton(
            'Go Back', self, 400, 100, 400, 700,
            view.go_back
        )
