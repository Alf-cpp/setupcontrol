1.: Falls Kameraparameter Errors zurück geben: richtigen Treiber installieren!!!

Fragen an IC:

self.camera.GetPropertyAbsoluteValue("Brightness","Value",BrightnessValue)  #Funktioniert nicht, warum???

Ordner: 
old:
Programme die für Tests gebraucht wurden

tkInter:
Bisheriger Stand einer GUI. Um diese voll funktionsfähig zu bekommen und aus ihr einen mehrwert abzuleiten ist enorm viel Aufwand von Nöten

Programme:
> Main:
Hauptprogramm, welches alle Bauteile vereint

>cameraTestMain:
Programm zum Testen der Kamera im Triggermodus/ kontinuierlichem Modus OHNE Serial Trigger...

Klassen:
>isCamera: zur Erstellung eines Objektes einer Imaging Source Kamera mit allen Einstellungen
>imageProcessing: wird von der isCamera erstellt, beinhaltet die Callbackfunktionen für die isCamera
>callbackUserData: für Callbackfunktion der Kamera
>tisgrabber: für Imaging Source Kameras (python wrapper)

>trigger: Klasse zur Ansteuerung eines DG645 Delay Generators.