#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

import maya.cmds as cmds

def create_joint_symmetry(axis="X"):
    # type: (str) -> None
    """
    Sets up a symmetry constraint between two selected joints in Maya.
    """
    # Get the selected joints
    selected_joints = cmds.ls(selection=True)

    # Check if two joints are selected
    if len(selected_joints) != 2:
        cmds.warning("Please select two joints to set up a symmetry constraint.")
        return

    # Check if the selected joints are valid
    if not all(cmds.objectType(joint) == "joint" for joint in selected_joints):
        cmds.warning("Please select two valid joints to set up a symmetry constraint.")
        return

    # Set up the symmetry constraint between the selected joints
    try:
        set_symmetry_constraint(selected_joints[0], selected_joints[1], axis)
    except Exception as e:
        # Print the error message
        cmds.warning("An error occurred: {}".format(str(e)))

def set_symmetry_constraint(source_joint, target_joint, axis="X"):
    # type: (str, str, str) -> None
    """
    Creates a symmetry constraint between the source and target joints.
    """
    # Check if the source joint already has a symmetry constraint
    if cmds.objExists(source_joint + "_symmetry_constraint"):
        cmds.warning("The source joint already has a symmetry constraint. Please delete it before running this script.")
        return

    # Check if the target joint already has a symmetry constraint
    if cmds.objExists(target_joint + "_symmetry_constraint"):
        cmds.warning("The target joint already has a symmetry constraint. Please delete it before running this script.")
        return

    # Check if the offset attributes already exist on the target joint
    # If they do, delete them
    if cmds.objExists(target_joint + ".offsetTranslate"):
        cmds.deleteAttr(target_joint + ".offsetTranslate")
    if cmds.objExists(target_joint + ".offsetRotate"):
        cmds.deleteAttr(target_joint + ".offsetRotate")
    if cmds.objExists(target_joint + ".offsetScale"):
        cmds.deleteAttr(target_joint + ".offsetScale")

    # Add the offset attributes to the target joint
    cmds.addAttr(target_joint, longName="offsetTranslate", attributeType="double3", keyable=True)
    cmds.addAttr(target_joint, longName="offsetTranslateX", attributeType="double", defaultValue=0.0, keyable=True, parent="offsetTranslate")
    cmds.addAttr(target_joint, longName="offsetTranslateY", attributeType="double", defaultValue=0.0, keyable=True, parent="offsetTranslate")
    cmds.addAttr(target_joint, longName="offsetTranslateZ", attributeType="double", defaultValue=0.0, keyable=True, parent="offsetTranslate")
    cmds.addAttr(target_joint, longName="offsetRotate", attributeType="double3", keyable=True)
    cmds.addAttr(target_joint, longName="offsetRotateX", attributeType="double", defaultValue=0.0, keyable=True, parent="offsetRotate")
    cmds.addAttr(target_joint, longName="offsetRotateY", attributeType="double", defaultValue=0.0, keyable=True, parent="offsetRotate")
    cmds.addAttr(target_joint, longName="offsetRotateZ", attributeType="double", defaultValue=0.0, keyable=True, parent="offsetRotate")
    cmds.addAttr(target_joint, longName="offsetScale", attributeType="double3", keyable=True)
    cmds.addAttr(target_joint, longName="offsetScaleX", attributeType="double", defaultValue=1.0, keyable=True, parent="offsetScale")
    cmds.addAttr(target_joint, longName="offsetScaleY", attributeType="double", defaultValue=1.0, keyable=True, parent="offsetScale")
    cmds.addAttr(target_joint, longName="offsetScaleZ", attributeType="double", defaultValue=1.0, keyable=True, parent="offsetScale")

    # Create a name for the symmetry constraint node
    symmetry_constraint_name = target_joint + "_symmetry_constraint"

    # Create the symmetry constraint and parent it to the target joint
    sym_node = cmds.createNode("symmetryConstraint", name=symmetry_constraint_name, parent=target_joint)

    # Set the axis attribute of the symmetry constraint
    cmds.setAttr(sym_node + ".{}Axis".format(axis.lower()), 1)

    # Set the other axis attributes to 0
    for axis_name in ["X", "Y", "Z"]:
        if axis_name != axis:
            cmds.setAttr(sym_node + ".{}Axis".format(axis_name.lower()), 0)

    # Check if plus minus average nodes already exist on the target joint
    # If they do, delete them
    if cmds.objExists(target_joint + "_pma_translate"):
        cmds.delete(target_joint + "_pma_translate")
    if cmds.objExists(target_joint + "_pma_rotate"):
        cmds.delete(target_joint + "_pma_rotate")
    if cmds.objExists(target_joint + "_pma_scale"):
        cmds.delete(target_joint + "_pma_scale")

    # Create a plus minus average node to offset the target joint
    pma_node_trans = cmds.createNode("plusMinusAverage", name=target_joint + "_pma_translate")
    pma_node_rot = cmds.createNode("plusMinusAverage", name=target_joint + "_pma_rotate")
    pma_node_scale = cmds.createNode("multiplyDivide", name=target_joint + "_pma_scale")

    # Connect the attributes between the source and target joints
    cmds.connectAttr(source_joint + ".translate", sym_node + ".targetTranslate")
    cmds.connectAttr(source_joint + ".rotate", sym_node + ".targetRotate")
    cmds.connectAttr(source_joint + ".scale", sym_node + ".targetScale")
    cmds.connectAttr(source_joint + ".parentMatrix[0]", sym_node + ".targetParentMatrix")
    cmds.connectAttr(source_joint + ".worldMatrix[0]", sym_node + ".targetWorldMatrix")
    cmds.connectAttr(source_joint + ".rotateOrder", sym_node + ".targetRotateOrder")
    cmds.connectAttr(source_joint + ".jointOrient", sym_node + ".targetJointOrient")

    # Get the offset values between the source and target joints
    mat_source = cmds.xform(source_joint, query=True, matrix=True, worldSpace=True)
    constrained_trans = cmds.getAttr(sym_node + ".constraintTranslate")[0]
    mat_target = cmds.xform(target_joint, query=True, matrix=True, worldSpace=True)
    offset_translate = [mat_target[12] - constrained_trans[0], mat_target[13] - constrained_trans[1], mat_target[14] - constrained_trans[2]]
    # Convert the matrices to euler rotations and calculate the offset
    euler_source = cmds.xform(source_joint, query=True, rotation=True, worldSpace=True)
    euler_target = cmds.xform(target_joint, query=True, rotation=True, worldSpace=True)
    offset_rotate = [euler_target[i] - euler_source[i] for i in range(3)]
    offset_scale = [mat_target[0] / mat_source[0], mat_target[5] / mat_source[5], mat_target[10] / mat_source[10]]

    # Set the offset values on the target joint
    cmds.setAttr(target_joint + ".offsetTranslate", offset_translate[0], offset_translate[1], offset_translate[2], type="double3")
    cmds.setAttr(target_joint + ".offsetRotate", offset_rotate[0], offset_rotate[1], offset_rotate[2], type="double3")
    cmds.setAttr(target_joint + ".offsetScale", offset_scale[0], offset_scale[1], offset_scale[2], type="double3")

    cmds.connectAttr(sym_node + ".constraintTranslate", pma_node_trans + ".input3D[0]")
    cmds.connectAttr(sym_node + ".constraintRotate", pma_node_rot + ".input3D[0]")
    cmds.connectAttr(sym_node + ".constraintScale", pma_node_scale + ".input1")
    cmds.connectAttr(sym_node + ".constraintRotateOrder", target_joint + ".rotateOrder")
    cmds.connectAttr(sym_node + ".targetJointOrient", target_joint + ".jointOrient")
    cmds.connectAttr(target_joint + ".parentInverseMatrix[0]", sym_node + ".constraintInverseParentWorldMatrix")
    cmds.connectAttr(target_joint + ".offsetTranslate", pma_node_trans + ".input3D[1]")
    cmds.connectAttr(target_joint + ".offsetRotate", pma_node_rot + ".input3D[1]")
    cmds.connectAttr(target_joint + ".offsetScale", pma_node_scale + ".input2")
    cmds.connectAttr(pma_node_trans + ".output3D", target_joint + ".translate")
    cmds.connectAttr(pma_node_rot + ".output3D", target_joint + ".rotate")
    cmds.connectAttr(pma_node_scale + ".output", target_joint + ".scale")

    def delete_added_elements():
        # type: () -> None
        # Delete the added attributes on the target joint if they exist
        if cmds.objExists(target_joint + ".offsetTranslate"):
            cmds.deleteAttr(target_joint + ".offsetTranslate")
        if cmds.objExists(target_joint + ".offsetRotate"):
            cmds.deleteAttr(target_joint + ".offsetRotate")
        if cmds.objExists(target_joint + ".offsetScale"):
            cmds.deleteAttr(target_joint + ".offsetScale")

        # Delete the added plus minus average nodes on the target joint if they exist
        if cmds.objExists(target_joint + "_pma_translate"):
            cmds.delete(target_joint + "_pma_translate")
        if cmds.objExists(target_joint + "_pma_rotate"):
            cmds.delete(target_joint + "_pma_rotate")
        if cmds.objExists(target_joint + "_pma_scale"):
            cmds.delete(target_joint + "_pma_scale")

        # Delete the symmetry constraint node if it exists
        if cmds.objExists(sym_node):
            cmds.delete(sym_node)

        # Delete the added attribute for the script job IDs on the target joint if it exists
        if cmds.objExists(target_joint + ".symmetryConstraintScriptJobIDs"):
            cmds.deleteAttr(target_joint + ".symmetryConstraintScriptJobIDs")

        for job_id in job_id_list:
            # Delete the script job
            cmds.scriptJob(kill=job_id, force=True)

    # Create a list to store the script job IDs
    job_id_list = [] # type: List[int]

    # Create a script job to delete the pma nodes when the symmetry constraint node is deleted
    job_id_list.append(cmds.scriptJob(nodeDeleted=[sym_node, delete_added_elements], runOnce=True, killWithScene=True))

    # Create a script job to delete the pma nodes when the target joint is deleted
    job_id_list.append(cmds.scriptJob(nodeDeleted=[target_joint, delete_added_elements], runOnce=True, killWithScene=True))

    # Create a script job to delete the pma nodes when the source joint is deleted
    job_id_list.append(cmds.scriptJob(nodeDeleted=[source_joint, delete_added_elements], runOnce=True, killWithScene=True))

    # Create a script job to delete the pma nodes when scene opens
    job_id_list.append(cmds.scriptJob(event=["SceneOpened", delete_added_elements], runOnce=True, killWithScene=True))

    # Create a script job to delete the pma nodes when Maya is closed
    job_id_list.append(cmds.scriptJob(event=["quitApplication", delete_added_elements], runOnce=True, killWithScene=True))

    # Check if the attribute already exists on the target joint
    # If it does, delete it
    if cmds.objExists(target_joint + ".symmetryConstraintScriptJobIDs"):
        cmds.deleteAttr(target_joint + ".symmetryConstraintScriptJobIDs")

    # Create new attributes on the target joint to store the script job IDs
    cmds.addAttr(target_joint, longName="symmetryConstraintScriptJobIDs", attributeType="long", multi=True)

    # Set the script job IDs on the target joint
    for i, job_id in enumerate(job_id_list):
        cmds.setAttr(target_joint + ".symmetryConstraintScriptJobIDs[" + str(i) + "]", job_id)

def execute(axis="X"):
    # type: (str) -> None
    try:
        # Open an undo chunk
        cmds.undoInfo(openChunk=True)
        # Create the joint symmetry
        create_joint_symmetry(axis=axis)
    except Exception as e:
        # Print the error message
        cmds.warning("An error occurred: {}".format(str(e)))
    finally:
        # Close the undo chunk
        cmds.undoInfo(closeChunk=True)

if __name__ == '__main__':
    # Execute the script
    execute()
