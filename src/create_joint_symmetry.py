#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

import maya.cmds as cmds

def create_joint_symmetry() -> None:
    """
    Sets up a symmetry constraint between two selected joints in Maya.
    """
    # Get the selected joints
    selected_joints = cmds.ls(selection=True)

    # Set up the symmetry constraint between the selected joints
    set_symmetry_constraint(selected_joints[0], selected_joints[1])

def set_symmetry_constraint(source_joint: str, target_joint: str) -> None:
    """
    Creates a symmetry constraint between the source and target joints.
    """
    # Create a name for the symmetry constraint node
    symmetry_constraint_name = target_joint + "_symmetry_constraint"

    # Create the symmetry constraint and parent it to the target joint
    sym_node = cmds.createNode("symmetryConstraint", name=symmetry_constraint_name, parent=target_joint)

    # Connect the attributes between the source and target joints
    cmds.connectAttr(source_joint + ".translate", sym_node + ".targetTranslate")
    cmds.connectAttr(source_joint + ".rotate", sym_node + ".targetRotate")
    cmds.connectAttr(source_joint + ".scale", sym_node + ".targetScale")
    cmds.connectAttr(source_joint + ".parentMatrix[0]", sym_node + ".targetParentMatrix")
    cmds.connectAttr(source_joint + ".worldMatrix[0]", sym_node + ".targetWorldMatrix")
    cmds.connectAttr(source_joint + ".rotateOrder", sym_node + ".targetRotateOrder")
    cmds.connectAttr(source_joint + ".jointOrient", sym_node + ".targetJointOrient")
    cmds.connectAttr(sym_node + ".constraintTranslate", target_joint + ".translate")
    cmds.connectAttr(sym_node + ".constraintRotate", target_joint + ".rotate")
    cmds.connectAttr(sym_node + ".constraintScale", target_joint + ".scale")
    cmds.connectAttr(sym_node + ".constraintRotateOrder", target_joint + ".rotateOrder")
    cmds.connectAttr(sym_node + ".targetJointOrient", target_joint + ".jointOrient")
    cmds.connectAttr(target_joint + ".parentInverseMatrix[0]", sym_node + ".constraintInverseParentWorldMatrix")

def execute() -> None:
    create_joint_symmetry()

if __name__ == '__main__':
    execute()
