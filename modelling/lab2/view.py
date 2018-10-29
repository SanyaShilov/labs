from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QLineEdit,
    QTableWidget, QTableWidgetItem, QGridLayout, QWidget, QCheckBox
)
from PyQt5.QtCore import Qt

import criterions
import lcg
import lists


LENGTH = 5000


class Item (QTableWidgetItem) :
    def __init__ (self, *args, editable=False, **kwargs):
        super().__init__(*args, **kwargs)
        if not editable:
            self.setFlags(self.flags() & (~ Qt.ItemIsEditable))


class View(QWidget):
    def __init__(self):
        self.qapp = QApplication([])
        super().__init__()
        self.setWindowTitle(
            'Лабораторная работа №2 по моделированию. '
            'Шилов ИУ7-72'
        )
        self.setGeometry(100, 100, 1800, 500)

        self.ranges = [
            (0, 9),
            (10, 99),
            (100, 999),
        ]

        self.file_lst1 = lists.get_file_list('random1.txt')
        self.file_lst2 = lists.get_file_list('random2.txt')
        self.file_lst3 = lists.get_file_list('random3.txt')

        self.file_lbl = QLabel('табличные значения', self)
        self.file_lbl.setGeometry(300, 0, 360, 50)

        self.file_table = QTableWidget(self)
        self.file_table.setGeometry(200, 50, 360, 350)
        self.file_table.setColumnCount(3)
        self.file_table.setHorizontalHeaderLabels(
            ('0-9', '10-99', '100-999'))
        self.file_table.setColumnWidth(0, 100)
        self.file_table.setColumnWidth(1, 100)
        self.file_table.setColumnWidth(2, 100)

        self.fill_table(self.file_table, [self.file_lst1, self.file_lst2, self.file_lst3])

        self.coef_lbl = QLabel('Коэффициент\nслучайности\nпоследовательности', self)
        self.coef_lbl.setGeometry(25, 350, 200, 200)

        self.coef_lbl1 = QLabel(
            str(round(criterions.common_criterion(
                0, 9, self.file_lst1
            ) * 100, 2)) + '%', self
        )
        self.coef_lbl1.setGeometry(250, 400, 100, 100)
        self.coef_lbl2 = QLabel(
            str(round(criterions.common_criterion(
                10, 99, self.file_lst2
            ) * 100, 2)) + '%', self
        )
        self.coef_lbl2.setGeometry(350, 400, 100, 100)
        self.coef_lbl3 = QLabel(
            str(round(criterions.common_criterion(
                100, 999, self.file_lst3
            ) * 100, 2)) + '%', self
        )
        self.coef_lbl3.setGeometry(450, 400, 100, 100)

        # == #

        self.lcg = lcg.LCG(x0=0, a=84589, c=45989, m=217728)
        self.random_lst1 = lists.get_random_list(self.lcg, 0, 9, LENGTH)
        self.random_lst2 = lists.get_random_list(self.lcg, 10, 99, LENGTH)
        self.random_lst3 = lists.get_random_list(self.lcg, 100, 999, LENGTH)

        self.random_lbl = QLabel('сгенерированные значения', self)
        self.random_lbl.setGeometry(680, 0, 360, 50)

        self.random_table = QTableWidget(self)
        self.random_table.setGeometry(600, 50, 360, 350)
        self.random_table.setColumnCount(3)
        self.random_table.setHorizontalHeaderLabels(
            ('0-9', '10-99', '100-999'))
        self.random_table.setColumnWidth(0, 100)
        self.random_table.setColumnWidth(1, 100)
        self.random_table.setColumnWidth(2, 100)

        self.fill_table(self.random_table, [self.random_lst1, self.random_lst2, self.random_lst3])

        self.coef_lbl4 = QLabel(
            str(round(criterions.common_criterion(
                0, 9, self.random_lst1
            ) * 100, 2)) + '%', self
        )
        self.coef_lbl4.setGeometry(650, 400, 100, 100)
        self.coef_lbl5 = QLabel(
            str(round(criterions.common_criterion(
                10, 99, self.random_lst2
            ) * 100, 2)) + '%', self
        )
        self.coef_lbl5.setGeometry(750, 400, 100, 100)
        self.coef_lbl6 = QLabel(
            str(round(criterions.common_criterion(
                100, 999, self.random_lst3
            ) * 100, 2)) + '%', self
        )
        self.coef_lbl6.setGeometry(850, 400, 100, 100)

        # == #

        self.input_lbl = QLabel('введенные значения', self)
        self.input_lbl.setGeometry(1100, 0, 200, 50)

        self.input_table = QTableWidget(self)
        self.input_table.setGeometry(1000, 50, 360, 350)
        self.input_table.setColumnCount(3)
        self.input_table.setHorizontalHeaderLabels(
            ('0-9', '10-99', '100-999'))
        self.input_table.setColumnWidth(0, 100)
        self.input_table.setColumnWidth(1, 100)
        self.input_table.setColumnWidth(2, 100)

        self.input_lsts = [
            lists.get_input_list(0, 9),
            lists.get_input_list(10, 99),
            lists.get_input_list(100, 999),
        ]

        self.fill_table(self.input_table, [self.input_lsts[0], self.input_lsts[1], self.input_lsts[2]], editable=True)

        self.input_coef_lbls = [None for i in range(3)]

        self.input_coef_lbls[0] = QLabel(
            str(round(criterions.common_criterion(
                0, 9, self.input_lsts[0]
            ) * 100, 2)) + '%', self
        )
        self.input_coef_lbls[0].setGeometry(1050, 400, 100, 100)
        self.input_coef_lbls[1] = QLabel(
            str(round(criterions.common_criterion(
                10, 99, self.input_lsts[1]
            ) * 100, 2)) + '%', self
        )
        self.input_coef_lbls[1].setGeometry(1150, 400, 100, 100)
        self.input_coef_lbls[2] = QLabel(
            str(round(criterions.common_criterion(
                100, 999, self.input_lsts[2]
            ) * 100, 2)) + '%', self
        )
        self.input_coef_lbls[2].setGeometry(1250, 400, 100, 100)

        # == #

        self.calc_input_button = QPushButton('Пересчитать', self)
        self.calc_input_button.clicked.connect(self.calc_input)
        self.calc_input_button.setGeometry(1400, 300, 350, 100)

        self.lcg_lbl = QLabel('Параметры\nгенератора', self)
        self.lcg_lbl.setGeometry(1425, 0, 200, 50)

        self.x0_lbl = QLabel('x0 =', self)
        self.x0_lbl.setGeometry(1400, 50, 50, 50)
        self.x0_edit = QLineEdit('0', self)
        self.x0_edit.setGeometry(1450, 50, 100, 50)

        self.a_lbl = QLabel('a =', self)
        self.a_lbl.setGeometry(1400, 100, 50, 50)
        self.a_edit = QLineEdit('84589', self)
        self.a_edit.setGeometry(1450, 100, 100, 50)

        self.c_lbl = QLabel('c =', self)
        self.c_lbl.setGeometry(1400, 150, 50, 50)
        self.c_edit = QLineEdit('45989', self)
        self.c_edit.setGeometry(1450, 150, 100, 50)

        self.m_lbl = QLabel('m =', self)
        self.m_lbl.setGeometry(1400, 200, 50, 50)
        self.m_edit = QLineEdit('217728', self)
        self.m_edit.setGeometry(1450, 200, 100, 50)

        # == #

        self.crit_lbl = QLabel('Учитывать\nкритерии', self)
        self.crit_lbl.setGeometry(1625, 0, 200, 50)

        self.uni_lbl = QLabel('Равномерность', self)
        self.uni_lbl.setGeometry(1600, 50, 150, 50)
        self.uni_flag = QCheckBox(self)
        self.uni_flag.move(1750, 70)
        self.uni_flag.setChecked(True)

        self.cor_lbl = QLabel('Корреляция', self)
        self.cor_lbl.setGeometry(1600, 100, 150, 50)
        self.cor_flag = QCheckBox(self)
        self.cor_flag.move(1750, 120)
        self.cor_flag.setChecked(True)

        self.ent_lbl = QLabel('Энтропия', self)
        self.ent_lbl.setGeometry(1600, 150, 150, 50)
        self.ent_flag = QCheckBox(self)
        self.ent_flag.move(1750, 170)
        self.ent_flag.setChecked(True)

    def start_application(self):
        self.update()
        self.show()
        self.qapp.exec_()

    def fill_table(self, table, lsts, editable=False):
        table.setRowCount(0)
        for i, data in enumerate(zip(*lsts)):
            table.insertRow(i)
            for j, n in enumerate(data):
                table.setItem(i, j, Item(str(n), editable=editable))

    def calc_input(self):
        self.coef_lbl1.setText(
            str(round(criterions.common_criterion(
                0, 9,
                self.file_lst1,
                uni=self.uni_flag.isChecked(),
                cor=self.cor_flag.isChecked(),
                ent=self.ent_flag.isChecked(),
            ) * 100, 2)) + '%'
        )
        self.coef_lbl2.setText(
            str(round(criterions.common_criterion(
                10, 99,
                self.file_lst2,
                uni=self.uni_flag.isChecked(),
                cor=self.cor_flag.isChecked(),
                ent=self.ent_flag.isChecked(),
            ) * 100, 2)) + '%'
        )
        self.coef_lbl3.setText(
            str(round(criterions.common_criterion(
                100, 999,
                self.file_lst3,
                uni=self.uni_flag.isChecked(),
                cor=self.cor_flag.isChecked(),
                ent=self.ent_flag.isChecked(),
            ) * 100, 2)) + '%'
        )
        for i in range(3):
            try:
                self.input_lsts[i] = [
                    int(n) for n in [
                        self.input_table.item(j, i).text() for j in range(10)
                    ]
                ]
                self.input_coef_lbls[i].setText(
                    str(round(criterions.common_criterion(
                        *self.ranges[i],
                        self.input_lsts[i],
                        uni=self.uni_flag.isChecked(),
                        cor=self.cor_flag.isChecked(),
                        ent=self.ent_flag.isChecked(),
                    ) * 100, 2)) + '%'
                )
            except:
                pass
        try:
            x0 = int(self.x0_edit.text())
            a = int(self.a_edit.text())
            c = int(self.c_edit.text())
            m = int(self.m_edit.text())

            self.lcg = lcg.LCG(x0=x0, a=a, c=c, m=m)

            self.random_lst1 = lists.get_random_list(self.lcg, 0, 9, LENGTH)
            self.random_lst2 = lists.get_random_list(self.lcg, 10, 99, LENGTH)
            self.random_lst3 = lists.get_random_list(self.lcg, 100, 999, LENGTH)

            self.coef_lbl4.setText(
                str(round(criterions.common_criterion(
                    0, 9,
                    self.random_lst1,
                    uni=self.uni_flag.isChecked(),
                    cor=self.cor_flag.isChecked(),
                    ent=self.ent_flag.isChecked(),
                ) * 100, 2)) + '%'
            )
            self.coef_lbl5.setText(
                str(round(criterions.common_criterion(
                    10, 99,
                    self.random_lst2,
                    uni=self.uni_flag.isChecked(),
                    cor=self.cor_flag.isChecked(),
                    ent=self.ent_flag.isChecked(),
                ) * 100, 2)) + '%'
            )
            self.coef_lbl6.setText(
                str(round(criterions.common_criterion(
                    100, 999,
                    self.random_lst3,
                    uni=self.uni_flag.isChecked(),
                    cor=self.cor_flag.isChecked(),
                    ent=self.ent_flag.isChecked(),
                ) * 100, 2)) + '%'
            )

            self.fill_table(self.random_table, [self.random_lst1, self.random_lst2, self.random_lst3])

        except Exception as exc:
            pass
