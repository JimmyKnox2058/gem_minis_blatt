import os
from pathlib import Path
import sys
os.chdir(Path(__file__).parent)
sys.path.append("./data")
from data import *


"""Diese Datei nur einmal starten um die Daten zu verarbeiten und für die Auswertung (Dash Board)
vorzubereiten.
Dies kann einige Zeit inanspruch nehmen.

Muss nur 1 mal ausgeführt werden!

"""

if __name__ == "__main__":
    pickleDataSpacy.pickleData() 
    makeStats.pickle_everything(*makeStats.make_stats())
    makeCorrelation.makeCorrelation()
    makeClouds.makeClouds()
    makeTopics.makeTopics()
