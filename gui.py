import tkinter as tk
import tkinter as ttk
root = tk.Tk()
#root the frame poatiioning and such
root.title('Tdroid_Tool')
root.configure(bg='#D8D5C8')
frame = tk.Frame(root)
frame.configure(bg='white',padx=20)
frame.place(height=1000)
root.resizable(False,False)
root_wid = 900
root_hi = 600
screen_wdth = root.winfo_screenwidth()
scree_height = root.winfo_screenwidth()
cent_screen = int(screen_wdth/1-root_wid)
cent_screenh = int(scree_height/2-root_hi)
root.geometry(f'{root_wid}x{root_hi}+{cent_screen}+{cent_screenh}')
#end of root sizings
#butons


detect = tk.Button(frame,text='Detect Device').pack()
efs = tk.Button(frame, text='Efs Reset').pack()
backup = tk.Button(frame, text='Back up Items').pack()
restore_backup = tk.Button(frame, text='Restore Items').pack()
install = tk.Button(frame,text='install apk',bg='green',fg='white').pack()
root.mainloop()
