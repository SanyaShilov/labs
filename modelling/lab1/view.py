from math import log
from matplotlib import pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QLineEdit
)

from laws import UniformDistributionLaw, NormalDistributionLaw


def hist_steps(sample):
    return int(log(len(sample), 2)) + 1


class View(QMainWindow):
    def __init__(self):
        self.qapp = QApplication([])
        super().__init__()
        self.setFixedSize(700, 800)
        self.move(100, 10)
        self.setWindowTitle(
            'Лабораторная работа №1 по моделированию, вариант №14. '
            'Шилов ИУ7-72'
        )

        self.uniform_label = QLabel('Равномерное\nраспределение', self)
        self.uniform_label.setFixedSize(200, 100)
        self.uniform_label.move(100, 100)

        self.a = -1
        self.a_label = QLabel('a =', self)
        self.a_label.setFixedSize(100, 100)
        self.a_label.move(100, 200)
        self.a_line_edit = QLineEdit(str(self.a), self)
        self.a_line_edit.setFixedSize(100, 100)
        self.a_line_edit.move(200, 200)

        self.b = 1
        self.b_label = QLabel('b =', self)
        self.b_label.setFixedSize(100, 100)
        self.b_label.move(100, 300)
        self.b_line_edit = QLineEdit(str(self.b), self)
        self.b_line_edit.setFixedSize(100, 100)
        self.b_line_edit.move(200, 300)

        self.uniform_n = 100
        self.uniform_n_label = QLabel('n =', self)
        self.uniform_n_label.setFixedSize(100, 100)
        self.uniform_n_label.move(100, 400)
        self.uniform_n_line_edit = QLineEdit(str(self.uniform_n), self)
        self.uniform_n_line_edit.setFixedSize(100, 100)
        self.uniform_n_line_edit.move(200, 400)

        self.normal_label = QLabel('Нормальное\nраспределение', self)
        self.normal_label.setFixedSize(200, 100)
        self.normal_label.move(400, 100)

        self.nu = 0
        self.nu_label = QLabel('nu =', self)
        self.nu_label.setFixedSize(100, 100)
        self.nu_label.move(400, 200)
        self.nu_line_edit = QLineEdit(str(self.nu), self)
        self.nu_line_edit.setFixedSize(100, 100)
        self.nu_line_edit.move(500, 200)

        self.sigma = 1
        self.sigma_label = QLabel('sigma =', self)
        self.sigma_label.setFixedSize(100, 100)
        self.sigma_label.move(400, 300)
        self.sigma_line_edit = QLineEdit(str(self.sigma), self)
        self.sigma_line_edit.setFixedSize(100, 100)
        self.sigma_line_edit.move(500, 300)

        self.normal_n = 100
        self.normal_n_label = QLabel('n =', self)
        self.normal_n_label.setFixedSize(100, 100)
        self.normal_n_label.move(400, 400)
        self.normal_n_line_edit = QLineEdit(str(self.normal_n), self)
        self.normal_n_line_edit.setFixedSize(100, 100)
        self.normal_n_line_edit.move(500, 400)

        self.uniform_distribution_law = UniformDistributionLaw(
            a=self.a, b=self.b
        )
        self.normal_distribution_law = NormalDistributionLaw(
            nu=self.nu, sigma=self.sigma
        )

        self.button = QPushButton('Провести рассчет', self)
        self.button.setFixedSize(500, 100)
        self.button.clicked.connect(self.calculate)
        self.button.move(100, 600)

    def start_application(self):
        self.update()
        self.show()
        self.qapp.exec_()

    def get_input(self):
        try:
            self.a = float(self.a_line_edit.text())
            self.b = float(self.b_line_edit.text())
            self.uniform_n = int(self.uniform_n_line_edit.text())
            self.nu = float(self.nu_line_edit.text())
            self.sigma = float(self.sigma_line_edit.text())
            self.normal_n = int(self.normal_n_line_edit.text())
        except ValueError:
            return 'Неверный формат входных данных'
        if (
                self.b <= self.a or
                not (10 <= self.uniform_n <= 10000) or
                self.sigma <= 0 or
                not (10 <= self.normal_n <= 10000)
        ):
            return 'Нарушены ограничения на входные данные'

    def calculate(self):
        error = self.get_input()
        if error:
            return
        self.uniform_distribution_law = UniformDistributionLaw(
            a=self.a, b=self.b
        )
        self.normal_distribution_law = NormalDistributionLaw(
            nu=self.nu, sigma=self.sigma
        )
        plt.subplot(221)
        plt.plot(
            self.uniform_distribution_law.x_list,
            self.uniform_distribution_law.F_list
        )
        uniform_sample = self.uniform_distribution_law.sample(self.uniform_n)
        plt.plot(
            (
                [self.uniform_distribution_law.left_border] +
                uniform_sample +
                [self.uniform_distribution_law.right_border]
            ),
            (
                [i / self.uniform_n for i in range(self.uniform_n + 1)] +
                [1]
            )
        )
        plt.grid(True)
        plt.title('Равномерное распределение')
        plt.xlabel('x')
        plt.ylabel('F(x)')
        plt.subplot(222)
        plt.plot(
            self.normal_distribution_law.x_list,
            self.normal_distribution_law.F_list
        )
        normal_sample = self.normal_distribution_law.sample(self.normal_n)
        plt.plot(
            (
                [self.normal_distribution_law.left_border] +
                normal_sample +
                [self.normal_distribution_law.right_border]
            ),
            (
                [i / self.normal_n for i in range(self.normal_n + 1)] +
                [1]
            )
        )
        plt.grid(True)
        plt.title('Нормальное распределение')
        plt.xlabel('x')
        plt.subplot(223)
        plt.plot(
            self.uniform_distribution_law.x_list,
            self.uniform_distribution_law.f_list,
        )
        plt.hist(uniform_sample, hist_steps(uniform_sample), density=True, alpha=0.5)
        plt.grid(True)
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.subplot(224)
        plt.plot(
            self.normal_distribution_law.x_list,
            self.normal_distribution_law.f_list,
        )
        plt.hist(normal_sample, hist_steps(normal_sample), density=True, alpha=0.5)
        plt.grid(True)
        plt.xlabel('x')
        plt.show()
