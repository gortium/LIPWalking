import numpy as np
import ForwardKinematic as fk


#/* Step One */
def JacobianIK():
    endEffectorPos = fk.TFL[3, 0:2]
    _endEffectorPosition = endEffectorPosition
    _targetPosition = targetPosition
    while( abs(_endEffectorPosition - _targetPosition) > EPS ):
        dO = GetDeltaOrientation()
        O += dO * h  # T=O+dO*h


#/* Step Two */
def GetDeltaOrientation(endEffectorPosition, targetPosition):
    _endEffectorPosition = endEffectorPosition
    _targetPosition = targetPosition

    Jt = GetJacobianTranspose()
    V = _targetPosition - _endEffectorPosition
    dO = Jt * V  # Matrix-Vector Mult.
    return dO


#/* Step Three */
def GetJacobianTranspose():
    rot1 = fk.T1L[0:2, 0:2]
    rot2 = fk.T2L[0:2, 0:2]
    rot3 = fk.T3L[0:2, 0:2]
    rot4 = fk.T4L[0:2, 0:2]
    rot5 = fk.T5L[0:2, 0:2]

    joint1Pos = (fk.T1L)[3, 0:2]
    joint2Pos = (fk.T1L*fk.T2L)[3, 0:2]
    joint3Pos = (fk.T1L*fk.T2L*fk.T3L)[3, 0:2]
    joint4Pos = (fk.T1L*fk.T2L*fk.T3L*fk.T4L)[3, 0:2]
    joint5Pos = (fk.T1L*fk.T2L*fk.T3L*fk.T4L*fk.T5L)[3, 0:2]

    J_1 = np.cross(rot1, endEffectorPos - joint1Pos)
    J_2 = np.cross(rot2, endEffectorPos - joint2Pos)
    J_3 = np.cross(rot3, endEffectorPos - joint3Pos)
    J_4 = np.cross(rot4, endEffectorPos - joint4Pos)
    J_5 = np.cross(rot5, endEffectorPos - joint5Pos)

    J = np.empty()
    J.np.append(J_1, axis=0)
    J.np.append(J_2, axis=0)
    J.np.append(J_3, axis=0)
    J.np.append(J_4, axis=0)
    J.np.append(J_5, axis=0)

    return J
