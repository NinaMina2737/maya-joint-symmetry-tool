#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

import maya.cmds as cmds

def create_joint_symmetry():
    # type: () -> None
    """
    Sets up a symmetry constraint between two selected joints in Maya.
    """
    # Get the selected joints
    selected_joints = cmds.ls(selection=True)

    # Check if the selected joints are valid
    if not all(cmds.objectType(joint) == "joint" for joint in selected_joints):
        cmds.warning("Please select two valid joints to set up a symmetry constraint.")
        return

    # Check if two joints are selected
    if len(selected_joints) != 2:
        cmds.warning("Please select two joints to set up a symmetry constraint.")
        return

    # Set up the symmetry constraint between the selected joints
    try:
        set_symmetry_constraint(selected_joints[0], selected_joints[1])
    except Exception as e:
        # Print the error message
        cmds.warning("An error occurred: {}".format(str(e)))

def set_symmetry_constraint(source_joint, target_joint):
    # type: (str, str) -> None
    """
    Creates a symmetry constraint between the source and target joints.
    """
    # Check if the source joint and target joint have the same parent
    if cmds.listRelatives(source_joint, parent=True) == cmds.listRelatives(target_joint, parent=True):
        cmds.warning("The source joint and target joint have the same parent. Please select a different target joint.")
        return

    # Check if the source joint already has a symmetry constraint
    if cmds.objExists(source_joint + "_symmetry_constraint"):
        cmds.warning("The source joint already has a symmetry constraint. Please delete it before running this script.")
        return

    # Check if the target joint already has a symmetry constraint
    if cmds.objExists(target_joint + "_symmetry_constraint"):
        cmds.warning("The target joint already has a symmetry constraint. Please delete it before running this script.")
        return

    # Add the offset attributes to the target joint
    cmds.addAttr(target_joint, longName="offsetTranslate", attributeType="double3", keyable=True, defaultValue=[0.0, 0.0, 0.0])
    cmds.addAttr(target_joint, longName="offsetRotate", attributeType="double3", keyable=True, defaultValue=[0.0, 0.0, 0.0])
    cmds.addAttr(target_joint, longName="offsetScale", attributeType="double3", keyable=True, defaultValue=[1.0, 1.0, 1.0])

    # Create a name for the symmetry constraint node
    symmetry_constraint_name = target_joint + "_symmetry_constraint"

    # Create the symmetry constraint and parent it to the target joint
    sym_node = cmds.createNode("symmetryConstraint", name=symmetry_constraint_name, parent=target_joint)

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

    def delete_pma_nodes():
        # type: () -> None
        # Delete the pma nodes
        cmds.delete(target_joint + "_pma_translate")
        cmds.delete(target_joint + "_pma_rotate")
        cmds.delete(target_joint + "_pma_scale")

        for job_id in job_id_list:
            # Delete the script job
            cmds.scriptJob(kill=job_id, force=True)

    # Create a list to store the script job IDs
    job_id_list = [] # type: List[int]

    # Create a script job to delete the pma nodes when the symmetry constraint node is deleted
    job_id_list.append(cmds.scriptJob(nodeDeleted=[sym_node, delete_pma_nodes], runOnce=True, killWithScene=True))

    # Create a script job to delete the pma nodes when the target joint is deleted
    job_id_list.append(cmds.scriptJob(nodeDeleted=[target_joint, delete_pma_nodes], runOnce=True, killWithScene=True))

    # Create a script job to delete the pma nodes when the source joint is deleted
    job_id_list.append(cmds.scriptJob(nodeDeleted=[source_joint, delete_pma_nodes], runOnce=True, killWithScene=True))

    # Create a script job to delete the pma nodes when scene opens
    job_id_list.append(cmds.scriptJob(event=["SceneOpened", delete_pma_nodes], runOnce=True, killWithScene=True))

    # Create a script job to delete the pma nodes when Maya is closed
    job_id_list.append(cmds.scriptJob(event=["quitApplication", delete_pma_nodes], runOnce=True, killWithScene=True))

    # Create new attributes on the target joint to store the script job IDs
    cmds.addAttr(target_joint, longName="symmetryConstraintScriptJobIDs", attributeType="long", multi=True)

    # Set the script job IDs on the target joint
    for i, job_id in enumerate(job_id_list):
        cmds.setAttr(target_joint + ".symmetryConstraintScriptJobIDs[" + str(i) + "]", job_id)

def execute():
    # type: () -> None
    try:
        # Open an undo chunk
        with cmds.undoInfo(openChunk=True):
            # Create the joint symmetry
            create_joint_symmetry()
    except Exception as e:
        # Print the error message
        cmds.warning("An error occurred: {}".format(str(e)))
    finally:
        # Close the undo chunk
        cmds.undoInfo(closeChunk=True)

if __name__ == '__main__':
    # Execute the script
    execute()
