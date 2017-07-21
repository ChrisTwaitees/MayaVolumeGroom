import PySide2.QtCore as qc
import PySide2.QtGui as qg
import PySide2.QtWidgets as qw


class SimpleGUI(qw.QDialog):
    def __init__(self):
        qw.QDialog.__init__(self)
        self.setWindowTitle('Samson')
        self.setWindowFlags(qc.Qt.WindowStaysOnTopHint)
        self.setModal(False)
        self.setMinimumHeight(250)
        self.setMinimumWidth(300)

        self.setLayout(qw.QVBoxLayout())
        self.layout().setContentsMargins(5,5,5,5)
        self.layout().setSpacing(5)



        # adding layouts

        self.scalplayout = qw.QVBoxLayout()
        self.centerguidelayout = qw.QVBoxLayout()
        self.tubelayout = qw.QVBoxLayout()
        self.gencurveslayout = qw.QVBoxLayout()


        # scalplayout widgets

        voronoi_bttn = qw.QPushButton('Voronoi Surface')
        self.scalplayout.addWidget(voronoi_bttn)

        refreshscalp_bttn = qw.QPushButton('Refresh')
        self.scalplayout.addWidget(refreshscalp_bttn)

        exportregionmap_bttn = qw.QPushButton('Export Region Map')
        self.scalplayout.addWidget(exportregionmap_bttn)


        # centerguide widgets

        generatecurve_bttn = qw.QPushButton('Generate New Curve')
        self.centerguidelayout.addWidget(generatecurve_bttn)

        rebuildcurve_bttn = qw.QPushButton('Rebuild Curve')
        self.centerguidelayout.addWidget(rebuildcurve_bttn)

        editexistingcurve_bttn = qw.QPushButton('Edit Existing Curve')
        self.centerguidelayout.addWidget(editexistingcurve_bttn)

        savechangescurve_bttn = qw.QPushButton('Save Changes')
        self.centerguidelayout.addWidget(savechangescurve_bttn)

        deletecurve_bttn = qw.QPushButton('Delete CenterGuide')
        self.centerguidelayout.addWidget(deletecurve_bttn)


        # tube widgetes

        generatenewtube_bttn = qw.QPushButton('Generate New Tube')
        self.tubelayout.addWidget(generatenewtube_bttn)

        edittube_bttn = qw.QPushButton('Edit Tube')
        self.tubelayout.addWidget(edittube_bttn)

        savechangestube_bttn = qw.QPushButton('Save Changes')
        self.tubelayout.addWidget(savechangestube_bttn)

        deletetube_bttn = qw.QPushButton('Delete Tube')
        self.tubelayout.addWidget(deletetube_bttn)


        # curvegen widgets

        filltube_bttn = qw.QPushButton('Fill Tube With Curves')
        self.gencurveslayout.addWidget(filltube_bttn)

        editguides_bttn = qw.QPushButton('Change number of Guides')
        self.gencurveslayout.addWidget(editguides_bttn)




        #   adding layouts

        self.layout().addLayout(self.scalplayout)
        self.layout().addLayout(self.centerguidelayout)
        self.layout().addLayout(self.tubelayout)
        self.layout().addLayout(self.gencurveslayout)
        





dialog = SimpleGUI()
dialog.show()