import numpy as np

#/* Step One */
def JacobianIK(O):
    while( abs(endEffectorPosition — targetPosition) > EPS ):
        dO = GetDeltaOrientation()
        O += dO * h  # T=O+dO*h

#/* Step Two */
def GetDeltaOrientation():
    Jt = GetJacobianTranspose()
    V = targetPosition — endEffectorPosition
    dO = Jt * V  # Matrix-Vector Mult.
    return dO


#/* Step Three */
def GetJacobianTranspose():
    J_A = np.cross(rotAxisA, endEffectorPos — jointAPos)
    J_B = np.cross(rotAxisB, endEffectorPos — jointBPos)
    J_C = np.cross(rotAxisC, endEffectorPos — jointCPos)
    J = np.empty()
    J.np.append(J_A, axis=0)
    J.np.append(J_B, axis=0)
    J.np.append(J_C, axis=0)
    return J