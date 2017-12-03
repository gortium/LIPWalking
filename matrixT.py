import numpy as np

#variable pour les angles
teta1 = 2
teta2 = 5
teta3 = 20
teta4 = 15
teta5 = 70

#variable pour les distances
l1 = 20
l2 = 50
l3 = 15

T1L = np.matrix([[np.cos(teta1),-np.sin(teta1),0,0], [np.sin(teta1),np.cos(teta1),0,0], [0,0,1,0], [0,0,0,1]])
T2L = np.matrix([[np.cos(teta2),-np.sin(teta2),0,0], [0,0,-1,0], [np.sin(teta2),np.cos(teta2),0,0], [0,0,0,1]])
T3L = np.matrix([[np.cos(teta3),-np.sin(teta3),0,0], [np.sin(teta3),np.cos(teta3),0,0], [0,0,1,l1], [0,0,0,1]])
T4L = np.matrix([[np.cos(teta4),-np.sin(teta4),0,0], [np.sin(teta4),np.cos(teta4),0,0], [0,0,1,l2], [0,0,0,1]])
T5L = np.matrix([[np.cos(teta5),-np.sin(teta5),0,l3], [0,0,1,0], [-np.sin(teta5),-np.cos(teta5),0,0], [0,0,0,1]])

T1R = np.matrix([[np.cos(teta1),-np.sin(teta1),0,0], [np.sin(teta1),np.cos(teta1),0,0], [0,0,1,0], [0,0,0,1]])
T2R = np.matrix([[np.cos(teta2),-np.sin(teta2),0,0], [0,0,-1,0], [-np.sin(teta2),-np.cos(teta2),0,0], [0,0,0,1]])
T3R = np.matrix([[np.cos(teta3),-np.sin(teta3),0,0], [np.sin(teta3),np.cos(teta3),0,0], [0,0,1,l1], [0,0,0,1]])
T4R = np.matrix([[np.cos(teta4),-np.sin(teta4),0,0], [np.sin(teta4),np.cos(teta4),0,0], [0,0,1,l2], [0,0,0,1]])
T5R = np.matrix([[np.cos(teta5),-np.sin(teta5),0,l3], [0,0,1,0], [np.sin(teta5),np.cos(teta5),0,0], [0,0,0,1]])



TFL = (T1L*T2L*T3L*T4L*T5L)
TFR = (T1R*T2R*T3R*T4R*T5R)

