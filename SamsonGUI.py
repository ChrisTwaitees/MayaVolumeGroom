import PySide2.QtCore as qc
import PySide2.QtGui as qg
import PySide2.QtWidgets as qw


class SimpleGUI(qw.QDialog):
    def __init__(self):
        qw.QDialog.__init__(self)
        self.setWindowTitle('Samson')
        self.setWindowFlags(qc.Qt.WindowStaysOnTopHint)
        self.setModal(False)
        self.setMinimumHeight(500)
        self.setMinimumWidth(300)

        self.setLayout(qw.QVBoxLayout())
        self.layout().setContentsMargins(5,5,5,5)
        self.layout().setSpacing(7)


        # adding frames for each step

        characterinfo_frame = qw.QFrame()
        characterinfo_frame.setFrameStyle(qw.QFrame.Panel | qw.QFrame.Raised)
        characterinfo_frame.setSizePolicy(qw.QSizePolicy.Minimum, qw.QSizePolicy.Minimum)

        scalp_frame = qw.QFrame()
        scalp_frame.setFrameStyle(qw.QFrame.Panel | qw.QFrame.Raised)

        centerguide_frame = qw.QFrame()
        centerguide_frame.setFrameStyle(qw.QFrame.Panel | qw.QFrame.Raised)

        tube_frame = qw.QFrame()
        tube_frame.setFrameStyle(qw.QFrame.Panel | qw.QFrame.Raised)

        generatecurves_frame = qw.QFrame()
        generatecurves_frame.setFrameStyle(qw.QFrame.Panel | qw.QFrame.Raised)

        # creating layouts

        characterinfo_layout = qw.QVBoxLayout()
        characterinfo_layout.setAlignment(qc.Qt.AlignVCenter)
        scalplayout = qw.QVBoxLayout()
        scalplayout.setContentsMargins(5,5,5,5)
        scalplayout.setAlignment(qc.Qt.AlignVCenter)
        centerguidelayout = qw.QVBoxLayout()
        centerguidelayout.setAlignment(qc.Qt.AlignVCenter)
        tubelayout = qw.QVBoxLayout()
        tubelayout.setAlignment(qc.Qt.AlignVCenter)
        gencurveslayout = qw.QVBoxLayout()
        gencurveslayout.setAlignment(qc.Qt.AlignVCenter)

        # setting layouts to frames

        characterinfo_frame.setLayout(characterinfo_layout)
        scalp_frame.setLayout(scalplayout)
        centerguide_frame.setLayout(centerguidelayout)
        tube_frame.setLayout(tubelayout)
        generatecurves_frame.setLayout(gencurveslayout)

        # widgets

        bold_font = qg.QFont()
        bold_font.setBold(True)

        # CHARACTER INFO WIDGETS

        characterinfo_header = qw.QLabel('CHARACTER INFO\n')
        characterinfo_header.setFont(bold_font)
        characterinfo_layout.addWidget(characterinfo_header)

        characterinfo_name = qw.QLineEdit()
        characterinfo_name.setPlaceholderText('Enter Character Asset Code...')
        characterinfo_layout.addWidget(characterinfo_name)


        # SCALP widgets

        scalp_header = qw.QLabel('SCALP')
        scalp_header.setFont(bold_font)
        scalplayout.addWidget(scalp_header)

        voronoi_bttn = qw.QPushButton('Voronoi Surface')
        scalplayout.addWidget(voronoi_bttn)\

        refreshscalp_bttn = qw.QPushButton('Refresh')
        scalplayout.addWidget(refreshscalp_bttn)

        exportregionmap_bttn = qw.QPushButton('Export Region Map')
        scalplayout.addWidget(exportregionmap_bttn)


        # CENTERGUIDE widgets

        centerguide_header = qw.QLabel('CENTERGUIDE')
        centerguide_header.setFont(bold_font)
        centerguidelayout.addWidget(centerguide_header)

        generatecurve_bttn = qw.QPushButton('Generate New Curve')
        centerguidelayout.addWidget(generatecurve_bttn)

        rebuildcurve_bttn = qw.QPushButton('Rebuild Curve')
        centerguidelayout.addWidget(rebuildcurve_bttn)

        editexistingcurve_bttn = qw.QPushButton('Edit Existing Curve')
        centerguidelayout.addWidget(editexistingcurve_bttn)

        savechangescurve_bttn = qw.QPushButton('Save Changes')
        centerguidelayout.addWidget(savechangescurve_bttn)

        deletecurve_bttn = qw.QPushButton('Delete CenterGuide')
        centerguidelayout.addWidget(deletecurve_bttn)


        # TUBE widgetes

        tube_header = qw.QLabel('TUBE')
        tube_header.setFont(bold_font)
        tubelayout.addWidget(tube_header)

        generatenewtube_bttn = qw.QPushButton('Generate New Tube')
        tubelayout.addWidget(generatenewtube_bttn)

        edittube_bttn = qw.QPushButton('Edit Tube')
        tubelayout.addWidget(edittube_bttn)

        savechangestube_bttn = qw.QPushButton('Save Changes')
        tubelayout.addWidget(savechangestube_bttn)

        deletetube_bttn = qw.QPushButton('Delete Tube')
        tubelayout.addWidget(deletetube_bttn)


        # CURVE GEN widgets

        gencurves_header = qw.QLabel('GENERATE CURVES')
        gencurves_header.setFont(bold_font)
        gencurveslayout.addWidget(gencurves_header)

        filltube_bttn = qw.QPushButton('Fill Tube With Curves')
        gencurveslayout.addWidget(filltube_bttn)

        editguides_bttn = qw.QPushButton('Change number of Guides')
        gencurveslayout.addWidget(editguides_bttn)




        #   adding frames

        self.layout().addWidget(characterinfo_frame)
        self.layout().addWidget(scalp_frame)
        self.layout().addWidget(centerguide_frame)
        self.layout().addWidget(tube_frame)
        self.layout().addWidget(generatecurves_frame)






dialog = SimpleGUI()
dialog.show()