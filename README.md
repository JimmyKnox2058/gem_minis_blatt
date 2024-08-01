# Wortanalyse der gemeinsamen Ministerialblätter

# Ziele des README
 - Zielsetzung: Was wollen wir vom README? Ergebnisse? Beschreibung der Methodik? Anleitung?
 - Nebenziele: Ansprechende Darstellung, (implizite) Betonung der Fähigkeiten
![Screenshot (33)](https://github.com/user-attachments/assets/60db6cea-051f-4f54-bd8b-84d9522c297b)

# Strukturierung
 - Kurzbeschreibung des Projekts
 - Ergebnisse (evtl. vor den Methoden?)
 - Ausführlicheres Eingehen auf verwendete Methoden
 - Analyse/Kommentare zu Problemen
 - Anleitung für eigene Ausführung des Codes
![BW_Metzger](https://github.com/user-attachments/assets/06ad5ad5-f2ee-4bb6-a2e9-58307aa2ffad)
![Studentenfutter](https://github.com/user-attachments/assets/27f3e99a-da77-4775-b4f2-24f8f2b859c9)

# Ideen für Aufhübschung/Bilder
 - Wordclouds
 - Topic Clouds
 - Spurious Correlations
 - Weitere Funktionalität des Dashboards

## Kurzbeschreibung des Projekts
 Das Projekt ist ein Lernprojekt, dessen Inhalt die Wortanalyse von ca. 2700 Ausgaben des *gemeinsamen Ministerialblattes* ist. Die *gemeinsamen Ministerialblätter* sind die seit 1950 von der Bundesregierung Deutschlands herausgegebenen Verwaltungsanweisungen - diese wurden auf der Website fragdenstaat.de als .pdf veröffentlicht.

 Teilaspekte, mit denen wir uns auseinandergesetzt haben, sind:
- Beschaffung, Bereinigung und Verarbeitung der Textdaten
- Natural Language Processing
- statistische Methoden und Topic Modelling
- Darstellung der Ergebnisse mit Word Clouds, Graphen und Tabellen in einem Dashboard

## Gemeinsames Ministerialblatt von www.fragdenstaat.de
### Vorwort
www.fragdenstaat.de hat alle "Gemeinsames Ministerialblatt" kostenlos veröffentlicht. Die juristischen Zusammenhänge dazu werden auf ihrer Webseite, sowie Wikipedia und anderen Nachrichtenmedien veröffentlicht. Der Inhalt der Daten ist nicht urheberrechtlich geschützt, auch die Weiterverarbeitung der Daten ist erlaubt.

### Datenbeschaffung
Mit den Dateien DL_doc_list.py, DL_doc_instance.py und DL_pdf.py wurden die Daten vom Server von www.fragdenstaat.de runtergeladen. Dabei wurde die bereitgestellte API von www.fragdenstaat.de benutzt.

## Zusatz für das Projekt und der Datenaustausch
Die Daten können runtergeladen werden, was relativ lange dauert (im Stundenbereich). Die bereitgestellten Daten sind die Ergebnisse von den Downloads und müssen nicht noch einmal durchgeführt werden. Leider sind vor allem die PDFs zu groß und werden nicht bereitgestellt.

In den Unterordnern des data Ordners befinden sich Dateien gezippt. Diese müssen so entpackt werden, dass diese Dateien in dem Ordner der .zip sind, nicht in einem neuen Unterordner.

## Erklärung zu den Python-Skripten für den Download
init_download.py
Diese führt die Python-Programme aus, die für den Download der Daten benötigt werden.

Es wird das Inhaltsverzeichnis, anhand der Vorgaben der API, stückweise geladen und danach zu einem Inhaltsverzeichnis zusammengeführt und gespeichert (data/data/list_doc.json)
Von dieser Datei werden die gewünschten Dokumente gesucht und geladen.
Zuerst werden die Dateien als json geladen und dann zu einer einzigen json mit allen Dokumenten zusammengefasst. (data/data/docs.json)
Zusätzlich werden die PDFs aller Dokumente geladen und in data/docs_pdf gespeichert.

## Datenstruktur im Ordner fragdenstaat
### für die Programme benötigte/benutzte Unterordner:
fragdenstaat (root)
-data
--data
--docs_json
--docs_pdf
--pickle_jar
-pages

### andere Ordner für Archivierung und Entwicklung
fragdenstaat (root)
-daten-grab
-daten-austausch

### Erkärung
fragdenstaat (root)
Hier kommen readme.md und ähnliche grundlegende Dokumente rein.
Sowie die benötigten Python-Dateien für grundlegende Funktionen, z.B. Initiierung des Downloads, Starten des Dash-Boards...

-data
Python Dateien für die Datenverarbeitung
-- diverse Unterordner ausschließlich für Daten

-pages
Für Dash-Board benötigte Dateien.

### Dateien in Root
inits können ausgeführt werden, wenn die Unterordner in /data leer sind.
Alle Daten werden geladen und verarbeitet.
in dieser Reihenfolge ausführen:
init_download
init_pickleing
init_comp_pdf

für das DashBoard
homeDash ausführen

für die PDF Analyse und stöbern inden Daten von der Präsentation über PDF
compare_pdf öffnen
