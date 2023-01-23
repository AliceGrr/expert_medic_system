import os
import sys
import PyQt5
from PyQt5.QtWidgets import QMessageBox
import docx
from docx import Document
from PyQt5 import QtWidgets

import help_form
import main_form
import expert_medic_system
from expert_medic_system import ExpertMedicSystemBack


class HelpForm(QtWidgets.QDialog, help_form.Ui_HelpDialog):

    def __init__(self, help_text):
        super().__init__()
        self.ui = help_form.Ui_HelpDialog()
        self.ui.setupUi(self)

        # связки кнопок и функций
        self.ui.quit_button.clicked.connect(self.close_dialog)

        self.ui.help_field.setText(help_text)

    def close_dialog(self):
        self.close()


def export_test_from_docx(disease_name):
    doc_path = os.path.join(os.path.abspath(os.getcwd()), 'static\docs\\', f'{disease_name}.docx')
    doc = Document(doc_path)
    all_paras = f'Скорее всего у вас: {disease_name}\n' + '\n'.join(paragraph.text for paragraph in doc.paragraphs)
    return all_paras


class ExpertMedicSystemForm(QtWidgets.QMainWindow, main_form.Ui_ExpertMedicSystemForm):

    def __init__(self):
        super().__init__()
        self.ui = main_form.Ui_ExpertMedicSystemForm()
        self.ui.setupUi(self)

        self.back = ExpertMedicSystemBack()

        self.ui.question_field.setWordWrap(True)

        # связки кнопок и функций
        self.ui.yes_button.clicked.connect(self.yes_button_clicked)
        self.ui.no_button.clicked.connect(self.no_button_clicked)
        self.ui.restart_button.clicked.connect(self.restart)
        self.ui.result_help_button.clicked.connect(self.result_help)
        self.ui.question_help_button.clicked.connect(self.question_help)

        QMessageBox.about(self, "Запомните", "Решение, принимаемое системой может быть ошибочным! Обязательно сходите к врачу!")

        self.show_question()

    def yes_button_clicked(self):
        self.ui.hello_field.clear()

        self.back.current_state += 'y'

        self.back.solve_path += self.back.symptoms.get(self.back.current_state) + '\n'

        if self.back.current_state in self.back.questions:
            self.show_question()
            self.update_suspected_result()
        else:
            self.show_result()

    def no_button_clicked(self):
        self.ui.hello_field.clear()

        self.back.current_state += 'n'

        self.back.solve_path += self.back.symptoms.get(self.back.current_state) + '\n'

        if self.back.current_state in self.back.questions:
            self.show_question()
            self.update_suspected_result()
        else:
            self.show_result()

    def show_question(self):
        self.ui.question_field.setText(self.back.questions.get(self.back.current_state))

    def show_result(self):
        self.ui.question_field.setText('Опрос закончен!')
        disease_description = export_test_from_docx(self.back.endpoints.get(self.back.current_state))
        self.ui.result_field.setText(disease_description)
        self.ui.no_button.setEnabled(False)
        self.ui.yes_button.setEnabled(False)

    def update_suspected_result(self):
        self.ui.result_field.setText(self.back.suspected_results)

    def restart(self):
        self.ui.result_field.clear()
        self.ui.no_button.setEnabled(True)
        self.ui.yes_button.setEnabled(True)
        self.back.current_state = ''
        self.back.last_solution = ''
        self.back.solve_path = 'Вы указали следующие симптомы:\n'
        self.ui.hello_field.setText('Добро пожаловать в медицинскую экспертную систему!'
                                    '\nЗдесь будут предполагаемые в ходе опроса заболевания и конечный результат.')
        self.show_question()

    def result_help(self):
        if self.back.solve_path == 'Вы указали следующие симптомы:\n':
            help_window = HelpForm('Вы пока еще ничего не ответили!')
        else:
            help_window = HelpForm(self.back.solve_path)
        help_window.exec_()

    def question_help(self):
        help_window = HelpForm(self.back.questions_explanation.get(self.back.current_state))
        help_window.exec_()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = ExpertMedicSystemForm()
    main_window.show()
    app.exec_()
