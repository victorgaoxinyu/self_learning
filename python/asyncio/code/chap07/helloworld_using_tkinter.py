# import tkinter as tk
# import time

# window = tk.Tk()
# window.title('Hello world app')
# window.geometry('200x100')
# window.grid_columnconfigure(0, weight=1)

# def say_hello():
#     # time.sleep(10)   # this will make the app hang for 10 sec!
#     print("Hello there!")

# hello_button = tk.Button(window, text='Say hello', command=say_hello)
# hello_button.grid(column=0, row=1, padx=10, pady=10)

# # url_label = tk.Label(window, text="URL:")
# # url_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

# # url_field = tk.Entry(window, width=10)
# # url_field.grid(column=1, row=0, padx=10, pady=5, sticky='w')

# window.lift()
# window.attributes('-topmost', True)
# window.after_idle(window.attributes, '-topmost', False)

# window.mainloop()



import tkinter as tk

window = tk.Tk()
window.title('Hello world app')
window.geometry('300x120')  # Make it a bit taller

def say_hello():
    print("Hello there!")

# Label in row 0, column 0
url_label = tk.Label(window, text="URL:", fg="black", bg="white")  # Force colors for visibility
url_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')

# Entry in row 0, column 1
url_entry = tk.Entry(window, width=25)
url_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')

# Button in row 1, spanning 2 columns
hello_button = tk.Button(window, text='Say hello', command=say_hello)
hello_button.grid(row=1, column=0, columnspan=2, pady=10)

# Make sure columns can stretch
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)

window.lift()
window.attributes('-topmost', True)
window.after_idle(window.attributes, '-topmost', False)

window.mainloop()
