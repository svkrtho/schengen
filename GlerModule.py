import flet as ft
dctSchengen = [ft.dropdown.Option(" - "),#0
               ft.dropdown.Option("Lokað"),#1
               ft.dropdown.Option("Schengen"),#2
               ft.dropdown.Option("Schengen Koma"),#3
               ft.dropdown.Option("Schengen Brottför"),#4
               ft.dropdown.Option("Non-Schengen"),#5
               ft.dropdown.Option("Non-Schengen Koma"),#6
               ft.dropdown.Option("Non-Schengen Brottför")#7
               ]

""" dctSchengen = [" - ",#0
               "Lokað",#1
               "Schengen",#2
               "Schengen Koma",#3
               "Schengen Brottför",#4
               "Non-Schengen",#5
               "Non-Schengen Koma",#6
               "Non-Schengen Brottför"#7
               ] """


DATA = {"15": {"GlerValm": [dctSchengen[g] for g in [0,1,2,6,7]],
               "GlerStaða": " - "},
        "21": {"GlerValm": [dctSchengen[g] for g in [0,1,3,4,6,7]],
               "GlerStaða": " - "},
        "22": {"GlerValm": [dctSchengen[g] for g in [0,1,3,4,6,7]],
               "GlerStaða": " - "},
        "23": {"GlerValm": [dctSchengen[g] for g in [0,1,3,4,5]],
               "GlerStaða": " - "},
        "32": {"GlerValm": [dctSchengen[g] for g in [0,1,3,4,6,7]],
               "GlerStaða": " - "},
        "34": {"GlerValm": [dctSchengen[g] for g in [0,1,3,4,6,7]],
               "GlerStaða": " - "},
        "35": {"GlerValm": [dctSchengen[g] for g in [0,1,3,4,6,7]],
               "GlerStaða": " - "},
        "2427": {"GlerValm": [dctSchengen[g] for g in [0,1,4,7]],
               "GlerStaða": " - "},
        "2829": {"GlerValm": [dctSchengen[g] for g in [0,1,4,7]],
               "GlerStaða": " - "},
        "E2": {"GlerValm": [dctSchengen[0]],
               "GlerStaða": " - "},
        "3133": {"GlerValm": [dctSchengen[0]],
               "GlerStaða": " - "}
        }
