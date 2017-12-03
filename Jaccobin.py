#/* Step One */
void JacobianIK(O) {
    while( abs(endEffectorPosition — targetPosition) > EPS ) {
        dO = GetDeltaOrientation();
        O += dO * h; // T=O+dO*h
    }
}

#/* Step Two */
Vector GetDeltaOrientation() {
    Jt = GetJacobianTranspose();
    V = targetPosition — endEffectorPosition;
    dO = Jt * V; // Matrix-Vector Mult.
    return dO;
}


#/* Step Three */
Matrix GetJacobianTranspose() {
    J_A = CrossProduct(rotAxisA, endEffectorPos — jointAPos);
    J_B = CrossProduct(rotAxisB, endEffectorPos — jointBPos);
    J_C = CrossProduct(rotAxisC, endEffectorPos — jointCPos);
    J = new Matrix();
    J.addColumn(J_A);
    J.addColumn(J_B);
    J.addColumn(J_C);
    return J.transpose();
}