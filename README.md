# Joint Symmetry Tool

[Japanese](README-ja.md)

This is a Maya Python script that provides a simple UI for setting up a symmetry constraint between two selected joints. The `create_joint_symmetry_ui.py` script will create a UI that allows the user to specify the axis of symmetry (X, Y, or Z), and will call the `create_joint_symmetry.py` script to set up the symmetry constraint.

## Environment

- Windows 10
- Maya 2020

## Installation

1. Clone this repository or download the ZIP file.
2. Copy the `create_joint_symmetry_ui.py` and `create_joint_symmetry.py` scripts to your Maya scripts directory. The default location for this directory is `C:\Users\<username>\Documents\maya\scripts` on Windows and `/Users/<username>/Library/Preferences/Autodesk/maya/scripts` on macOS.
3. In Maya, open the Script Editor (`Windows > General Editors > Script Editor`).
4. In the Script Editor, select `File > Open Script` and navigate to the directory where you saved the scripts.
5. Open the `create_joint_symmetry_ui.py` script.
6. Select `File > Save Script to Shelf...` and save the script to your shelf for easy access.

## Usage

To use the Joint Symmetry Tool:

1. Click the Joint Symmetry Tool button you registered on the shelf to open the UI.
2. Select the two joints you want to set up a symmetry constraint between. The first joint you select will be the source joint, and the second joint you select will be the target joint.
3. Select the axis of symmetry (X, Y, or Z).
4. Click the `Set Up Symmetry Constraint` button.

If successful, the script will create a symmetry constraint node between the two selected joints and set up the necessary offset attributes on the target joint. If an error occurs, a warning will be displayed in the Maya Script Editor.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
