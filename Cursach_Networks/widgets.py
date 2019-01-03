from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QPushButton,QTableWidget, QTableWidgetItem,
                             QMessageBox, QComboBox, QTextEdit, QHBoxLayout)

import view

general_font = QFont('Times New Roman', 24, 1)
title_font = QFont('Times New Roman', 24, 1)


def base_init (self, base_cls, string, parent) :
    if isinstance(string, str) :
        base_cls.__init__(self, string, parent)
    elif isinstance(string, QWidget):
        base_cls.__init__(self, string)
    else :
        base_cls.__init__(self, parent)


def yes_no (boolean) :
    if boolean :
        return 'Yes'
    else :
        return 'No'


class Content (QWidget):
    def __init__ (self):
        super().__init__()


class Header (QWidget) :
    def __init__ (self) :
        super().__init__()

        self.hbox = QHBoxLayout(self)
        self.hbox.addStretch(0)

    def add (self, btn) :
        self.hbox.addWidget(btn)


class PushButton (QPushButton) :
    def __init__ (self, string = '', parent = None,
                  width = None, height = None,
                  pos_x = None, pos_y = None,
                  slot = None) :
        base_init(self, QPushButton, string, parent)
        self.setFont(general_font)
        if width is not None and height is not None :
            self.setFixedSize(width, height)
        if pos_x is not None and pos_y is not None :
            self.move(pos_x, pos_y)
        if slot is not None :
            self.clicked.connect(slot)


class TaskButton (PushButton) :
    def __init__ (self, string = '', parent = None,
                  width = None, height = None,
                  pos_x = None, pos_y = None,
                  task = None) :
        self.task = task
        PushButton.__init__(self, string, parent, width, height, pos_x, pos_y,
                            self.push)

    def push (self) :
        presenter.Presenter().current_task = self.task
        view.View().show_content_task()


class ProposedTaskButton (PushButton) :
    def __init__ (self, string = '', parent = None,
                  width = None, height = None,
                  pos_x = None, pos_y = None,
                  task = None, solved = False) :
        self.task = task
        PushButton.__init__(self, string, parent, width, height, pos_x, pos_y,
                            self.push)

    def push (self) :
        presenter.Presenter().current_proposed_task = self.task
        view.View().show_content_publish()


class Label (QLabel) :
    def __init__ (self, string = '', parent = None,
                  width = None, height = None,
                  pos_x = None, pos_y = None,
                  alignment = None, font = general_font) :
        base_init(self, QLabel, string, parent)
        self.setFont(font)
        if width is not None and height is not None :
            self.setFixedSize(width, height)
        if pos_x is not None and pos_y is not None :
            self.move(pos_x, pos_y)
        if alignment is not None :
            self.setAlignment(alignment)


class TextEdit (QTextEdit) :
    def __init__ (self, string = '', parent = None,
                  width = None, height = None,
                  pos_x = None, pos_y = None) :
        base_init(self, QTextEdit, string, parent)
        self.setFont(general_font)
        if width is not None and height is not None :
            self.setFixedSize(width, height)
        if pos_x is not None and pos_y is not None :
            self.move(pos_x, pos_y)


class LineEdit (QLineEdit) :
    def __init__ (self, string = '', parent = None,
                  width = None, height = None,
                  pos_x = None, pos_y = None) :
        base_init(self, QLineEdit, string, parent)
        self.setFont(general_font)
        if width is not None and height is not None :
            self.setFixedSize(width, height)
        if pos_x is not None and pos_y is not None :
            self.move(pos_x, pos_y)


class List (QComboBox) :
    def __init__ (self, parent = None,
                  width = None, height = None,
                  pos_x = None, pos_y = None) :
        super().__init__(parent)
        self.setFont(general_font)
        if width is not None and height is not None :
            self.setFixedSize(width, height)
        if pos_x is not None and pos_y is not None :
            self.move(pos_x, pos_y)


class MessageBox (QMessageBox) :
    pass


class Item (QTableWidgetItem) :
    def __init__ (self, *args, **kwargs) :
        super().__init__(*args, **kwargs)
        self.setFlags(self.flags() & (~ Qt.ItemIsEditable))


class Table (QTableWidget) :
    def __init__ (self, parent = None,
                  width = None, height = None,
                  pos_x = None, pos_y = None) :
        super().__init__(parent)
        self.setFont(general_font)
        if width is not None and height is not None :
            self.setFixedSize(width, height)
        if pos_x is not None and pos_y is not None :
            self.move(pos_x, pos_y)


class Pagination (QWidget) :
    def __init__ (self, n, parent = None) :
        super().__init__(parent)

        self.object = None

        self.setFixedSize(250, 20)

        self.first_btn = PushButton('1', self, 50, 20, 0, 0, self.push_first)
        self.prev_btn = PushButton('<<', self, 50, 20, 50, 0, self.push_prev)
        self.index_lbl = Label('1', self, 50, 20, 100, 0, Qt.AlignCenter)
        self.next_btn = PushButton('>>', self, 50, 20, 150, 0, self.push_next)
        self.last_btn = PushButton(str(n), self, 50, 20, 200, 0, self.push_last)

        self.init(n)
        
    def init (self, n) :
        self.index = 0
        self.len = n

        self.last_btn.setText(str(self.len))

        self.prev_btn.setEnabled(self.index != 0)
        self.next_btn.setEnabled(self.index != self.len - 1)

    def set_paginating_object (self, obj) :
        self.object = obj

    def push_first (self) :
        self.index = 0
        self.paginate()

    def push_prev (self) :
        self.index -= 1
        self.paginate()

    def push_next (self) :
        self.index += 1
        self.paginate()

    def push_last (self) :
        self.index = self.len - 1
        self.paginate()

    def paginate (self) :
        self.prev_btn.setEnabled(self.index != 0)
        self.next_btn.setEnabled(self.index != self.len - 1)
        
        self.index_lbl.setText(str(self.index + 1))
        if self.object is not None :
            self.object.paginate(self.index)

class TasksTable (QWidget) :
    def __init__ (self, parent = None) :
        super().__init__(parent)

        self.setStyleSheet("border : 1px solid #6c6c6c; background-color : white")

        self.order_by = 'TaskID'
        self.order = 'ASC'
        self.solved_by_you = 'ALL'
        self.get_content()
        
        self.on_one_page = 20
        self.current_page = 0
        
        self.len = len(self.tasks)
        self.pages = max((self.len - 1) // self.on_one_page + 1, 1)

        self.pagination = Pagination(self.pages, self)
        self.pagination.move(0, 0)
        self.pagination.set_paginating_object(self)
        
        self.id_btns = []
        self.title_btns = []
        self.difficulty_lbls = []
        self.solved_by_lbls = []
        self.solved_by_you_lbls = []

        self.sort_id_acs_btn = PushButton('ACS', self, 100, 25, 0, 50, self.sort_id_asc)
        self.sort_difficulty_acs_btn = PushButton('ACS', self, 100, 25, 600, 50, self.sort_difficulty_asc)
        self.sort_solved_by_acs_btn = PushButton('ACS', self, 100, 25, 700, 50, self.sort_solved_by_asc)
        self.all_btn = PushButton('ALL', self, 100, 25, 800, 50, self.show_all)

        self.id_lbl = Label('ID', self, 100, 50, 0, 75, Qt.AlignCenter)
        self.title_lbl = Label('Title', self, 500, 100, 100, 50, Qt.AlignCenter)
        self.difficulty_lbl = Label('Difficulty', self, 100, 50, 600, 75, Qt.AlignCenter)
        self.solved_by_lbl = Label('Solved by', self, 100, 50, 700, 75, Qt.AlignCenter)
        self.solved_by_you_lbl = Label('Solved by\nyou', self, 100, 50, 800, 75, Qt.AlignCenter)

        self.sort_id_desc_btn = PushButton('DESC', self, 100, 25, 0, 125, self.sort_id_desc)
        self.sort_difficulty_desc_btn = PushButton('DESC', self, 100, 25, 600, 125, self.sort_difficulty_desc)
        self.sort_solved_by_desc_btn = PushButton('DESC', self, 100, 25, 700, 125, self.sort_solved_by_desc)
        self.solved_btn = PushButton('YES', self, 50, 25, 800, 125, self.show_solved)
        self.not_solved_btn = PushButton('NO', self, 50, 25, 850, 125, self.show_not_solved)
        
        for i in range(self.on_one_page) :
            try :
                task = self.tasks[i]
                solved = self.solved[i]
                self.id_btns.append(TaskButton(str(task.id), self,
                                               100, 20, 0, 150 + i * 20, task))
                self.title_btns.append(TaskButton(task.title, self,
                                               500, 20, 100, 150 + i * 20, task))
                self.difficulty_lbls.append(Label(str(task.difficulty), self,
                                               100, 20, 600, 150 + i * 20, Qt.AlignCenter))
                self.solved_by_lbls.append(Label(str(task.solved_by), self,
                                               100, 20, 700, 150 + i * 20, Qt.AlignCenter))
                self.solved_by_you_lbls.append(Label(solved, self,
                                               100, 20, 800, 150 + i * 20, Qt.AlignCenter))
            except :
                self.id_btns.append(TaskButton('', self,
                                               100, 20, 0, 150 + i * 20, None))
                self.title_btns.append(TaskButton('', self,
                                               500, 20, 100, 150 + i * 20, None))
                self.difficulty_lbls.append(Label('', self,
                                               100, 20, 600, 150 + i * 20, Qt.AlignCenter))
                self.solved_by_lbls.append(Label('', self,
                                               100, 20, 700, 150 + i * 20, Qt.AlignCenter))
                self.solved_by_you_lbls.append(Label('', self,
                                               100, 20, 800, 150 + i * 20, Qt.AlignCenter))

        self.pagination.push_first()

    def get_content (self) :
        self.tasks, self.solved = presenter.Presenter().tasks_content(self.order_by, self.order, self.solved_by_you)

    def reload (self) :
        self.get_content()
        self.resize()

    def resize (self) :
        self.len = len(self.tasks)
        self.pages = max((self.len - 1) // self.on_one_page + 1, 1)

        self.pagination.init(self.pages)
        self.pagination.push_first()

    def paginate (self, index) :
        self.current_page = index
        start = self.current_page * self.on_one_page
        end = min(start + self.on_one_page, self.len)

        for i in range(start, end) :
            ind = i % self.on_one_page
            task = self.tasks[i]
            solved = self.solved[i]
            
            self.id_btns[ind].setText(str(task.id))
            self.id_btns[ind].task = task
            self.title_btns[ind].setText(task.title)
            self.title_btns[ind].task = task
            self.difficulty_lbls[ind].setText(str(task.difficulty))
            self.solved_by_lbls[ind].setText(str(task.solved_by))
            self.solved_by_you_lbls[ind].setText(solved)

            self.id_btns[ind].show()
            self.title_btns[ind].show()
            self.difficulty_lbls[ind].show()
            self.solved_by_lbls[ind].show()
            self.solved_by_you_lbls[ind].show()

        for i in range(end, start + self.on_one_page) :
            ind = i % self.on_one_page
            
            self.id_btns[ind].hide()
            self.title_btns[ind].hide()
            self.difficulty_lbls[ind].hide()
            self.solved_by_lbls[ind].hide()
            self.solved_by_you_lbls[ind].hide()

    def sort_id_asc (self) :
        self.order_by = 'TaskID'
        self.order = 'ASC'
        self.reload()

    def sort_id_desc (self) :
        self.order_by = 'TaskID'
        self.order = 'DESC'
        self.reload()

    def sort_difficulty_asc (self) :
        self.order_by = 'Difficulty'
        self.order = 'ASC'
        self.reload()

    def sort_difficulty_desc (self) :
        self.order_by = 'Difficulty'
        self.order = 'DESC'
        self.reload()

    def sort_solved_by_asc (self) :
        self.order_by = 'SolvedBy'
        self.order = 'ASC'
        self.reload()

    def sort_solved_by_desc (self) :
        self.order_by = 'SolvedBy'
        self.order = 'DESC'
        self.reload()

    def show_all (self) :
        self.solved_by_you = 'ALL'
        self.reload()

    def show_solved (self) :
        self.solved_by_you = 'YES'
        self.reload()
   
    def show_not_solved (self) :
        self.solved_by_you = 'NO'
        self.reload()

class ProposedTasksTable (QWidget) :
    def __init__ (self, parent = None) :
        super().__init__(parent)

        self.setStyleSheet("border : 1px solid #6c6c6c; background-color : white")

        self.order_by = 'ProposedTaskID'
        self.order = 'ASC'
        self.get_content()
        
        self.on_one_page = 20
        self.current_page = 0
        
        self.len = len(self.tasks)
        self.pages = max((self.len - 1) // self.on_one_page + 1, 1)

        self.pagination = Pagination(self.pages, self)
        self.pagination.move(0, 0)
        self.pagination.set_paginating_object(self)
        
        self.id_btns = []
        self.title_btns = []
        self.difficulty_lbls = []

        self.sort_id_acs_btn = PushButton('ACS', self, 100, 25, 0, 50, self.sort_id_asc)
        self.sort_difficulty_acs_btn = PushButton('ACS', self, 100, 25, 600, 50, self.sort_difficulty_asc)

        self.id_lbl = Label('ID', self, 100, 50, 0, 75, Qt.AlignCenter)
        self.title_lbl = Label('Title', self, 500, 100, 100, 50, Qt.AlignCenter)
        self.difficulty_lbl = Label('Difficulty', self, 100, 50, 600, 75, Qt.AlignCenter)

        self.sort_id_desc_btn = PushButton('DESC', self, 100, 25, 0, 125, self.sort_id_desc)
        self.sort_difficulty_desc_btn = PushButton('DESC', self, 100, 25, 600, 125, self.sort_difficulty_desc)
        
        for i in range(self.on_one_page) :
            try :
                task = self.tasks[i]
                solved = self.solved[i]
                self.id_btns.append(ProposedTaskButton(str(task.id), self,
                                               100, 20, 0, 150 + i * 20, task))
                self.title_btns.append(ProposedTaskButton(task.title, self,
                                               500, 20, 100, 150 + i * 20, task))
                self.difficulty_lbls.append(Label(str(task.difficulty), self,
                                               100, 20, 600, 150 + i * 20, Qt.AlignCenter))
            except :
                self.id_btns.append(ProposedTaskButton('', self,
                                               100, 20, 0, 150 + i * 20, None))
                self.title_btns.append(ProposedTaskButton('', self,
                                               500, 20, 100, 150 + i * 20, None))
                self.difficulty_lbls.append(Label('', self,
                                               100, 20, 600, 150 + i * 20, Qt.AlignCenter))

        self.pagination.push_first()

    def get_content (self) :
        self.tasks = presenter.Presenter().proposed_tasks_content(self.order_by, self.order)

    def reload (self) :
        self.get_content()
        self.pagination.push_first()

    def paginate (self, index) :
        self.current_page = index
        start = self.current_page * self.on_one_page
        end = min(start + self.on_one_page, self.len)

        for i in range(start, end) :
            ind = i % self.on_one_page
            task = self.tasks[i]
            
            self.id_btns[ind].setText(str(task.id))
            self.id_btns[ind].task = task
            self.title_btns[ind].setText(task.title)
            self.title_btns[ind].task = task
            self.difficulty_lbls[ind].setText(str(task.difficulty))

            self.id_btns[ind].show()
            self.title_btns[ind].show()
            self.difficulty_lbls[ind].show()

        for i in range(end, start + self.on_one_page) :
            ind = i % self.on_one_page
            
            self.id_btns[ind].hide()
            self.title_btns[ind].hide()
            self.difficulty_lbls[ind].hide()

    def sort_id_asc (self) :
        self.order_by = 'ProposedTaskID'
        self.order = 'ASC'
        self.reload()

    def sort_id_desc (self) :
        self.order_by = 'ProposedTaskID'
        self.order = 'DESC'
        self.reload()

    def sort_difficulty_asc (self) :
        self.order_by = 'Difficulty'
        self.order = 'ASC'
        self.reload()

    def sort_difficulty_desc (self) :
        self.order_by = 'Difficulty'
        self.order = 'DESC'
        self.reload()
