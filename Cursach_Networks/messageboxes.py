import widgets


YES = widgets.MessageBox.Yes
NO = widgets.MessageBox.No
OK = widgets.MessageBox.Ok


def sure_to_give_up():
    return widgets.MessageBox(
        title='Give up',
        text='Are you sure? You will automatically loose this game',
        standard_buttons=YES | NO,
        default_button=NO
    ).exec()


def opponent_give_up():
    return widgets.MessageBox(
        title='Win',
        text='You win! Your opponent give up',
        standard_buttons=OK,
        default_button=OK
    ).exec()


def loose():
    return widgets.MessageBox(
        title='Loose',
        text='You loose!',
        standard_buttons=OK,
        default_button=OK
    ).exec()


def win():
    return widgets.MessageBox(
        title='Win',
        text='You win!',
        standard_buttons=OK,
        default_button=OK
    ).exec()
