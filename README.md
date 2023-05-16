# Maya Joint Symmetry Tool

[Japanese](README-ja.md)

This is a Maya Python script that provides a simple UI for setting up a symmetry constraint between two selected joints. The `create_joint_symmetry_ui.py` script will create a UI that allows the user to specify the axis of symmetry (X, Y, or Z), and will call the `create_joint_symmetry.py` script to set up the symmetry constraint.

## Environment

- Windows 10
- Maya 2020

## Installation

1. Download zip file from [latest release](https://github.com/NinaMina2737/maya-joint-symmetry-tool/releases/latest). and extract the archive.
2. Move `maya-joint-symmetry-tool` folder to your Maya's script folder (e.g. `C:\Users\<user>\Documents\maya\scripts`)
3. Drag and drop `install.py` to Maya's viewport.
4. Then, you can see `jointSymmetryTool` in your active shelf.

## Usage

To use the Joint Symmetry Tool:

1. Run `componentRelativeScale` from your shelf.
2. Select the two joints you want to set up a symmetry constraint between. The first joint you select will be the source joint, and the second joint you select will be the target joint.
3. Select the axis of symmetry (X, Y, or Z).
4. Click the `Set Up Symmetry Constraint` button.

If successful, the script will create a symmetry constraint node between the two selected joints and set up the necessary offset attributes on the target joint. If an error occurs, a warning will be displayed in the Maya Script Editor.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
