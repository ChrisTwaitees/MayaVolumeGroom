import PySide2.QtCore as qc
import PySide2.QtGui as qg
import PySide2.QtWidgets as qw


class SimpleInput(qw.QDialog):
    def __init__(self, title, label, button):
        self.title = title
        self.label = label
        self.button = button
        qw.QDialog.__init__(self)
        self.setWindowTitle(title)
        self.setWindowFlags(qc.Qt.WindowStaysOnTopHint)
        self.setModal(False)
        self.setMinimumHeight(50)
        self.setMinimumWidth(200)

        self.setLayout(qw.QVBoxLayout())
        self.layout().setContentsMargins(5, 5, 5, 5)
        self.layout().setSpacing(7)

        # adding frames

        simple_frame = qw.QFrame()
        simple_frame.setFrameStyle(qw.QFrame.Panel | qw.QFrame.Raised)
        simple_frame.setSizePolicy(qw.QSizePolicy.Minimum, qw.QSizePolicy.Minimum)

        # creating layout

        simple_layout = qw.QVBoxLayout()
        simple_layout.setAlignment(qc.Qt.AlignVCenter)

        # setting layout to frame

        simple_frame.setLayout(simple_layout)

        # WIDGETS

        bold_font = qg.QFont()
        bold_font.setBold(True)

        simple_label = qw.QLabel(self.label)
        simple_label.setFont(bold_font)
        simple_layout.addWidget(simple_label)

        simple_entryLayout = qw.QFormLayout()
        simple_entryLayout.setAlignment(qc.Qt.AlignVCenter)
        simple_layout.addLayout(simple_entryLayout)

        simple_bttn = qw.QPushButton(self.button)
        simple_entry = qw.QLineEdit()
        simple_entry.setClearButtonEnabled(True)
        simple_entry.setSizePolicy(qw.QSizePolicy.Minimum, qw.QSizePolicy.Minimum)
        simple_entryLayout.addRow(simple_bttn, simple_entry)

        simple_bttn.clicked.connect(lambda: self.returnText(simple_entry.text()))

        # adding frames
        self.layout().addWidget(simple_frame)

    # FUNCTIONS

    def returnText(self, simple_input):
        print simple_input
        return simple_input


def simpleInputMain(title, label, button):
    simpleInputWindow = SimpleInput(title, label, button)
    return simpleInputWindow


class ProgressBarWindow(qw.QDialog):
    def __init__(self, title, label):
        self.title = title
        self.label = label

        qw.QDialog.__init__(self)
        self.setWindowTitle(title)
        self.setWindowFlags(qc.Qt.WindowStaysOnTopHint)
        self.setModal(False)
        self.setMinimumHeight(50)
        self.setMinimumWidth(200)

        self.setLayout(qw.QVBoxLayout())
        self.layout().setContentsMargins(5, 5, 5, 5)
        self.layout().setSpacing(7)

        # adding frames

        simple_frame = qw.QFrame()
        simple_frame.setFrameStyle(qw.QFrame.Panel | qw.QFrame.Raised)
        simple_frame.setSizePolicy(qw.QSizePolicy.Minimum, qw.QSizePolicy.Minimum)

        # creating layout

        simple_layout = qw.QVBoxLayout()
        simple_layout.setAlignment(qc.Qt.AlignVCenter)

        # setting layout to frame

        simple_frame.setLayout(simple_layout)

        # WIDGETS

        bold_font = qg.QFont()
        bold_font.setBold(True)

        self.simple_label = qw.QLabel(self.label)
        self.simple_label.setFont(bold_font)
        self.simple_label.setAlignment(qc.Qt.AlignHCenter)
        simple_layout.addWidget(self.simple_label)

        # ProgressBar

        self.simple_progressBar = qw.QProgressBar()
        self.simple_progressBar.setAlignment(qc.Qt.AlignHCenter)
        simple_layout.addWidget(self.simple_progressBar)

        # adding frames
        self.layout().addWidget(simple_frame)

    # FUNCTIONS

    def updateProgress(self, percentile):
        self.simple_progressBar.setValue(percentile)

    def updateLabel(self, updateText):
        self.simple_label.setText(updateText)


def simpleProgressBarWindow(title, label):
    progressBar = ProgressBarWindow(title, label)
    return progressBar