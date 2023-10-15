import tkinter as tk
import datetime
import time

def timer():
   print(datetime.datetime.now())
   time.sleep(1)
   app.after(100, timer)

app = tk.Tk()
app.title('Timer')

app.after(1000, timer)

exit_button = tk.Button(app, text="Exit", fg="red", command=app.destroy)
exit_button.pack()

app.mainloop()