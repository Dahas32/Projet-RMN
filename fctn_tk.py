import tkinter as tk
from tkinter import filedialog


def selection_fichier(root):
    root.filename = filedialog.askopenfilename(
        initialdir="~/Bureau/", title="Select a .drx fil to analyse.",
    )
    return root.filename
