import widgets


YES = widgets.MessageBox.Yes
NO = widgets.MessageBox.No
OK = widgets.MessageBox.Ok


def sure_to_give_up(app):
    messagebox = widgets.MessageBox(app)
    messagebox.setWindowTitle('Give up')
    messagebox.setInformativeText('Are you sure? You will automatically loose this game')
    messagebox.setStandardButtons(widgets.MessageBox.Yes |
                                       widgets.MessageBox.No)
    messagebox.setDefaultButton(widgets.MessageBox.No)
    return messagebox.exec()


def opponent_give_up(app):
    messagebox = widgets.MessageBox(app)
    messagebox.setWindowTitle('Win')
    messagebox.setInformativeText('You win! Your opponent gave up')
    messagebox.setStandardButtons(widgets.MessageBox.Ok)
    messagebox.setDefaultButton(widgets.MessageBox.Ok)
    return messagebox.exec()
