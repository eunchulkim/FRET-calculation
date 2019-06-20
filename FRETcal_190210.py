print("Hellow World!")

all = [var for var in globals() if var[0] != "_"]
for var in all:
    del globals()[var]

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv

filename = ("c2s2m2l2-pheinx_real_refine-coot-12_MgNABCD.csv")
temp = pd.read_csv(filename)
temp.replace("\t", " ")
labeltemp = temp["Label"]
label2 = labeltemp.drop_duplicates(keep='first')
label3 = label2.reset_index()
label = []
label = label3["Label"]

data = temp.set_index(["Label","Element"])

result=np.array(["Dprotein","Dmol","DChl","Aprotein","Amol","AChl", "R", "FRETrate", "Kfs"])

n = len(label)

n_index = 1.55
# Gradinaru et al., Biophysics Journal 1998

for i in range(0,n):
    Donor = label[i]
    for j in range(0,n):
        Acceptor = label[j]

        if Donor != Acceptor:

            Rx = data.loc[(Donor, "MG"), "X"] - data.loc[(Acceptor, "MG"), "X"]
            Ry = data.loc[(Donor, "MG"), "Y"] - data.loc[(Acceptor, "MG"), "Y"]
            Rz = data.loc[(Donor, "MG"), "Z"] - data.loc[(Acceptor, "MG"), "Z"]
            R = (Rx ** 2 + Ry ** 2 + Rz ** 2) ** (1 / 2)
            Rux = Rx / R
            Ruy = Ry / R
            Ruz = Rz / R

                if R <= 50:

                    Dx = data.loc[(Donor, "ND"), "X"] - data.loc[(Donor, "NB"), "X"]
                    Dy = data.loc[(Donor, "ND"), "Y"] - data.loc[(Donor, "NB"), "Y"]
                    Dz = data.loc[(Donor, "ND"), "Z"] - data.loc[(Donor, "NB"), "Z"]
                    D = (Dx ** 2 + Dy ** 2 + Dz ** 2) ** (1 / 2)
                    Dux = Dx / D
                    Duy = Dy / D
                    Duz = Dz / D

                    Ax = data.loc[(Acceptor, "ND"), "X"] - data.loc[(Acceptor, "NB"), "X"]
                    Ay = data.loc[(Acceptor, "ND"), "Y"] - data.loc[(Acceptor, "NB"), "Y"]
                    Az = data.loc[(Acceptor, "ND"), "Z"] - data.loc[(Acceptor, "NB"), "Z"]
                    A = (Ax ** 2 + Ay ** 2 + Az ** 2) ** (1 / 2)
                    Aux = Ax / A
                    Auy = Ay / A
                    Auz = Az / A

                    DA = Dux * Aux + Duy * Auy + Duz * Auz
                    DR = Dux * Rux + Duy * Ruy + Duz * Ruz
                    AR = Aux * Rux + Auy * Ruy + Auz * Ruz

                    Kfs = (DA - 3 * DR * AR) ** 2

                    # constants (nm^6 ps^-1) Gradinaru et al., Biophysics Journal 1998
                    DChl = data.loc[(Donor, "MG"), "Mol"]
                    AChl = data.loc[(Acceptor, "MG"), "Mol"]

                    if DChl == "CLA":

                        if AChl == "CLA":

                            C_DA = 32.26
                            # Chl a -> Chl a
                        else:

                            C_DA = 1.11
                            # Chl a -> Chl b
                    else:
                        if AChl == "CLA":

                            C_DA = 9.61
                            # Chl b -> Chl a
                        else:

                            C_DA = 14.45
                            # Chl b -> Chl b

                    FRETrate = (C_DA * Kfs) / ((n_index ** 4) * ((R * 0.1) ** 6))
                    Dprotein = Donor.split(" ")[0]
                    Dmol = Donor.split(" ")[1]
                    Aprotein = Acceptor.split(" ")[0]
                    Amol = Acceptor.split(" ")[1]
                    result = np.vstack((result, [Dprotein, Dmol, DChl, Aprotein, Amol, AChl, R, FRETrate, Kfs]))
                print(i/n)



print(result)

np.savetxt("output.csv", result, delimiter=",", fmt='%s')