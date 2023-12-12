import sys
sys.path.append('./RECOTOOLS/')
# import project_metadata
from core import system_run, survey_metadata, run_collection
import datalibrary
import processor
import systems.pelisystem as peli
import numpy as np
import pandas as pd
from os.path import exists

metadata_filename="metadata.csv"

runlib = pd.read_csv( metadata_filename )

# Add new columns for DF and OSDF
runlib["DF"] = ""
runlib["OSDF"] = ""
runlib["COUNT"] = 0
runlib["EXP"] = 0.0
runlib["RATE"] = 0.0
runlib["RATIO"] = 0.0

for index, row in runlib.iterrows():
    print(index, row)

    runfilename =  row["FILE"]
    osfilename = row["OSFILE"]
    chmap = row["CHMAP"]
    
    runfilename = runfilename.strip()
    osfilename = osfilename.strip()
  
    if ".dat" not in runfilename: runfilename += ".dat"
    if ".dat" not in osfilename: osfilename += ".dat"

    row["DF"] = runfilename.replace(".dat","") + "_df.csv"
    row["OSDF"] = osfilename.replace(".dat","") + "_df.csv"

    if not exists(row["DF"]):
        print(" -> Building Run Dataset")
        runhits = peli.read_detector_run(runfilename)
        #runhits = CalcAttributes(runhits,chmap)
        runhits=peli.prepare_frame(runhits,row)
        runhits.to_csv( row["DF"] )
    else:
        print(" -> Run DF already found:", row["DF"])
        runhits = pd.read_csv( row["DF"] )
        #runhits = CalcAttributes(runhits, chmap)
        runhits=peli.prepare_frame(runhits,row)
        # print(runhits.attrs)
#         assert False

    if not exists(row["OSDF"]):
        print(" -> Building OS Dataset")
        print(osfilename)
        oshits = peli.read_detector_run(osfilename)

        runhits=peli.prepare_frame(runhits,row)
        oshits.to_csv( row["OSDF"] )
    else:
        print(" -> OS DF already found:",row["OSDF"])
        oshits = pd.read_csv( row["OSDF"] )

        runhits=peli.prepare_frame(runhits,row)

    # print(runhits.attrs)
#     assert False
    row["COUNT"] = runhits.attrs["total"]
    row["EXP"] = runhits.attrs["exp"]
    row["RATE"] = runhits.attrs["rate"]
    #row["RATIO"] = runhits.attrs["rate"]/oshits.attrs["rate"]

    # Fix to new pandas setting
    # runlib.at[index] = row
    # runlib.loc[row.index[0]] = row
    # runlib.loc[row.index[index]] = row
    runlib.iloc[index] = row

runlib.to_csv( metadata_filename )
