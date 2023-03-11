import os

# Pfad des Ordners, dessen Dateinamen in einer Liste gespeichert werden sollen
folder_path = '/Users/juliusbergmann/Documents/pythonProject'

# Leere Liste, um die Dateinamen zu speichern
file_names = []

# Iteriere über alle Dateien im Ordner
for file in os.listdir(folder_path):
    # Überprüfe, ob die Datei eine PDF-Datei ist
    if file.endswith('.pdf'):
        # Füge den Dateinamen zur Liste hinzu
        file_names.append(file)

# Ausgabe der Liste mit Dateinamen
print(file_names)
