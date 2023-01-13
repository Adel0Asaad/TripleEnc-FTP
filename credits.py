import tkinter as tk
from PIL import ImageTk
import threading

def textApp():
    
    window = tk.Tk()
    window.title("Project Credits")
    window.rowconfigure(0, minsize=600, weight=1)
    window.columnconfigure(1, minsize=200, weight=1)
    # window.protocol("WM_DELETE_WINDOW", on_closing)
    window.geometry("800x600")
    window.minsize(800, 600)
    window.resizable(False, False)

    # txt_edit = tk.CustomText(window, bg="#242424", fg="#FFFFFF", insertbackground="#DDDDDD", wrap= tk.WORD, font=("Consolas", 13), state=tk.DISABLED)
    team_frame = tk.Frame(window, relief=tk.RAISED, bd=10, bg="#242424")
    team_members_label= tk.Label(team_frame, bg="#242424", fg="#075ea1", text="Team Members", font=("Times New Roman", 32))
    adel_asaad_label= tk.Label(team_frame, bg="#242424", fg="#FFFFFF", text="Adel Asaad - 18P2949", font=("Times New Roman", 18))
    madonna_bassem_label= tk.Label(team_frame, bg="#242424", fg="#FFFFFF", text="Madonna Bassem - 18P5194", font=("Times New Roman", 18))
    mohamed_adel_label= tk.Label(team_frame, bg="#242424", fg="#FFFFFF", text="Mohamed Adel - 18P1724", font=("Times New Roman", 18))

    fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=10, bg="#242424")
    
    photo = ImageTk.PhotoImage(file= "ASUENG Logo.png")
    imageLabel = tk.Label(fr_buttons, bg="#242424", image = photo)
    imageLabel.image = photo

    imageLabel.grid(row=1, column=0, pady=60)

    team_members_label.place(relx=0.5, rely=0.1, anchor="center")
    adel_asaad_label.place(relx=0.5, rely=0.3, anchor="center")
    madonna_bassem_label.place(relx=0.5, rely=0.45, anchor="center")
    mohamed_adel_label.place(relx=0.5, rely=0.6, anchor="center")

    fr_buttons.grid(row=0, column=0, sticky="ns")
    team_frame.grid(row=0, column=1, sticky="nsew")

    window.mainloop()


print('Team Credits are opened in a separate window, which you may close if you want.')

textThread = threading.Thread(target=textApp)
textThread.start()

