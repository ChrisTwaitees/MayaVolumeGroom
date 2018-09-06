import PySide2.QtCore as qc
import PySide2.QtGui as qg
import PySide2.QtWidgets as qw
import sys

def Start():
    m = AddAttrGUI()
    m.show()
    return m


class AddAttrGUI(qw.QDialog):
    def __init__(self):
        qw.QDialog.__init__(self)
        self.setWindowTitle('ADD EXTRA ATTRIBUTE')
        self.setWindowFlags(qc.Qt.WindowStaysOnTopHint)
        self.setModal(False)
        self.setMinimumHeight(500)
        self.setMinimumWidth(300)

        self.setLayout(qw.QVBoxLayout())
        self.layout().setContentsMargins(5, 5, 5, 5)
        self.layout().setSpacing(7)
        qw.QApplication.setStyle(qw.QStyleFactory.create('Plastique'))

        # adding frames for each step

        attributeInfo_frame = qw.QFrame()
        attributeInfo_frame.setFrameStyle(qw.QFrame.Panel | qw.QFrame.Raised)
        attributeInfo_frame.setSizePolicy(qw.QSizePolicy.Minimum, qw.QSizePolicy.Minimum)

        # creating layouts

        attributeInfo_layout = qw.QVBoxLayout()
        attributeInfo_layout.setAlignment(qc.Qt.AlignVCenter)

        # setting layouts to frames

        attributeInfo_frame.setLayout(attributeInfo_layout)

        # widgets

        bold_font = qg.QFont()
        bold_font.setBold(True)

        # ATTRIBUTE INFO WIDGETS

        self.attributetypes = {'float': 'float', 'float3': 'float3', 'Color': 'float3'}

        attributeTypesDropdown_layout = qw.QFormLayout()

        attributeTypes_label = qw.QLabel('Attribute Types: ')
        self.attributeTypesDropdown = qw.QComboBox()
        for k, v in self.attributetypes.items():
            self.attributeTypesDropdown.addItem(k)

        attributeTypesDropdown_layout.addRow(attributeTypes_label, self.attributeTypesDropdown)

        attributeNameLabel = qw.QLabel('Attribute Name:\n')
        attributeNameLabel.setFont(bold_font)


        attributeName = qw.QLineEdit()
        attributeName.setClearButtonEnabled(True)
        attributeName.insert('random01')
        attributeName.setSizePolicy(qw.QSizePolicy.Minimum, qw.QSizePolicy.Minimum)

        attributeTypesDropdown_layout.addRow(attributeNameLabel, attributeName)

        attributeInfo_layout.addLayout(attributeTypesDropdown_layout)


        # AddAttr widgets


        addAttr_bttn = qw.QPushButton('Add Attr')

        attributeInfo_layout.addWidget(addAttr_bttn)

        # addAttr_bttn.clicked.connect(lambda: STB.voronoisurface(int(voronoi_densitycount.text())))

        #   adding frames

        self.layout().addWidget(attributeInfo_frame)