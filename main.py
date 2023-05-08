import tkinter as tk
from tkinter import filedialog, messagebox
import re
import os
import win32gui
import win32con


# Cache la fenêtre de la console de commande
def hide_console():
    hide_me = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hide_me, win32con.SW_HIDE)


hide_console()

# Crée une fenêtre racine Tkinter
root = tk.Tk()
root.withdraw()

# Ouvre une boîte de dialogue pour sélectionner un fichier
file_path = filedialog.askopenfilename(initialdir='Documents/', title='Sélectionner un fichier')

# Lit le contenu du fichier
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()
    lines = content.splitlines()

# Suppression des '0' entre 'T' et le numéro d'outil
pattern = re.compile(r'T0+([1-9])')
for i, line in enumerate(lines):
    lines[i] = pattern.sub(r'T\1', line)

# Recherche des 'M2' à supprimer
lines_to_replace = [i for i, line in enumerate(lines) if 'M2' in line]

# Recherche de la première occurrence de 'M30'
index = next((i for i, line in enumerate(lines) if 'M30' in line), None)
# Supprime les lignes à remplacer et toutes les autres occurrences de "M30"
if lines_to_replace:
    lines_to_replace.append(index)
    lines = [line for i, line in enumerate(lines) if i not in lines_to_replace]

# Enregistre les modifications dans un nouveau fichier
new_file_path = filedialog.asksaveasfilename(initialdir='Documents/', title='Enregistrer sous', defaultextension='.txt')
with open(new_file_path, 'w', encoding='utf-8') as file:
    file.write('\n'.join(lines))

# Demande si l'utilisateur veut ouvrir le nouveau fichier généré
answer = messagebox.askyesno("Ouvrir le fichier ?", "Voulez-vous ouvrir le nouveau fichier généré ?")

if answer:
    os.startfile(new_file_path)

# pyinstaller main.py dans le terminal pour créer un .exe
