#Copyright 8TheDJ
#Application for grade calculator.
import customtkinter as ctk
import os 
import pandas as pd

Mainwindow = ctk.CTk()
Mainwindow.geometry("300x400")
Mainwindow.title('GCijferexport')
Mainwindow._set_appearance_mode("dark")
Mainwindow.config(background='#081c82')

entrybox1 = ctk.CTkEntry(Mainwindow, placeholder_text="Voer norm in", bg_color=Mainwindow.cget("background"),width=200)
entrybox1.grid(row=0, column=0, pady=5)

entrybox2 = ctk.CTkEntry(Mainwindow, placeholder_text="Voer max aantal punten in.", bg_color=Mainwindow.cget("background"),width=200)
entrybox2.grid(row=1, column=0, pady=5)



def bereken_cijfer(aantal_behaalde_punten, totaal_aantal_punten, procent_norm):
    
    if "%" in procent_norm: #verwijderen van het procent teken
        norm = int(procent_norm.replace("%", ""))
    else:
        norm = int(procent_norm)
    anorm = (norm - 50) * 2 # de norm omzetten naar hoeveel procent je nodigt hebt voor een 1
    a = (10 - 1) / (100 - int(anorm)) # de a berekenen van y=ax+b
    b = -(a*100) + 10 # de b berekenen van y=ax+b
    x = aantal_behaalde_punten / totaal_aantal_punten * 100 # de x berekenen, zodat je het cijfer kunt uitlezen dat overeekomt met het aantal procent dat je goed hebt
    if b > 0: # je kan niet lager hebben dan een 1
        cijfer = round(a*x-b, 1) # afronden op 1 decimaal
    else:
        cijfer = round(a*x+b, 1)
    return cijfer # terug geven van cijfer

def createfile():
    norminput = entrybox1.get()
    maxaantalinput = int(entrybox2.get())
    excel_bestand = "cijfers.xlsx"
    if os.path.exists(excel_bestand):
        os.remove(excel_bestand)

    aantal_behaalde_punten_lijst = list(range(maxaantalinput * 2, 0, -1)) # Verdubbel het maxaantalinput zodat de stapgrootte van 0.5 wordt bereikt
    aantal_behaalde_punten_lijst = [punt / 2 for punt in aantal_behaalde_punten_lijst] # Converteer de punten terug naar floats

    totaal_aantal_punten_lijst = [maxaantalinput] * len(aantal_behaalde_punten_lijst)

    cijfers = []

    for aantal_behaalde_punten, totaal_aantal_punten in zip(aantal_behaalde_punten_lijst, totaal_aantal_punten_lijst):
        cijfer = bereken_cijfer(aantal_behaalde_punten, totaal_aantal_punten, norminput)
        if cijfer < 1:
            cijfer = 1
        cijfers.append(cijfer)

    data = {'Aantal behaalde punten': aantal_behaalde_punten_lijst,
            'Totaal aantal punten': totaal_aantal_punten_lijst,
            'Cijfer': cijfers}
    df = pd.DataFrame(data)

    script_dir = os.path.dirname(__file__)
    excel_bestand = os.path.join(script_dir, "cijfers.xlsx")

    df.to_excel(excel_bestand, index=False)

    print("Cijfers zijn geëxporteerd naar", excel_bestand)# conformatie, dat alles goed geëxporteerd is

createbutton = ctk.CTkButton(Mainwindow, text="Create File", command=createfile, bg_color=Mainwindow.cget("background"),)
createbutton.grid(row=3, column=0, pady=5)

Mainwindow.mainloop()
