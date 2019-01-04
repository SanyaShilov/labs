import widgets


class ContentSignIn(widgets.Content):
    def __init__(self, app):
        super().__init__(app)
        self.login_lineedit = widgets.LineEdit(
            '', self, 400, 100, 400, 100,
        )
        self.login_lineedit.setPlaceholderText('Login')
        self.password_lineedit = widgets.LineEdit(
            '', self, 400, 100, 400, 250,
        )
        self.password_lineedit.setEchoMode(self.password_lineedit.Password)
        self.password_lineedit.setPlaceholderText('Password')
        self.sign_in_btn = widgets.PushButton(
            'Sign In', self, 400, 100, 400, 400,
            self.sign_in
        )
        self.go_back_btn = widgets.PushButton(
            'Go Back', self, 400, 100, 400, 550,
            app.go_back
        )

    def sign_in(self):
        login = self.login_lineedit.text()
        password = self.password_lineedit.text()
        self.app.sign_in(login, password)
