from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from utils import pyside


#Samson Imports
global STB

class SamsonUIMain(pyside.SimpleToolWindow):
    toolName = 'SamsonUI'

    def __init__(self, parent=None):
        super(self.__class__, self).__init__()
        # Setup window's properties
        self.setWindowTitle('SAMSON')
        self.setModal(False)
        self.setMinimumHeight(700)
        self.setMinimumWidth(300)

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(5, 5, 5, 5)
        self.layout().setSpacing(7)


        # adding frames for each step

        scalp_frame = QFrame()
        scalp_frame.setFrameStyle(QFrame.Panel | QFrame.Raised)

        centerguide_frame = QFrame()
        centerguide_frame.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.MinimumExpanding)
        centerguide_frame.setFrameStyle(QFrame.Panel | QFrame.Raised)

        tube_frame = QFrame()
        tube_frame.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.MinimumExpanding)
        tube_frame.setFrameStyle(QFrame.Panel | QFrame.Raised)

        centerguide_tube_frame = QFrame()
        centerguide_tube_frame.setFrameStyle(QFrame.Panel | QFrame.Raised)

        generatecurves_frame = QFrame()
        generatecurves_frame.setFrameStyle(QFrame.Panel | QFrame.Raised)

        # creating layouts

        scalplayout = QVBoxLayout()
        scalplayout.setContentsMargins(5, 5, 5, 5)
        scalplayout.setAlignment(Qt.AlignVCenter)

        centerguidelayout = QVBoxLayout()
        centerguidelayout.setAlignment(Qt.AlignVCenter)

        tubelayout = QVBoxLayout()
        tubelayout.setAlignment(Qt.AlignVCenter)

        centerguide_tube_layout = QGridLayout()
        centerguide_tube_layout.setAlignment(Qt.AlignHCenter)

        gencurveslayout = QVBoxLayout()

        # setting layouts to frames

        scalp_frame.setLayout(scalplayout)
        centerguide_frame.setLayout(centerguidelayout)
        tube_frame.setLayout(tubelayout)
        centerguide_tube_frame.setLayout(centerguide_tube_layout)
        generatecurves_frame.setLayout(gencurveslayout)

        # parenting frames

        centerguide_tube_layout.addWidget(centerguide_frame,0,0)
        centerguide_tube_layout.addWidget(tube_frame,0,1)

        # widgets

        bold_font = QFont()
        bold_font.setBold(True)

        # SCALP widgets

        scalp_header = QLabel('SCALP')
        scalp_header.setFont(bold_font)
        scalplayout.addWidget(scalp_header)

        scalpvoronoilayout = QFormLayout()
        scalpvoronoilayout.setHorizontalSpacing(5)
        scalpvoronoilayout.setFormAlignment(Qt.AlignHCenter)
        scalpvoronoilayout.setRowWrapPolicy(QFormLayout.WrapLongRows)
        scalplayout.addLayout(scalpvoronoilayout)

        self.voronoi_surface_entry = QLabel()
        self.voronoi_surface_entry.setText("Select Surface")
        voronoi_surface_button = QPushButton('<<')
        voronoi_surface_button.clicked.connect(lambda: self.setScalpShape())
        scalpvoronoilayout.addRow(self.voronoi_surface_entry, voronoi_surface_button)


        voronoi_bttn = QPushButton('Voronoi Scalp')
        voronoi_bttn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        # voronoi_bttn.clicked.connect(lambda: Utilities.voronoi.main(self.voronoi_surface_entry.text()))
        scalplayout.addWidget(voronoi_bttn)

        refreshscalp_bttn = QPushButton('Refresh Scalp')
        scalplayout.addWidget(refreshscalp_bttn)
        refreshscalp_bttn.clicked.connect(lambda: STB.refresh_scalp())

        exportregionmap_bttn = QPushButton('Export Region Map')
        scalplayout.addWidget(exportregionmap_bttn)

        # CENTERGUIDE widgets

        centerguide_header = QLabel('CENTERGUIDE')
        centerguide_header.setFont(bold_font)
        centerguidelayout.addWidget(centerguide_header)

        #generate guide
        generatecurve_layout = QFormLayout()
        generatecurve_layout.setAlignment(Qt.AlignVCenter)
        centerguidelayout.addLayout(generatecurve_layout)

        generatecurve_bttn = QPushButton('Add Guide')
        self.generatecurve_bttn_densitycount = QLineEdit()
        self.generatecurve_bttn_densitycount.setMaxLength(3)
        self.generatecurve_bttn_densitycount.insert('5')
        self.generatecurve_bttn_densitycount.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        generatecurve_layout.addRow(generatecurve_bttn, self.generatecurve_bttn_densitycount)
        # generatecurve_bttn.clicked.connect(lambda: Utilities.addGuide.main(self.voronoi_surface_entry.text(),
        #                                                                    self.generatecurve_bttn_densitycount.text()))

        editcurve_bttn = QPushButton('Edit Curve')
        centerguidelayout.addWidget(editcurve_bttn)
        editcurve_bttn.clicked.connect(lambda: STB.editcenterguide(self.voronoi_surface_entry.text()))

        savechangescurve_bttn = QPushButton('Save Changes')
        centerguidelayout.addWidget(savechangescurve_bttn)
        savechangescurve_bttn.clicked.connect(lambda: STB.savecenterguide_changes())

        rebuildcurvelayout = QFormLayout()
        rebuildcurvelayout.setAlignment(Qt.AlignVCenter)
        centerguidelayout.addLayout(rebuildcurvelayout)

        rebuildcurve_bttn = QPushButton('Rebuild Curve')

        rebuildcurve_densitycount = QLineEdit()
        rebuildcurve_densitycount.setMaxLength(3)
        rebuildcurve_densitycount.insert('8')
        rebuildcurve_densitycount.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        rebuildcurve_bttn.clicked.connect(lambda: STB.rebuildcurve(int(rebuildcurve_densitycount.text())))
        rebuildcurvelayout.addRow(rebuildcurve_bttn, rebuildcurve_densitycount)

        centerguidelayout.addLayout(rebuildcurvelayout)

        selectallcurves_bttn = QPushButton('Select All CenterGuides')
        centerguidelayout.addWidget(selectallcurves_bttn)
        selectallcurves_bttn.clicked.connect(lambda: STB.select_curves(self.descriptions_dropdown.currentText()))

        deletecurve_bttn = QPushButton('Delete CenterGuide')
        centerguidelayout.addWidget(deletecurve_bttn)
        deletecurve_bttn.clicked.connect(lambda: STB.deleteclump())

        # TUBE widgetes

        tube_header = QLabel('TUBE')
        tube_header.setFont(bold_font)
        tubelayout.addWidget(tube_header)

        generatenewtube_bttn = QPushButton('Generate New Tube')
        tubelayout.addWidget(generatenewtube_bttn)
        generatenewtube_bttn.clicked.connect(lambda: STB.attachtube(0.8))

        edittube_bttn = QPushButton('Edit Tube')
        tubelayout.addWidget(edittube_bttn)
        edittube_bttn.clicked.connect(lambda: STB.edittube())

        # savechangestube_bttn = QPushButton('Save Changes')
        # tubelayout.addWidget(savechangestube_bttn)

        selectalltubes_bttn = QPushButton('Select All Tubes')
        tubelayout.addWidget(selectalltubes_bttn)
        selectalltubes_bttn.clicked.connect(lambda: STB.select_tubes(self.descriptions_dropdown.currentText()))

        deletetube_bttn = QPushButton('Delete Tube')
        tubelayout.addWidget(deletetube_bttn)
        deletetube_bttn.clicked.connect(lambda: STB.deletetube())

        # CURVE GEN widgets

        gencurves_header = QLabel('GENERATE CURVES')
        gencurves_header.setFont(bold_font)
        gencurveslayout.addWidget(gencurves_header)

        generateguidecurveslayout = QFormLayout()
        generateguidecurveslayout.setAlignment(Qt.AlignVCenter)
        gencurveslayout.addLayout(generateguidecurveslayout)

        generate_onlyexternalguides_check = QCheckBox('Generate Only Outer Guides')
        gencurveslayout.addWidget(generate_onlyexternalguides_check)

        # generate_onlyexternalguides_check.stateChanged.connect()

        filltube_bttn = QPushButton('Fill Selected Tube With Curves')

        filltube_densitycount = QLineEdit()
        filltube_densitycount.setMaxLength(3)
        filltube_densitycount.insert('2')
        filltube_densitycount.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        filltube_bttn.clicked.connect(lambda: STB.gencurvesfromtube(numberofcurves=int(filltube_densitycount.text()),
                                                                    onlyoutercurves=generate_onlyexternalguides_check.isChecked()))

        generateguidecurves_bttn = QPushButton('Generate Guide Curves')

        gencurves_densitycount = QLineEdit()
        gencurves_densitycount.setMaxLength(3)
        gencurves_densitycount.setClearButtonEnabled(True)
        gencurves_densitycount.insert('2')
        gencurves_densitycount.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        generateguidecurves_bttn.clicked.connect(lambda: STB.gencurvesglobal(int(gencurves_densitycount.text()),
                                                                             onlyoutercurves=generate_onlyexternalguides_check.isChecked()))

        generateguidecurveslayout.addRow(filltube_bttn, filltube_densitycount)
        generateguidecurveslayout.addRow(generateguidecurves_bttn, gencurves_densitycount)

        deleteguidecurves_bttn = QPushButton("Delete Selected Tube's Guide Curves")
        gencurveslayout.addWidget(deleteguidecurves_bttn)
        deleteguidecurves_bttn.clicked.connect(lambda: STB.deleteguidecurves())

        deleteallguidecurves_bttn = QPushButton("Delete All Guide Curves")
        gencurveslayout.addWidget(deleteallguidecurves_bttn)
        deleteallguidecurves_bttn.clicked.connect(lambda: STB.remove_allguidecurves())

        extractguides_bttn = QPushButton('Extract Guides')
        gencurveslayout.addWidget(extractguides_bttn)
        extractguides_bttn.clicked.connect(lambda: STB.extract_guide_curves())

        #   adding frames

        self.layout().addWidget(scalp_frame)
        #self.layout().addWidget(centerguide_frame)
        #self.layout().addWidget(tube_frame)
        self.layout().addWidget(centerguide_tube_frame)
        self.layout().addWidget(generatecurves_frame)

    # functions

    def setScalpShape(self):
        return
        # scalp = Utilities.selection.fetch_selection(shape=True)
        # self.voronoi_surface_entry.setText(scalp)
        # print "Scalp shape has been set to : %s"%scalp


def main():
    SamsonUIMain().run()


