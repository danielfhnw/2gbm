# 2-Gelenk-Bogen-Modell
Software zum ersten Teil im msL

## Installation 

### Voraussetungen
- Python
- Python IDE (empfohlen VS Code)
- Git
- Arduino Nano Treiber

### Repository
Der Ordner mit allen Unterlagen kann mit folgendem Codezeilenbefehl kopiert werden.
```
git clone https://github.com/danielfhnw/2gbm
```
Alternativ kann auch GitHub Desktop oder die GitHub-Integration im VS Code verwendet werden.
Um in den 2gbm Ordner zu gelangen kann folgende Kommandozeileneingabe verwendet werden.
```
cd 2gbm
```

### Virtual Environement
Im 2gbm-Ordner soll nun ein virtuelles Environement erstellt werden. Dies dient dazu, dass alle Bibliotheken miteinander kompatibel bleiben und nicht durch Updates geändert werden.
```
python -m venv .venv
```
Um die nötigen Bibliotheken in das virtuelle Environement zu laden muss es zuerst aktiviert werden. Dies erfolgt über das activate-Script.
```
.venv\Scripts\activate.bat
```
Sobald das Environement aktiviert ist erscheint `(.venv)` vor dem Pfad.
Anschliessend müssen die nötigen Bibliotheken heruntergeladen werden. Dazu wird der folgende Befehl verwendet.
```
pip install -r requirements.txt
```
Sobald alles erfolgreich installiert wurde, ist das virtuelle Environement bereit.

### Environement Variable
Damit nicht in jedem Skript die COM-Ports angepasst werden müssen, werden in diesem Projekt Environement Variablen zur Speicherung verwendet. Dies hat den Vorteil, dass die Skripts updated werden können, ohne dass die COM-Ports überschrieben werden. Damit dies funktioniert muss im 2gbm-Ordner ein File erstellt werden mit dem Namen `.env`. Dies kann mit dem folgenden Befehl erstellt werden.
```
notepad .env
```
Diese Datei muss mit folgendem Inhalt gefüllt werden.
```
COM_PORT_NANO=COM3
COM_PORT_MOTOR=COM4
```
Dabei muss der COM-Port für den Nano und das Motorboard entsprechend angepasst werden.
