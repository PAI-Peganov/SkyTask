from src.qt_app import *


class ListStringsInput(QWidget):
    def __init__(self, min_lines_count, can_add_lines=False):
        super().__init__()
        self.adjustSize()
        self.min_lines_count = min_lines_count
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        if can_add_lines:
            self.buttons = QWidget()
            self.buttons.setLayout(QHBoxLayout())
            font = QtGui.QFont()
            font.setPointSize(12)
            self.add_button = QPushButton(text="+")
            self.add_button.setFont(font)
            self.add_button.clicked.connect(self.add_line)
            self.remove_button = QPushButton(text="—")
            self.remove_button.setFont(font)
            self.remove_button.clicked.connect(self.remove_line)
            self.remove_button.setEnabled(False)
            self.buttons.layout().addWidget(self.add_button)
            self.buttons.layout().addWidget(self.remove_button)
            self.layout.addWidget(self.buttons)
        self.lines = list()
        for _ in range(min_lines_count):
            self.add_line()
        self.setLayout(self.layout)

    def add_line(self):
        self.lines.append(QLineEdit())
        self.layout.addWidget(self.lines[-1])
        self.remove_button.setEnabled(True)

    def remove_line(self):
        if len(self.lines) > self.min_lines_count:
            self.layout.removeWidget(self.lines[-1])
            self.lines.remove(self.lines[-1])
            if len(self.lines) == self.min_lines_count:
                self.remove_button.setEnabled(False)

    def result_list(self):
        result = list()
        for el in self.lines:
            text = el.text().strip()
            if any(sign in text for sign in {",", ";", "/n", "/r"}):
                raise ValueError()
            result.append(text)
        return result


class AddingWidget(QDialog):
    def __init__(self, name: str, input_params: list[tuple], func: callable):
        super().__init__()
        self.setWindowTitle(name)
        self.adjustSize()

        self.layout = QVBoxLayout()
        self.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Policy.Preferred,
                QtWidgets.QSizePolicy.Policy.Maximum
            )
        )
        self.inputs = dict()
        self.func = func

        for param in input_params:
            if param[2] is str:
                new_input = QLineEdit()
            elif param[2] is float:
                new_input = QDoubleSpinBox()
                new_input.setRange(-1000.0, 1000.0)
                new_input.setValue(0.0)
            elif param[2] is int:
                new_input = QSpinBox()
                new_input.setRange(-1000, 1000)
                new_input.setValue(0)
            else:
                new_input = ListStringsInput(
                    param[3], can_add_lines=param[4]
                )
            self.inputs[param[0]] = new_input
            label = QLabel(text=param[1])
            self.layout.addWidget(label)
            label.setSizePolicy(
                QtWidgets.QSizePolicy(
                    QtWidgets.QSizePolicy.Policy.Expanding,
                    QtWidgets.QSizePolicy.Policy.Maximum
                )
            )
            self.layout.addWidget(new_input)
            new_input.setSizePolicy(
                QtWidgets.QSizePolicy(
                    QtWidgets.QSizePolicy.Policy.Expanding,
                    QtWidgets.QSizePolicy.Policy.Maximum
                )
            )
            # self.layout.addRow(param[1], new_input)

        self.submit_btn = QPushButton("Создать")
        self.submit_btn.clicked.connect(self.validate_input)

        self.layout.addWidget(self.submit_btn)
        self.layout.addWidget(QWidget())

        self.setLayout(self.layout)

    def validate_input(self):
        result = dict()
        for param_name, qt_input in self.inputs.items():
            if isinstance(qt_input, QLineEdit):
                result[param_name] = qt_input.text().strip()
            elif isinstance(qt_input, QDoubleSpinBox):
                result[param_name] = float(qt_input.value())
            elif isinstance(qt_input, QSpinBox):
                result[param_name] = int(qt_input.value())
            else:
                result[param_name] = qt_input.result_list()

        try:
            self.func(**result)
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", "{}".format(e))


class AddingOptionsWidget(QDialog):
    def __init__(self, name: str, options: dict,
                 is_destroyable=True, parent=None):
        super().__init__(parent)
        self.adjustSize()
        self.is_destroyable = is_destroyable
        self.setWindowTitle(name)
        self.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Policy.Preferred,
                QtWidgets.QSizePolicy.Policy.MinimumExpanding
            )
        )
        self.layout = QVBoxLayout()
        for option_name, option in options.items():
            self.add_button(option_name, option)
        space_widget = QWidget()
        self.layout.addWidget(space_widget)
        self.setLayout(self.layout)
        space_widget.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Policy.Preferred,
                QtWidgets.QSizePolicy.Policy.MinimumExpanding
            )
        )

    def add_button(self, name, option):
        new_button = QPushButton(text=name)
        self.layout.addWidget(new_button)
        new_button.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Policy.Expanding,
                QtWidgets.QSizePolicy.Policy.Maximum
            )
        )

        def click_starter():
            if isinstance(option, dict):
                new_window = AddingOptionsWidget(name, option)
            else:
                new_window = AddingWidget(name, option[0], option[1])
            if new_window.exec_() == QDialog.Accepted and self.is_destroyable:
                self.accept()

        new_button.clicked.connect(click_starter)
