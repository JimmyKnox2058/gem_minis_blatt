import os
from pathlib import Path
import sys
os.chdir(Path(__file__).parent)
sys.path.append("./data")
from data import *

"""Diese Datei nur einmal starten um die PDF Auswertung vorzubereiten.
Dies kann einige Zeit inanspruch nehmen.

Muss nur 1 mal ausgeführt werden!

WARNING: am Ende kommen viele Nachrichten in der Konsole
"""

if __name__ == "__main__":
    compare_pdf_all.main()