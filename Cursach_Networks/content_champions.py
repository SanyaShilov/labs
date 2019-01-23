import widgets


class ContentChampions(widgets.Content):
    def __init__(self, app):
        super().__init__(app)
        self.table = widgets.Table(
            self, 822, 400, 200, 100
        )
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ('login', 'wins', 'looses', 'games')
        )
        for i in range(4):
            self.table.setColumnWidth(i, 200)
        for i, champion in enumerate(self.app.champions):
            self.table.insertRow(i)
            for j, field in enumerate(['login', 'wins', 'looses', 'games']):
                self.table.setItem(i, j, widgets.Item(str(champion[field])))
        self.go_back_btn = widgets.PushButton(
            'Go Back', self, 400, 100, 400, 550,
            app.go_back
        )
