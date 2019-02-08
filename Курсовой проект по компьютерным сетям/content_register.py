import widgets


class ContentRegister(widgets.Content):
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
        self.register_btn = widgets.PushButton(
            'Register', self, 400, 100, 400, 400,
            self.register
        )
        self.go_back_btn = widgets.PushButton(
            'Go Back', self, 400, 100, 400, 550,
            app.go_back
        )

    def register(self):
        login = self.login_lineedit.text()
        password = self.password_lineedit.text()
        self.app.send_register(login, password)
