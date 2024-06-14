import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread
import os
import sys
from melter import MelterBot


def on_check_button_selected():
    selected_bags = [int(bag.get()) for bag in bag_vars if bag.get()]
    print(f"Iterating over: {selected_bags} bags.")
    if len(selected_bags) == 0:
        messagebox.showinfo("Invalid Input", "No bags selected")
    else:
        melter = MelterBot(selected_bags)
        thread = Thread(target=melter.melt)
        thread.start()
        window.after(100, check_thread, thread)


def check_thread(thread):
    if thread.is_alive():
        window.after(100, check_thread, thread)
    else:
        messagebox.showinfo("Finished", "Bot has finished melting. Exiting...")
        window.destroy()


# Create the main window
window = tk.Tk()
window.title("Melter bot")
window.config(width=600, height=600, background='black')
window.resizable(False, False)

# Set the base path for images
if getattr(sys, 'frozen', False):
    base_path = os.path.dirname(sys.argv[0])
else:
    base_path = os.path.abspath(os.path.dirname(__file__))

# Load background image
# img_path = os.path.join(base_path, "imgs", "bg.png")

# Create canvas for background image
canvas = tk.Canvas(window, width=500, height=500, highlightthickness=0, background='black')
# bg_image = tk.PhotoImage(file=img_path)
# canvas.create_image(280, 440, image=bg_image)  # Centering the image
titleCanvas = canvas.create_text(250, 30, text="Melter Bot", width=500, font=("Arial", 20, "bold"), fill="gold",
                                 anchor='n')
canvas.grid(row=0, column=0, columnspan=3)

# Add label below "Melter Bot"
label_text = "Choose your inventory bags"
label = tk.Label(window, text=label_text, font=("Arial", 12), background="white")  # Added background color
label.grid(row=1, column=1)

# Create variables to store the selected values
bag_vars = [tk.StringVar() for _ in range(9)]

# Create check buttons with different values
check_btns = []
for i in range(3):
    for j in range(3):
        index = i * 3 + j
        check_btn = ttk.Checkbutton(window, text=f"Inventory {index + 1}", variable=bag_vars[index],
                                    onvalue=str(index + 1), offvalue="", style='Prettier.TCheckbutton')
        check_btn.place(x=j * 120 + 90, y=i * 120 + 120)  # Adjusted positions
        check_btns.append(check_btn)

# Create a button to trigger the selection action
select_btn = ttk.Button(window, text="Start", command=on_check_button_selected, style='WhiteText.TButton')
select_btn.place(relx=0.5, rely=0.85, anchor="center")  # Centered position

# Styling the button and check buttons
style = ttk.Style()
style.configure('WhiteText.TButton', font=('Arial', 12, 'bold'), padding=10, background='white',
                foreground='black')  # Changed button colorvv and text color
style.configure('Prettier.TCheckbutton', font=('Arial', 12, 'bold'), padding=5, background='#FFD700',
                foreground='black')  # Adjusted padding and color

# Run the main loop
window.mainloop()
