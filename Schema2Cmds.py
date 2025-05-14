import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import threading

def run_pipeline(schema_path, delay, x, y, z, output_label):
    try:
        output_label.config(text="Step 1: Grouping...")
        subprocess.run(["python", "grouping.py", schema_path, x, y, z], check=True)

        output_label.config(text="Step 2: Converting to commands...")
        subprocess.run(["python", "convert_to_commands.py", "groups.json"], check=True)

        output_label.config(text="Step 3: Listening and executing commands...")
        subprocess.run([
            "python", "listener.py",
            "commands.txt",
            str(delay),
            str(x),
            str(y),
            str(z)
        ], check=True)

        output_label.config(text="✅ All steps completed successfully.")

    except subprocess.CalledProcessError as e:
        output_label.config(text=f"❌ Error occurred: {e}")
        messagebox.showerror("Error", f"An error occurred:\n{e}")

def start_pipeline():
    try:
        schema_path = schema_entry.get()
        delay = float(delay_entry.get())
        x = int(x_entry.get())
        y = int(y_entry.get())
        z = int(z_entry.get())

        thread = threading.Thread(target=run_pipeline, args=(schema_path, delay, x, y, z, output_label))
        thread.start()

    except ValueError:
        messagebox.showerror("Invalid input", "Please make sure all inputs are valid.")

def browse_file():
    path = filedialog.askopenfilename(filetypes=[("Schematic Files", "*.*")])
    if path:
        schema_entry.delete(0, tk.END)
        schema_entry.insert(0, path)

root = tk.Tk()
root.title("Schematic Processor")
root.geometry("400x300")

# GUI layout
tk.Label(root, text="Schematic File:").pack()
schema_entry = tk.Entry(root, width=40)
schema_entry.pack()
tk.Button(root, text="Browse...", command=browse_file).pack()

tk.Label(root, text="Delay (seconds):").pack()
delay_entry = tk.Entry(root)
delay_entry.pack()

tk.Label(root, text="Start X:").pack()
x_entry = tk.Entry(root)
x_entry.pack()

tk.Label(root, text="Start Y:").pack()
y_entry = tk.Entry(root)
y_entry.pack()

tk.Label(root, text="Start Z:").pack()
z_entry = tk.Entry(root)
z_entry.pack()

tk.Button(root, text="Run Pipeline", command=start_pipeline).pack(pady=10)

output_label = tk.Label(root, text="")
output_label.pack()

root.mainloop()
