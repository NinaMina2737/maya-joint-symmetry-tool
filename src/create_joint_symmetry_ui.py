import maya.cmds as cmds

from maya.app.general.mayaMixin import MayaQWidgetBaseMixin
from PySide2 import QtCore, QtWidgets

import create_joint_symmetry as cjs
reload(cjs)

class JointSymmetryUI(MayaQWidgetBaseMixin, QtWidgets.QWidget):
    def __init__(self):
        super(self.__class__, self).__init__()

        # Set the window title and size
        self.setWindowTitle("Joint Symmetry")
        self.resize(300, 120)

        # Create a label for the axis of symmetry
        self.axis_label = QtWidgets.QLabel("Axis of Symmetry:")
        self.axis_label.setAlignment(QtCore.Qt.AlignCenter)

        # Create a combo box for the axis of symmetry
        self.axis_combo = QtWidgets.QComboBox()
        self.axis_combo.addItems(["X", "Y", "Z"])
        self.axis_combo.setCurrentIndex(0)

        # Create a button to set up the symmetry constraint
        self.symmetry_button = QtWidgets.QPushButton("Set Up Symmetry Constraint")
        self.symmetry_button.clicked.connect(self.create_joint_symmetry)

        # Create a layout for the axis of symmetry
        self.axis_layout = QtWidgets.QHBoxLayout()
        self.axis_layout.addWidget(self.axis_label)
        self.axis_layout.addWidget(self.axis_combo)

        # Create a layout for the button
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.addWidget(self.symmetry_button)

        # Create a main layout for the window
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(self.axis_layout)
        self.main_layout.addLayout(self.button_layout)

        # Set the main layout for the window
        self.setLayout(self.main_layout)

    def create_joint_symmetry(self):
        # type: (str) -> None
        """
        Creates a joint symmetry constraint on the selected joints.
        """
        axis = self.axis_combo.currentText()
        cjs.execute(axis=axis)

def execute():
    # type: () -> None
    """
    Executes the joint symmetry UI.
    """
    try:
        # Check if the window already exists
        if cmds.window("joint_symmetry_window", exists=True):
            cmds.deleteUI("joint_symmetry_window")

        # Create the window
        window = JointSymmetryUI()
        window.show()
    except Exception as e:
        # Print the error message
        cmds.warning("An error occurred: {}".format(str(e)))

if __name__ == "__main__":
    execute()
