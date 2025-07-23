import customtkinter as ctk
from tkinter import filedialog, messagebox
from logic import extract_card_block, replace_card_block
import os

COLOR_BUTTON="blue" # Choice: Or "dark-blue", "green", etc.
COLOR_PAGE="Dark" # Choice: "Light", "Dark", or "System"

ctk.set_appearance_mode(COLOR_PAGE)
ctk.set_default_color_theme(COLOR_BUTTON)

ui_elements = {}

def create_labeled_entry(parent, label, row, key):
    ctk.CTkLabel(parent, text=label).grid(row=row, column=0, padx=10, pady=5, sticky="w")
    entry = ctk.CTkEntry(parent)
    entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
    ui_elements[key] = entry



def select_file(label_widget, key):
    filepath = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
    if filepath:
        ui_elements[key] = filepath
        label_widget.configure(text=os.path.basename(filepath), text_color="green")

def create_file_button(parent, label, row, key):
    label_widget = ctk.CTkLabel(parent, text="No file selected", text_color="gray")
    label_widget.grid(row=row+1, column=0, columnspan=2, padx=10, sticky="w")


    btn = ctk.CTkButton(parent, text=label, command=lambda: select_file(label_widget, key))
    btn.grid(row=row, column=0, columnspan=2, padx=10, pady=5, sticky="ew")



def copy_configuration():
    try:
        source_info = [ui_elements[k].get() for k in ["source_name", "source_type", "source_slot"]]
        dest_info = [ui_elements[k].get() for k in ["dest_name", "dest_type", "dest_slot"]]
        source_path = ui_elements.get("source_file", "")
        dest_path = ui_elements.get("dest_file", "")

        if not all(source_info + dest_info + [source_path, dest_path]):
            messagebox.showwarning("Missing", "Fill all fields and select both XML files.")
            return

        with open(source_path, "r", encoding="utf-8") as f:
            source_lines = f.readlines()
        with open(dest_path, "r", encoding="utf-8") as f:
            dest_lines = f.readlines()

        block = extract_card_block(source_lines, *source_info)
        if not block:
            messagebox.showerror("Error", "Source card not found.")
            return

        modified = replace_card_block(dest_lines, *dest_info, block)
        if not modified:
            messagebox.showerror("Error", "Destination card not found.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
        if save_path:
            with open(save_path, "w", encoding="utf-8") as f:
                f.writelines(modified)
            messagebox.showinfo("Success", "Configuration copied successfully!")

    except Exception as e:
        messagebox.showerror("Error", str(e))

def Gui():
    app = ctk.CTk()
    app.title("TTC Configuration Transfer")
    app.geometry("650x550")
    app.grid_columnconfigure(1, weight=1)

    # Source
    ctk.CTkLabel(app, text="Source Card", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, columnspan=2, pady=(10, 0))
    create_labeled_entry(app, "Name", 1, "source_name")
    create_labeled_entry(app, "Type", 2, "source_type")
    create_labeled_entry(app, "Slot", 3, "source_slot")
    create_file_button(app, "Browse Source XML", 4, "source_file")

    # Destination
    ctk.CTkLabel(app, text="Destination Card", font=ctk.CTkFont(size=14, weight="bold")).grid(row=6, column=0, columnspan=2, pady=(20, 0))
    create_labeled_entry(app, "Name", 7, "dest_name")
    create_labeled_entry(app, "Type", 8, "dest_type")
    create_labeled_entry(app, "Slot", 9, "dest_slot")
    create_file_button(app, "Browse Destination XML", 10, "dest_file")

    # Button
    ctk.CTkButton(app, text="Copy Configuration", command=copy_configuration, width=150, height=30).grid(row=12, column=0, columnspan=2, pady=30, padx=15)

    app.mainloop()

Gui()
