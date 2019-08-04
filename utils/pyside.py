import sys
import os
import webbrowser
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from shiboken2 import wrapInstance
from maya import OpenMayaUI as omui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from maya.app.general.mayaMixin import MayaQDockWidget

__author__ = "chris.thwaites"
__email__ = "chrthw@gmail.com"
__docs__ = "https://github.com/ChrisTwaitees/Samson"

# Maya imports
import maya.cmds as mc

# Maya Main Window Hook
MAYA_MAIN_WINDOW_PTR = omui.MQtUtil.mainWindow()
MAYA_MAIN_WINDOW = wrapInstance(long(MAYA_MAIN_WINDOW_PTR), QWidget)


# QUICK UTILS - Style
def standard_icons_dict(icon_name):
    return {"Exit": "SP_BrowserStop", "OpenFile": "SP_DialogOpenButton", "Check": "SP_DialogApplyButton",
                 "Save": "SP_DialogSaveButton", "Refresh": "SP_BrowserReload", "Add": "SP_FileDialogNewFolder",
                 "New": "SP_FileDialogNewFolder", "Delete": "SP_DialogDiscardButton", "Trash": "SP_TrashIcon",
                 "Next": "SP_ToolBarHorizontalExtensionButton", "NewTab": "SP_ToolBarHorizontalExtensionButton",
                 "Info": "SP_MessageBoxInformation", "ArrowDown": "SP_ArrowDown", "ArrowUp": "SP_ArrowUp",
                 "ArrowBack": "SP_ArrowBack", "ArrowLeft": "SP_ArrowLeft", "ArrowRight": "SP_ArrowRight",
                 "ArrowForward": "SP_ArrowForward", "Help": "SP_MessageBoxQuestion"
            }[icon_name]


def get_standard_icon(object, icon_name):
    icon_type = standard_icons_dict(icon_name)
    return object.style().standardIcon(getattr(QStyle, icon_type))


def set_application_stylesheet(app, style="dark"):
    style_dir_path = os.path.join(os.path.dirname(__file__), "data/style")
    style_path = os.path.join(style_dir_path, "%s.css" % style)
    if os.path.exists(style_path):
        with open(style_path) as f:
            style_txt = f.read().replace("%STYLE%", style_dir_path.replace("\\", "/"))
            app.setStyleSheet(style_txt)
    else:
        print "style %s not found" % style
        return



# QUICK UTILS - widgets
def create_button(**kwargs):
    btn = QPushButton(kwargs["text"])
    btn.setToolTip(kwargs["tip"])
    btn.clicked.connect(kwargs["callback"])
    return btn


def create_label(text):
    label = QLabel(text)
    font = QFont()
    font.setBold(True)
    label.setFont(font)
    label.setAlignment(Qt.AlignLeft)
    label.setAlignment(Qt.AlignTop)
    return label


def get_color():
    color = QColorDialog.getColor()
    if color.isValid():
        return color
    else:
        return None


# QUICK UTILS - Layout operations
def delete_widgets_in_layout(parent):
    for i in reversed(range(parent.layout.count())):
        parent.layout.itemAt(i).widget().setParent(None)


def set_disabled_widgets_in_layout(layout, disabled=True, protected=[]):
    for i in reversed(range(layout.count())):
        widget = layout.itemAt(i).widget()
        if widget not in protected:
            widget.setDisabled(disabled)


# SIMPLE WIDGETS - Main Windows
class SimpleDockableWindow(MayaQWidgetDockableMixin, QDialog):
    """
    Base Class for Dockable Tool Windows
    """
    def __init__(self, tool_name="SimpleDockableWindow"):
        # ensure to delete all instances before setting parent
        self.delete_instances()
        super(SimpleDockableWindow, self).__init__()
        self.setParent(MAYA_MAIN_WINDOW)

        # Attributes
        self.tool_name = tool_name

        # Setup window's properties
        self.setWindowTitle(self.tool_name)
        self.setWindowFlags(Qt.Window)
        self.resize(500, 500)

    # If it's floating or docked, this will run and delete it self when it closes.
    def dockCloseEventTriggered(self):
        self.setParent(None)
        self.deleteLater()

    # Delete any instances of this class
    def delete_instances(self):
        for widget in qApp.allWidgets():
            if type(widget).__name__ == self.__class__.__name__:
                widget.close()
                widget.setParent(None)

    def run(self):
        self.show(dockable=True)
        # self.show(dockable=True, floating=False, area='left')


class SimpleToolWindow(SimpleDockableWindow):
    """
    Base Class for Tool Windows
    """
    def __init__(self, tool_name="SimpleToolWindow", dockable=True, logger=True, stylesheet = "darkorange"):
        self.delete_instances()
        super(SimpleToolWindow, self).__init__()
        self.setParent(MAYA_MAIN_WINDOW)
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle(tool_name)

        # Dimensions
        self.width = 500
        self.height = 500
        self.setGeometry(self.width, self.height, self.width, self.height)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        # Attributes
        self.tool_name = tool_name
        self.docs = __docs__
        self.author = __author__
        self.dockable = dockable
        self.loggerVisibility = logger

        # Logger
        self.logger = Logger()
        self.logger.set_exception_handler(self.exception_handler)

        # Create UI
        self.sw_create_menu_toolbar()
        self.sw_create_layout()
        self.sw_create_widgets()
        self.center()

        # Default Style Sheet
        set_application_stylesheet(self, stylesheet)

    def sw_create_menu_toolbar(self):
        self.helpBar = SimpleHelpToolBar(self)

    def sw_create_layout(self):
        # main layout
        self.setContentsMargins(0, 0, 0, 0)
        self.simpletool_layout = QVBoxLayout()
        self.setLayout(self.simpletool_layout)

    def sw_create_widgets(self):
        self.sw_widgets_container = QWidget()
        self.sw_widgets_container.setContentsMargins(0, 0, 0, 0)
        self.sw_widgets_container.layout = QVBoxLayout()
        self.sw_widgets_container.setLayout(self.sw_widgets_container.layout)
        # adding to layouts
        self.simpletool_layout.addWidget(self.sw_widgets_container)
        if self.loggerVisibility:
            self.simpletool_layout.addWidget(self.logger)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def run(self):
        self.show(dockable=self.dockable)

    # Delete any instances of this class
    def delete_instances(self):
        for widget in qApp.allWidgets():
            if type(widget).__name__ == self.__class__.__name__:
                widget.close()
                widget.setParent(None)

    # override QLayout.addWidget
    def addWidget(self, widget):
        self.sw_widgets_container.layout.addWidget(widget)

    # logger exception handler
    def exception_handler(self, exctype, value, traceback):
        print value
        if exctype == SystemError:
            self.logger.log(str(value), debug_level="Error")
        else:
            self.logger.log(str(value), debug_level="Warning")


# SIMPLE WIDGETS - Framed Widgets
class SimpleCollapsibleWidget(QWidget):
    """
    Simple Animated Collapsible Widget
    """
    def __init__(self, title="title", collapsed=True):
        super(SimpleCollapsibleWidget, self).__init__()
        self.title = title
        self.animation_duration = 200
        self.toggle_animation = QParallelAnimationGroup()
       # self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.setContentsMargins(0, 0, 0, 0)
        self.collapsed = collapsed

        self.scw_create_layout()
        self.scw_create_widgets()


    def scw_create_layout(self):
        self.main_layout = QGridLayout()
        self.content_area = QScrollArea()
        self.widget_layout = QVBoxLayout()
        # main layout
        self.main_layout.setVerticalSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)
        # content area
        self.content_area.setLayout(self.widget_layout)
        self.content_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # start out collapsed
        self.content_area.setMaximumHeight(0)
        self.content_area.setMinimumHeight(0)

    def scw_create_widgets(self):
        self.header_line = QFrame()
        # toggle button
        self.toggle_button = QToolButton()
        self.toggle_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(Qt.RightArrow)
        self.toggle_button.setText(self.title)
        self.toggle_button.setCheckable(True)

        # header line
        self.header_line.setFrameShape(QFrame.HLine)
        self.header_line.setFrameShadow(QFrame.Sunken)
        self.header_line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # adding widgets
        self.main_layout.addWidget(self.toggle_button, 0, 0, 1, 1, Qt.AlignLeft)
        self.main_layout.addWidget(self.header_line, 0, 2, 1, 1)
        self.main_layout.addWidget(self.content_area, 1, 0, 1, 3)

        self.scw_create_animation()

    def scw_create_animation(self):
        # let the entire widget grow and shrink with its content
        self.toggle_animation.addAnimation(QPropertyAnimation(self, "minimumHeight"))
        self.toggle_animation.addAnimation(QPropertyAnimation(self, "maximumHeight"))
        self.toggle_animation.addAnimation(QPropertyAnimation(self.content_area, "maximumHeight"))
        self.toggle_button.clicked.connect(self.start_animation)

    def start_animation(self):
        checked = self.toggle_button.isChecked()
        arrow_type = Qt.DownArrow if checked else Qt.RightArrow
        direction = QAbstractAnimation.Forward if checked else QAbstractAnimation.Backward
        self.toggle_button.setArrowType(arrow_type)
        self.toggle_animation.setDirection(direction)
        self.toggle_animation.start()

    def rebuild_animation(self):
        collapsed_height = self.sizeHint().height() - self.content_area.maximumHeight()
        content_height = self.widget_layout.sizeHint().height()
        for i in range(self.toggle_animation.animationCount() - 1):
            collapsible = self.toggle_animation.animationAt(i)
            collapsible.setDuration(self.animation_duration)
            collapsible.setStartValue(collapsed_height)
            collapsible.setEndValue(collapsed_height + content_height)
        content_animation = self.toggle_animation.animationAt(self.toggle_animation.animationCount() - 1)
        content_animation.setDuration(self.animation_duration)
        content_animation.setStartValue(0)
        content_animation.setEndValue(content_height)

    # override on QLayout
    def addWidget(self, widget):
        self.widget_layout.addWidget(widget)
        self.rebuild_animation()


class SimpleHighlightWidget(QWidget):
    """
    Creates re-scaling highlight overlay to widget. Needs visibility implementation from
    built-in mouseEvent functions.
    """
    def __init__(self, parent, alpha=125):
        super(SimpleHighlightWidget, self).__init__(parent)
        self.parent = parent
        self.opacity = alpha
        self.highlight_colour = parent.palette().color(QPalette.Highlight)
        self.highlight_colour.setAlpha(alpha)

        self.palette = QPalette(parent.palette())
        self.palette.setColor(self.palette.Background, Qt.transparent)

        self.setPalette(self.palette)
        self.hide()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setOpacity(self.opacity)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(event.rect(), QBrush(self.highlight_colour))
        painter.setPen(QPen(Qt.NoPen))
        painter.end()


class SimplePanelledVBoxWidget(QFrame):
    def __init__(self):
        super(SimplePanelledVBoxWidget, self).__init__()

        self.setFrameStyle(QFrame.Panel | QFrame.Raised)

        self.widget = QWidget()
        self.widget.layout = QVBoxLayout()
        self.widget.setLayout(self.widget.layout)

        self.widget.layout.setAlignment(Qt.AlignHCenter)
        self.widget.layout.setAlignment(Qt.AlignVCenter)

        self.setLayout(self.widget.layout)

    # Override from QLayout
    def addWidget(self, widget):
        self.widget.layout.addWidget(widget)

    # Override from QWidget
    def setMaximumWidth(self, width):
        self.widget.setMaximumWidth(width)

    # Override from QWidget
    def setMinimumWidth(self, width):
        self.widget.setMinimumWidth(width)

    # Override from QWidget
    def setMaximumHeight(self, height):
        self.widget.setMaximumHeight(height)

    # Override from QWidget
    def setMinimumHeight(self, height):
        self.widget.setMinimumHeight(height)


class SimplePanelledWidget(QFrame):
    """
    Creates a raised QFrame around empty widget
    """
    def __init__(self):
        super(SimplePanelledWidget, self).__init__()

        self.setFrameStyle(QFrame.Panel | QFrame.Raised)

        self.widget = QWidget()
        self.widget.layout = QVBoxLayout()
        self.widget.setLayout(self.widget.layout)

        self.widget.layout.setAlignment(Qt.AlignHCenter)
        self.widget.layout.setAlignment(Qt.AlignVCenter)

        self.setLayout(self.widget.layout)

    # Override from QLayout
    def addWidget(self, widget):
        self.widget.layout.addWidget(widget)

    # Override from QWidget
    def setMaximumWidth(self, width):
        self.widget.setMaximumWidth(width)

    # Override from QWidget
    def setMinimumWidth(self, width):
        self.widget.setMinimumWidth(width)

    # Override from QWidget
    def setMaximumHeight(self, height):
        self.widget.setMaximumHeight(height)

    # Override from QWidget
    def setMinimumHeight(self, height):
        self.widget.setMinimumHeight(height)


# SIMPLE WIDGETS - Line Edits
class SimpleLabelledLineEdit(QWidget):
    """
    Adds In-line Label to QSimpleLineEdit
    """
    def __init__(self, label="", comment="", data_type="text", tip=""):
        super(SimpleLabelledLineEdit, self).__init__()
        self.label = label
        self.comment = comment
        self.data_type = data_type.lower()
        self.setToolTip(tip)

        self.create_layout()
        self.create_widgets()

    def create_layout(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

    def create_widgets(self):
        self.line_edit = QLineEdit(self.comment)
        self.label = QLabel(self.label)

        if self.data_type == "int" or self.data_type == "integer":
            validator = QIntValidator()
            self.line_edit.setValidator(validator)
        if self.data_type == "f" or self.data_type == "float" or self.data_type == "double":
            validator = QDoubleValidator()
            self.line_edit.setValidator(validator)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.line_edit)

    def get_entry(self):
        return self.line_edit.text()


class SimpleLabelledVectorLineEdit(QWidget):
    """
    Number of Horizontally laid out Line Edits within parent layout
    Length is dependant on number of entries on initialization.
    """
    def __init__(self, label="", data_type="text", tip="", entries=[]):
        super(SimpleLabelledVectorLineEdit, self).__init__()
        self.label = label
        self.data_type = data_type.lower()
        self.setToolTip(tip)

        self.entries = entries
        self.create_layout()
        self.create_widgets()

    def create_layout(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

    def create_widgets(self):
        # Label
        self.label = QLabel(self.label)
        self.layout.addWidget(self.label)

        # Pointer to entries
        self.items = []

        # Validator depending on data_type
        if self.data_type == "int" or self.data_type == "integer":
            validator = QIntValidator()

        if self.data_type == "f" or self.data_type == "float" or self.data_type == "double":
            validator = QDoubleValidator()

        # Initial vector widgets
        for entry in self.entries:
            line_edit = QLineEdit(str(entry))
            line_edit.setValidator(validator)
            self.layout.addWidget(line_edit)
            self.items.append(line_edit)

    def set_entries(self, entries):
        for i, entry in enumerate(self.items):
            entry.setText(str(entries[i]))

    def get_entries(self):
        return [entry.text() for entry in self.items]


class SimpleButtonVectorLineEdit(QWidget):
    """
    Number of Horizontally laid out Line Edits within parent layout
    Length is dependant on number of entries on initialization.
    """
    def __init__(self, button_label="", data_type="text", tip="", button_callback=None, entries=[]):
        super(SimpleButtonVectorLineEdit, self).__init__()
        self.button_label = button_label
        self.data_type = data_type.lower()
        self.setToolTip(tip)
        self.callback = button_callback

        self.entries = entries
        self.create_layout()
        self.create_widgets()

    def create_layout(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

    def create_widgets(self):
        # Button
        self.button = create_button(text=self.button_label,
                                    tip="",
                                    callback=self.callback)
        self.layout.addWidget(self.button)

        # Pointer to entries
        self.items = []

        # Validator depending on data_type
        self.validator = None
        if self.data_type == "int" or self.data_type == "integer":
            self.validator = QIntValidator()
        elif self.data_type == "f" or self.data_type == "float" or self.data_type == "double":
            self.validator = QDoubleValidator()

        # Initial vector widgets
        for entry in self.entries:
            line_edit = QLineEdit(str(entry))
            if self.validator:
                line_edit.setValidator(self.validator)
            self.layout.addWidget(line_edit)
            self.items.append(line_edit)

    def set_entries(self, entries):
        for i, entry in enumerate(self.items):
            if isinstance(self.validator, QDoubleValidator ):
                entry.setText(str('%.3f'%entries[i]))
            else:
                entry.setText(str(entries[i]))

    def get_entries(self):
        return [entry.text() for entry in self.items]


class SimpleCheckableLineEdit(SimpleLabelledLineEdit):
    """
    Adds In-line checkbox to QSimpleLineEdit, disabling with checkbox
    """
    def __init__(self, label="", comment="", data_type="text", tip=""):
        super(SimpleCheckableLineEdit, self).__init__(label=label, comment=comment, data_type=data_type)
        self.label = label
        self.comment = comment
        self.data_type = data_type.lower()
        self.setToolTip(tip)

    # Override over SimpleLabelledLineEdit's create_widgets()
    def create_widgets(self):
        self.line_edit = QLineEdit(self.comment)
        self.checkbox = QCheckBox(self.label)
        self.checkbox.setChecked(True)
        self.checkbox.toggled.connect(self.disable_on_check)

        if self.data_type == "int" or self.data_type == "integer":
            validator = QIntValidator()
            self.line_edit.setValidator(validator)
        if self.data_type == "f" or self.data_type == "float" or self.data_type == "double":
            validator = QDoubleValidator()
            self.line_edit.setValidator(validator)

        self.layout.addWidget(self.checkbox)
        self.layout.addWidget(SimpleVSeparator())
        self.layout.addWidget(self.line_edit)

    def disable_on_check(self):
        self.line_edit.setDisabled(not self.checkbox.isChecked())

    # Override over QCheckbox's isChecked()
    def isChecked(self):
        return self.checkbox.isChecked()

    # Override over QCheckbox's setChecked()
    def setChecked(self, bool):
        self.checkbox.setChecked(bool)

    # Connecting textChanged function
    def onTextChanged(self, command):
        self.line_edit.textChanged.connect(command)

    # Overriding and connecting checkbox toggle function
    def onCheckBoxToggle(self, command):
        self.checkbox.toggled.connect(command)

    # Overriding text return
    def text(self):
        return self.line_edit.text()


# SIMPLE WIDGETS - Checkboxes
class SimpleHTransformCheckboxes(QWidget):
    def __init__(self):
        super(SimpleHTransformCheckboxes, self).__init__()
        self.setToolTip("Select valid Transforms")

        self.create_layout()
        self.create_widgets()

    def create_layout(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

    def create_widgets(self):
        self.translation_check = QCheckBox("Translation")
        self.translation_check.setChecked(True)
        self.layout.addWidget(self.translation_check)

        self.rotation_check = QCheckBox("Rotation")
        self.rotation_check.setChecked(True)
        self.layout.addWidget(self.rotation_check)

        self.scale_check = QCheckBox("Scale")
        self.scale_check.setChecked(True)
        self.layout.addWidget(self.scale_check)

    @property
    def translation(self):
        return self.translation_check.isChecked()

    @property
    def rotation(self):
        return self.rotation_check.isChecked()

    @property
    def scale(self):
        return self.scale_check.isChecked()


class SimpleVTransformCheckboxes(QWidget):
    def __init__(self):
        super(SimpleVTransformCheckboxes, self).__init__()
        self.setToolTip("Select valid Transforms")

        self.create_layout()
        self.create_widgets()

    def create_layout(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def create_widgets(self):
        self.translation_check = QCheckBox("Translation")
        self.translation_check.setChecked(True)
        self.layout.addWidget(self.translation_check)

        self.rotation_check = QCheckBox("Rotation")
        self.rotation_check.setChecked(True)
        self.layout.addWidget(self.rotation_check)

        self.scale_check = QCheckBox("Scale")
        self.scale_check.setChecked(True)
        self.layout.addWidget(self.scale_check)

    @property
    def translation(self):
        return self.translation_check.isChecked()

    @property
    def rotation(self):
        return self.rotation_check.isChecked()

    @property
    def scale(self):
        return self.scale_check.isChecked()


# SIMPLE WIDGETS - Buttons

class SimpleLabelledButton(QWidget):
    """
    Adds Label to Button
    """
    def __init__(self, button_label="", button_callback=None, tip="", label="", reverse=False,
                 standard_icon_name=""):
        super(SimpleLabelledButton, self).__init__()
        self.button_label = button_label
        self.setToolTip(tip)
        self.button_callback = button_callback
        self.icon_name = standard_icon_name

        self.label_text = label
        self.reverse = reverse

        self.create_layout()
        self.create_widgets()

    def create_layout(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

    def create_widgets(self):
        self.button = create_button(text=self.button_label,
                                    callback = self.button_callback,
                                    tip="")
        if len(self.icon_name):
            self.button.setIcon(get_standard_icon(self, self.icon_name))
        self.label = QLabel(self.label_text)

        if self.reverse:
            self.layout.addWidget(self.label)
            self.layout.addWidget(self.button)
        else:
            self.layout.addWidget(self.button)
            self.layout.addWidget(self.label)

    def set_text(self, text):
        self.label.setText(text)


class SimpleCheckableButton(QWidget):
    def __init__(self, button_label="", button_callback=None, tip="", checkbox_label=""):
        super(SimpleCheckableButton, self).__init__()
        self.button_label = button_label
        self.checkbox_label = checkbox_label
        self.setToolTip(tip)
        self.button_callback = button_callback

        self.create_layout()
        self.create_widgets()

    def create_layout(self):
        self.layout = QHBoxLayout()
        self.checkbox_widget = QWidget()
        self.checkbox_layout = QVBoxLayout()
        self.checkbox_widget.setLayout(self.checkbox_layout)
        self.setLayout(self.layout)

    def create_widgets(self):
        self.button = create_button(text=self.button_label,
                                    callback = self.button_callback,
                                    tip="")
        self.checkbox = QCheckBox(self.checkbox_label)
        self.checkbox.setChecked(True)

        self.layout.addWidget(self.button)
        self.checkbox_layout.addWidget(self.checkbox)
        self.layout.addWidget(self.checkbox_widget)

    # Override over QCheckbox's isChecked()
    def isChecked(self):
        return self.checkbox.isChecked()

    # Override over QCheckbox's setChecked()
    def setChecked(self, bool):
        self.checkbox.setChecked(bool)

    def addCheckBox(self, checkbox_widget):
        self.checkbox_layout.addWidget(checkbox_widget)


class SimpleButtonLineEdit(QWidget):
    """
    Button with entry
    """
    def __init__(self, button_label="", button_callback=None, tip="", label="", reverse=False):
        super(SimpleButtonLineEdit, self).__init__()
        self.button_label = button_label
        self.setToolTip(tip)
        self.button_callback = button_callback

        self.label_text = label
        self.reverse = reverse

        self.create_layout()
        self.create_widgets()

    def create_layout(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

    def create_widgets(self):
        self.button = create_button(text=self.button_label,
                                    callback = self.button_callback,
                                    tip="")
        self.entry = QLineEdit(self.label_text)

        if self.reverse:
            self.layout.addWidget(self.entry)
            self.layout.addWidget(self.button)
        else:
            self.layout.addWidget(self.button)
            self.layout.addWidget(self.entry)

    def set_text(self, text):
        self.entry.setText(text)

    def get_entry(self):
        return self.entry.text()

# SIMPLE WIDGETS - User Input
class SimpleUserInput(QInputDialog):
    """
    TODO: Implement Robust User Input Getting
    maybe tricky due to needing to bind to parent UI object
    """
    def __init__(self, header="User Input"):
        super(SimpleUserInput).__init__()
        pass


# SIMPLE WIDGETS - Help Tool Bars
class SimpleHelpToolBar(QMenuBar):
    """
    Binds to QWidget, avoiding necessity to bind to QMainWindow
    """
    def __init__(self, parent):
        super(SimpleHelpToolBar, self).__init__(parent)
        self.parent = parent
        help_menu = self.addMenu("Help")

        info_icon = get_standard_icon(parent, "Help")
        help_docs = QAction(info_icon, "Help on %s" % parent.tool_name, parent)
        help_docs.triggered.connect(lambda: self.show_help())
        help_menu.addAction(help_docs)

    def show_help(self):
        webbrowser.open(self.parent.docs, new=0, autoraise=True)


# SIMPLE WIDGETS - ComboBox
class SimpleComboBox(QComboBox):
    """
    Adding items getting and unique item adding.
    """
    def __init__(self):
        super(SimpleComboBox, self).__init__()

    def get_items(self):
        return [self.itemText(i) for i in range(0, self.count())]

    @property
    def items(self):
        return self.get_items()

    @property
    def current_item(self):
        return self.currentText()

    def add_unique_item(self, item):
        # checks whether current item already exists
        existing_items = self.get_items()
        if item not in existing_items:
            self.addItem(item)

    def add_unique_items(self, items):
        # checks whether items in list already exists
        existing_items = self.get_items()
        [self.addItem(item) for item in items if item not in existing_items]


class SimpleLabelledComboBox(QWidget):
    """
    Adding items getting and unique item adding.
    """
    def __init__(self, label="TestLabel"):
        super(SimpleLabelledComboBox, self).__init__()
        self.label_text = label
        #self.items = items

        # create layout and widgets
        self.create_layout()
        self.create_widgets()

    def create_layout(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

    def create_widgets(self):
        # label
        self.label = create_label(self.label_text)
        self.layout.addWidget(self.label)

        # SimpleCombobox
        self.combobox = SimpleComboBox()
        #self.combobox.add_unique_items(self.items)
        self.layout.addWidget(self.combobox)

    def get_items(self):
        return [self.combobox.itemText(i) for i in range(0, self.combobox.count())]

    @property
    def items(self):
        return self.get_items()

    @property
    def current_item(self):
        return self.combobox.currentText()

    # OVERRIDE of SimpleComboBox's add uniques item
    def add_unique_item(self, item):
        # checks whether current item already exists
        existing_items = self.get_items()
        if item not in existing_items:
            self.combobox.addItem(item)

    def add_unique_items(self, items):
        # checks whether items in list already exists
        existing_items = self.get_items()
        [self.combobox.addItem(item) for item in items if item not in existing_items]


# SIMPLE WIDGETS - Progress Bars
class SimpleProgressBar:
    # TODO: Create PySide implementation
    def __init__(self, title=""):
        self.window = mc.window(title)
        mc.columnLayout()
        self.progressBar = mc.progressBar(width=300)
        mc.showWindow(self.window)

    def update_progress(self, progress):
        mc.progressBar(self.progressBar, edit=True, progress=progress)

    def update_status(self, status):
        mc.progressBar(self.progressBar, edit=True, status=status)

    def close(self):
        mc.deleteUI(self.progressBar)
        mc.deleteUI(self.window)


# SIMPLE WIDGETS - Separators
class SimpleHSeparator(QFrame):
    def __init__(self):
        super(SimpleHSeparator, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


class SimpleVSeparator(QFrame):
    def __init__(self):
        super(SimpleVSeparator, self).__init__()
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Sunken)


# SIMPLE WIDGETS - Collapsible
class SimpleCollapsibleBox(QWidget):
    def __init__(self, title="", expand_duration=200):
        super(SimpleCollapsibleBox, self).__init__()

        self.expand_duration = expand_duration

        self.toggle_button = QToolButton(text=title, checkable=True, checked=False)
        self.toggle_button.setStyleSheet("QToolButton { border: none; }")
        self.toggle_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(Qt.ArrowType.RightArrow)
        self.toggle_button.pressed.connect(self.on_pressed)

        self.toggle_animation = QParallelAnimationGroup(self)

        self.content_area = QScrollArea(maximumHeight=0, minimumHeight=0)
        self.content_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.content_area.setFrameShape(QFrame.NoFrame)

        lay = QVBoxLayout(self)
        lay.setSpacing(0)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.toggle_button)
        lay.addWidget(self.content_area)

        self.toggle_animation.addAnimation(QPropertyAnimation(self, b"minimumHeight"))
        self.toggle_animation.addAnimation(QPropertyAnimation(self, b"maximumHeight"))
        self.toggle_animation.addAnimation(QPropertyAnimation(self.content_area, b"maximumHeight"))


    def on_pressed(self):
        checked = self.toggle_button.isChecked()
        self.toggle_button.setArrowType(Qt.ArrowType.DownArrow if not checked else Qt.ArrowType.RightArrow)
        self.toggle_animation.setDirection(QAbstractAnimation.Forward if not checked else QAbstractAnimation.Backward)
        self.toggle_animation.start()

    def setContentLayout(self, layout):
        lay = self.content_area.layout()
        del lay
        self.content_area.setLayout(layout)
        collapsed_height = self.sizeHint().height() - self.content_area.maximumHeight()
        content_height = layout.sizeHint().height()
        for i in range(self.toggle_animation.animationCount()):
            animation = self.toggle_animation.animationAt(i)
            animation.setDuration(self.expand_duration)
            animation.setStartValue(collapsed_height)
            animation.setEndValue(collapsed_height + content_height)

        content_animation = self.toggle_animation.animationAt(self.toggle_animation.animationCount() - 1)
        content_animation.setDuration(self.expand_duration )
        content_animation.setStartValue(0)
        content_animation.setEndValue(content_height)


# SIMPLE WIDGETS - Loggers
class Logger(SimpleCollapsibleWidget):
    """
    Generic collapsible logger for user feedback.
    """
    def __init__(self, height=150):
        super(Logger, self).__init__("Logger")
        self.exception_handler = None
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        font = QFont("Verdana", 10)
        self.text = QLabel()
        self.text.setFont(font)
        self.text.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.text.setMinimumHeight(height)

        self.addWidget(self.text)

    def log(self, text, debug_level="Log"):
        self.text.setText(text)
        if debug_level == "Log":
            style_sheet = "QLabel { color : green;}"
        elif debug_level == "Warning":
            style_sheet = "QLabel { color : orange;}"
        elif debug_level == "Error":
            style_sheet = "QLabel { color  : red;}"
        else:
            style_sheet = ""
        self.text.setStyleSheet(style_sheet)

    @staticmethod
    def set_exception_handler(exception_handler):
        sys.excepthook = exception_handler


# SIMPLE WIDGETS - Frame Range
class SimpleFrameRange(QWidget):
    '''
    Simple Widget for user entry for start and end frame
    '''
    def __init__(self, start_frame=0, end_frame=99, tip=""):
        super(SimpleFrameRange, self).__init__()
        self._start_frame = str(start_frame)
        self._end_frame = str(end_frame)
        self.setToolTip(tip)

        # Build Widgets
        self.create_layout()
        self.create_widgets()

    def create_layout(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

    def create_widgets(self):
        # start frame
        start_frame_lbl = QLabel("Start frame:")
        self.layout.addWidget(start_frame_lbl)
        self.start_frame_entry = QLineEdit(self._start_frame)
        self.start_frame_entry.setValidator(QIntValidator())
        self.layout.addWidget(self.start_frame_entry)

        end_frame_lbl = QLabel("End frame:")
        self.layout.addWidget(end_frame_lbl)
        self.end_frame_entry = QLineEdit(self._end_frame)
        self.end_frame_entry.setValidator(QIntValidator())
        self.layout.addWidget(self.end_frame_entry)

    # Start frame
    @property
    def start_frame(self):
        return self.start_frame_entry.text()

    # End frame
    @property
    def end_frame(self):
        return self.end_frame_entry.text()


# SIMPLE WIDGET - FileBrowsing
class SimpleDirectoryBrowser(QWidget):
    def __init__(self, label="", directory="", tip="", isCheckable=False):
        super(SimpleDirectoryBrowser, self).__init__()
        self._isCheckable = isCheckable
        self.label_text = label
        self.directory_text = directory
        self.setToolTip(tip)

        self.create_layout()
        self.create_widgets()

    def create_layout(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

    def create_widgets(self):
        self._directory = QLineEdit(self.directory_text)
        self.label = QLabel(self.label_text)
        self.file_browse_btn = QPushButton()

        if self._isCheckable:
            self.checkbox = QCheckBox()
            self.checkbox.setChecked(True)
            self.checkbox.toggled.connect(self.validate_check)
            self.layout.addWidget(self.checkbox)
            self.layout.addWidget(SimpleVSeparator())

        self.layout.addWidget(self.label)

        self.layout.addWidget(self._directory)

        self.layout.addWidget(SimpleVSeparator())

        self.file_browse_btn.setIcon(get_standard_icon(self, "OpenFile"))
        self.file_browse_btn.clicked.connect(self.get_file_directory)
        self.layout.addWidget(self.file_browse_btn)

    def get_file_directory(self):
        fileDirectory = QFileDialog()
        fileDirectory.setFileMode(QFileDialog.Directory)
        new_directory = fileDirectory.getExistingDirectory(self,"Choose Export Folder", self._directory.text())
        self._directory.setText(new_directory)

    def validate_check(self):
        self._directory.setEnabled(self.checkbox.isChecked())
        self.label.setEnabled(self.checkbox.isChecked())
        self.file_browse_btn.setEnabled(self.checkbox.isChecked())

    def onTextChanged(self, command):
        self._directory.textChanged.connect(command)

    @property
    def directory(self):
        return self._directory.text()

    def isChecked(self):
        if self._isCheckable:
            return self.checkbox.isChecked()
        else:
            return False

# SIMPLE WIDGETS - Color

class SimpleColorPicker(QColorDialog):
    def __init__(self):
        super(SimpleColorPicker, self).__init__()

    # Override of QColorDialog's getColor
    def getColor(self):
        return self.getColor()


# SIMPLE WIDGETS - RadioButtons

class SimpleRadioButtons(QWidget):
    def __init__(self, buttons=[], label=""):
        super(SimpleRadioButtons, self).__init__()

        self._button_labels = buttons
        self._buttons = []
        self._label = label
        self.create_layout()
        self.create_widgets()

    def create_layout(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def create_widgets(self):
        if len(self._label):
            self.label = create_label(self._label)
            self.layout.addWidget(self.label)
        for button in self._button_labels:
            new_button = QRadioButton(button)
            self.layout.addWidget(new_button)
            self._buttons.append(new_button)
        self._buttons[0].setChecked(True)

    # override of
    def get_checked(self):
        for button in self._buttons:
            if button.isChecked():
                return button


    def on_clicked(self, callback):
        for button in self._buttons:
            button.toggled.connect(callback)


# SIMPLE WIDGETS - Image Viewer
class SimpleImage(QWidget):
    def __init__(self, bit_depth=None):
        super(SimpleImage, self).__init__()
        # Fetching image format:
        self.image_format = self._get_bit_depth(bit_depth)

        # Creating parent layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Adding widgets
        self.create_widgets()

    @staticmethod
    def _get_bit_depth(bit_depth):
        if bit_depth:
            if bit_depth == "32" or bit_depth == "32RGB":
                return QImage.Format_RGB32
            elif bit_depth == "16" or bit_depth == "16RGB":
                return QImage.Format_RGB16
            elif bit_depth == "8" or bit_depth == "8RGB":
                return QImage.Format_Indexed8
            else:
                return QImage.Format_RGB32
        else:
            return QImage.Format_Indexed8

    @property
    def width(self):
        return self.image.width()

    @property
    def height(self):
        return self.image.height()

    def create_widgets(self):
        self.label = QLabel(self)
        self.image = QImage(250, 250, self.image_format)
        self.layout.addWidget(self.label)
        self.pixmap = QPixmap.fromImage(self.image)
        self.label.setPixmap(self.pixmap)

        self.set_black()

    def set_black(self):  # sets self.image to black
        color = QColor(0.0, 0.0, 0.0, 1)
        self.image.fill(color)
        self.refresh_image()

    def set_size(self, width, height):
        self.image = QImage(width, height, self.image_format)
        self.refresh_image()

    def set_pixel(self, x, y, color):
        # if using 8 bit depth, colorTable needs to be used
        if self.image_format == QImage.Format_Indexed8:
            color = qRgb(int(color[0]), int(color[1]), int(color[2]))
            # check whether color is already available in colorTable
            if color in self.image.colorTable():
                color_index = self.image.colorTable().index(color)
            else:
                color_index = len(self.image.colorTable())
                self.image.setColor(color_index, color)
            color = color_index
            self.image.setPixel(x, y, color)
        else:
            color = QColor(color[0], color[1], color[2])
            self.image.setPixelColor(x, y, color)
        self.refresh_image()


    def set_bit_depth(self, bit_depth):
        self.image_format = self._get_bit_depth(bit_depth)
        self.image = self.image.convertToFormat(self.image_format)
        self.refresh_image()

    def refresh_image(self):
        self.pixmap = QPixmap.fromImage(self.image)
        self.label.setPixmap(self.pixmap)

    def export(self, path):
        format = "PNG"
        self.image.save(path, format)
