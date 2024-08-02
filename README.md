# Wortanalyse der gemeinsamen Ministerialblätter
 ## Kurzbeschreibung des Projekts
 Das Projekt ist ein Lernprojekt von [Michael Heinrich](https://github.com/JimmyKnox2058) und [Thomas Voss](https://github.com/Thomas-Voss), dessen Inhalt die Wortanalyse von ca. 2700 Ausgaben des *gemeinsamen Ministerialblattes* ist. Die *gemeinsamen Ministerialblätter* sind die seit 1950 von der Bundesregierung Deutschlands herausgegebenen Verwaltungsanweisungen - diese wurden auf der Website fragdenstaat.de als .pdf veröffentlicht.
 
  ![Screenshot (33)](https://github.com/user-attachments/assets/60db6cea-051f-4f54-bd8b-84d9522c297b) 
            
 Teilaspekte, mit denen wir uns auseinandergesetzt haben, sind:
- Beschaffung, Bereinigung und Verarbeitung der Textdaten
- Natural Language Processing
- statistische Methoden und Topic Modelling
- Darstellung der Ergebnisse mit Word Clouds, Graphen und Tabellen in einem Dashboard

## Statistische Datenverarbeitung und Darstellung
Aus den Daten haben wir mehrere quantitative Informationen erstellt und zusammengetragen:
 - Zusammenfassung der wichtigsten Themen jedes Jahres in Word Clouds
   
   ![topiccloud](https://github.com/user-attachments/assets/31ae06e4-55d5-4f71-916c-33f2ccd2d593)

 - Ermittlung verwandter Begriffe durch Topic Modelling und Zusammenfassung verschiedener Themen in Word Clouds (Bsp: 1950)
   
   ![worldcloud1950](https://github.com/user-attachments/assets/7a32cc98-e0a7-4ab4-97ae-b5f7a02239fc)

 - Ermittlung der Worthäufigkeiten nach Jahr und Darstellung des Verlaufs in Diagrammen
 - Finden von 'Spurious Correlations', als zufälligerweise stark korrelierter Begriffe, die keinen kausalen Zusammenhang erkennen lassen:
  ### Einführung der Gulaschkanone
   ![BW_Metzger](https://github.com/user-attachments/assets/06ad5ad5-f2ee-4bb6-a2e9-58307aa2ffad)

   ### Studentenfutter
   ![Studentenfutter](https://github.com/user-attachments/assets/27f3e99a-da77-4775-b4f2-24f8f2b859c9)
 - Darstellung der Ergebnisse in einem simplen Dashboard, interaktiv mit Auswahl von Wörtern wie der oben gezeigten. 

## Technischer Projektablauf
 - Herunterladen der gemeinsamen Ministerialblätter im .json-Format unter Nutzung der von fragdenstaat.de bereitgestellten API (Datamining)
 - Auslesen, Filtern, Lemmatisierung und Vektorisierung der einzelnen Wörter, mittels Spacy (NLP) und multiprocessing optimiert
 - Explorative Datenanalyse (EDA)
 - Zusammenfassung der Worthäufigkeiten nach Jahren in einem Pandas-Dataframe
 - Herausfiltern 'langweiliger' Begriffe wie *Bundesregierung* mit zu hoher oder niedriger Standardabweichung. Zusammen mit der Verarbeitung durch Spacy wurden so die ursprünglich 500.000 unterschiedlichen Tokens auf 3.400 Tokens reduziert.
 - Topic Modelling mittels Latent Dirichlet Allocation

## Analyse und Kommentare
 - Trotz der starken, kontextvergessenden Zusammenfassung aller Wörter einer Ausgabe finden sich durch das Topic Modelling sinnvolle Themen mit verwandten Begriffen
 - Die Lemmatisierung mittels Spacy funktioniert nur bedingt. Das liegt insbesondere an der speziellen Beamtensprache, auf die die von Spacy bereitgestellten NLP-Modelle nicht trainiert sind. Auch werden Wortarten falsch erkannt.
 - Bei der Betrachtung der Daten haben wir festgestellt, dass die Qualität der Textdaten Mängel aufweist, die bei der Digitalisierung der Texte entstanden sind. Dazu gehören unter anderem:
   - Wörter mit mehr als 10 verschiedenen "Schreibweisen" aufgrund von ORC-Fehlern
   - abgeschnitte Wortfetzen aufgrund von Zeilenumbrüchen
   - unsinnige Zeichenketten, auch mit untypischen Unicode-Symbolen

   ![gem_minis_pdf](https://github.com/user-attachments/assets/303c6f10-0180-492f-af81-9d544dd772fd)

 - Ab dem Jahr 2009 nimmt die Häufigkeit der OCR-Fehler ab, die Häufigkeit der falsch oder nicht erkannten Textblöcke nimmt jedoch zu und innerhalb eines Dokuments werden beispielsweise für ein und denselben Umlaut unterschiedliche Formatierungen verwendet. Der Grund dafür liegt darin, dass ab diesem Zeitpunkt das Bundesinnenministerium  digitale Versionen veröffentlicht hat und diese digital aus einzelnen Teildokumenten zusammengefügt hat. 

## Anleitung
### Verwendung des Dashboards
Um das Dashboard zu verwenden, muss das Repository heruntergeladen, die requirements.txt installiert und homeDash.py ausgeführt werden. Dieses Programm erzeugt ein interaktives Dashboard mit den Ergebnissen des Projekts, das unter 127.0.0.1:8050 mithilfe eines Browsers abrufbar ist. Die Word Clouds sind aus Speicherplatzgründen nur exemplarisch vorhanden, können aber mithilfe der restlichen Skripte vollständig erzeugt werden.

### Analyse der in den PDFs vorhandenen Fehler
Im Hauptordner liegt das Jupyter-Notebook compare_pdf.ipynb, das die Fehler in den Rohdaten nachvollziehbar diskutiert. Für die reine Betrachtung des Notebooks ist kein weiterer Schritt nötig - um die Fehlererkennung selber durchzuführen, müssen mithilfe der restlichen Skripte die Rohdaten heruntergeladen und verarbeitet werden.

### Vervollständigung der Daten
Um die volle Funktionalität des Dashboards herzustellen und die Fehleranalyse zu reproduzieren, müssen die Rohdaten heruntergeladen und verarbeitet werden. Hierzu liegen im Hauptordner die drei folgenden Skripte:
 - init_download.py : Dieses Skript lädt die Rohdaten, also die gemeinsamen Ministerialblätter, von [www.fragdenstaat.de](https://fragdenstaat.de/) herunter. Hinweis: Datamining, um Serversperren vorzubeugen, läd dieses Skript die Daten langsam runter. (mehrere Stunden) 
 - init_pickleing.py : Dieses Skript verarbeite die Rohdaten, erzeugt die verwendeten Statistiken und Word Clouds und speichert diese als .pickle ab. (Rechenleistungsintensiv, benutzt Multiprocessing)
 - init_comp_pdf.py : Dieses Skript bereitet weiter Fehleranalysen vor, die nicht für die homeDash.py benötigt werden. (Rechenleistungsintensiv, benutzt Multiprocessing)
#### Geschafft!
Jetzt hat das Dashboard, alle Funktionen und auch die Analysen aus dem compare_pdf.ipynb funktionieren nachvollziehbar.



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
