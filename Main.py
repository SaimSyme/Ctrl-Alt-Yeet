from customtkinter import *
from tkinter.filedialog import askdirectory
import json
import os
import shutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict
from tkinter import messagebox

# --------> Logic <--------

APP_DIR = os.path.dirname(os.path.abspath(__file__))

def get_json_path():
    return os.path.join(APP_DIR, "file_types.json")

def load_file_categories():
    try:
        with open(get_json_path(), "r") as f:
            return json.load(f)
    except FileNotFoundError:
        # Create a default file_types.json if it doesn't exist
        default_categories = {
            "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf"],
            "Videos": [".mp4", ".avi", ".mov", ".mkv"],
            "Audios": [".mp3", ".wav", ".ogg"],
            "Images": [".jpg", ".jpeg", ".png", ".bmp", ".webp"],
            "Compressed": [".zip", ".rar"],
            "Programs": [".exe"],
            "General": [".iso", ".tar.gz", ".html", ".css", ".js", ".php", ".py", ".java", 
                        ".cpp", ".h", ".xml", ".json", ".log"]
        }
        save_file_categories(default_categories)
        return default_categories

def save_file_categories(file_categories):
    with open(get_json_path(), "w") as f:
        json.dump(file_categories,f, indent=4)

#initialize the file categories
file_categories = load_file_categories()

#open json file containing all file formats and doing the thing
directories = {ext: category for category, exts in file_categories.items() for ext in exts}

def openFile():
    filepath = askdirectory()
    if not filepath:  # User canceled directory selection
        return
    
    # Get count of files that will be organized
    files = [f for f in os.listdir(filepath) if os.path.isfile(os.path.join(filepath, f))]
    file_count = len(files)
    
    # Show confirmation dialog
    confirm = messagebox.askyesno(
        "Confirm Organization", 
        f"You are about to organize {file_count} files in:\n{filepath}\n\nDo you want to continue?"
    )
    
    if confirm:
        print(filepath)
        createFolders(filepath)
        org_File1(filepath)
    else:
        print_output("File organization canceled by user.")

def createFolders(filepath):
    for directory in set(directories.values()):
         os.makedirs(os.path.join(filepath, directory), exist_ok=True)
    print("Folders Created!")

def org_File1(filepath):
    progress_bar.pack_forget()
    files = os.listdir(filepath)
    progress_bar.pack(pady=10)
    total_files = len(files)
    processed_files = 0
    
    category_counts = defaultdict(int)
    
    progress_bar.set(total_files) 

    for file in files:
        source_path = os.path.join(filepath, file)
        if os.path.isfile(source_path):
            _, extension = os.path.splitext(file)
            extension_lower = extension.lower()

            if extension_lower in directories:
                target_folder = directories[extension_lower]
            else:
                target_folder = "General"

            category_counts[target_folder] += 1
            
            destination_folder = os.path.join(filepath, target_folder)

            # Create target folder if it doesn't exist
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)

            # Construct destination path
            destination_path = os.path.join(destination_folder, file)

            # Check if file with same name exists in destination folder
            if os.path.exists(destination_path):
                base, ext = os.path.splitext(file)
                counter = 1
                while True:
                    new_filename = f"{base}_{counter}{ext}"
                    new_destination_path = os.path.join(destination_folder, new_filename)
                    if not os.path.exists(new_destination_path):
                        destination_path = new_destination_path
                        break
                    counter += 1

            try:
                # Move the file to the destination folder
                shutil.move(source_path, destination_path)
                print_output(f"Moved '{file}' to '{target_folder}' folder.")
            except Exception as e:
                print_output(f"Failed to move '{file}': {str(e)}")
        
        processed_files += 1
        progress_bar.set(processed_files)

    print_output(" \n Files Organized!")

    show_file_distribution(category_counts)
    
def print_output(message):
    # Function to print output to Text widget
    output_text.configure(state="normal")
    output_text.insert(END, message + "\n")
    output_text.yview(END) # Focus on the last message
    output_text.configure(state="disabled") 
    window.update_idletasks() # update GUI

def show_file_distribution(category_counts):
    chart_window = CTkToplevel(window)
    chart_window.title("File Distribution Summary")
    chart_window.geometry("700x700")
    
    # Create a figure for the chart
    figure = plt.Figure(figsize=(6, 4), dpi=100, facecolor='#d1cfc0')
    ax = figure.add_subplot(111 , facecolor='#d1cfc0')
    
    # Get categories and counts
    categories = list(category_counts.keys())
    counts = list(category_counts.values())
    
    # Create the bar chart
    bars = ax.bar(categories, counts, color='#f76f53')
    ax.set_title('Files Organized by Category')
    ax.set_ylabel('Number of Files')
    ax.set_xlabel('Categories')
    
    # Rotate x-axis labels if there are many categories
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
    
    # Add the counts on top of the bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{int(height)}', ha='center', va='bottom')
    
    # Adjust layout to make room for the rotated labels
    figure.tight_layout()
    
    # Create the canvas to display the chart in the window
    canvas = FigureCanvasTkAgg(figure, master=chart_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1, padx=10, pady=10)
    
    # Add a summary label
    total_files = sum(counts)
    summary_label = CTkLabel(
        chart_window, 
        text=f"Total Files Organized: {total_files}",
        font=("Arial", 15, "bold"),
        text_color="#d1cfc0"
    )
    summary_label.pack(pady=10)
    
    # Add a close button
    close_button = CTkButton(
        chart_window,
        text="Close",
        font=("Arial", 15, "bold"),
        command=chart_window.destroy,
        fg_color="#f76f53",
        text_color="#1f1f1f"
    )
    close_button.pack(pady=10)

# --------> GUI <--------

window = CTk()
window.geometry("700x700")
window.title("CTRL+ALT+YEET")
set_appearance_mode("dark")

label = CTkLabel(window, text="Ctrl Alt Yeet", font=("Arial", 30, "bold"), text_color="#d1cfc0")
label.pack(pady=20)

directorySelector = CTkLabel(window, text="Select Directory to Organize:", 
                             font=("Arial", 15, 'bold'), text_color="#d1cfc0")
directorySelector.pack(pady=10)

file_Chooser_Btn = CTkButton(window, text="Select",font=("Arial", 15, 'bold'),
                             command=openFile, fg_color="#f76f53", text_color='#1f1f1f')
file_Chooser_Btn.pack(pady=10)

output_text = CTkTextbox(window, width=600, height=300,
                         text_color='#1f1f1f', fg_color='#d1cfc0',
                         font=("Arial", 12, "bold"))
output_text.pack(pady=20)
output_text.configure(state="disabled")

progress_bar = CTkProgressBar(window, width=600, height=15, progress_color='#f76f53')
progress_bar.pack_forget()
progress_bar.set(0)

# -------> Custom File Gui <------------

def show_file_types():
    # Create the pop-up window to show and edit JSON content
    file_types_window = CTkToplevel(window)
    file_types_window.geometry("750x900")  # Increased height for the additional components
    file_types_window.title("Manage File Types and Categories")

    file_types_window.lift()  # Brings the pop up above the main window
    # Ensure the pop-up stays on top
    file_types_window.attributes("-topmost", 1)
    file_types_window.attributes("-topmost", 0)
    
    # Read the current file_categories data
    try:
        with open("file_types.json", "r") as f:
            json_data = json.load(f)
            json_text = json.dumps(json_data, indent=4)  # Pretty print JSON
    except Exception as e:
        json_text = f"Error reading file: {str(e)}"

    # Title and instructions
    title_label = CTkLabel(file_types_window, text="Manage File Categories",
                            font=("Arial", 22, "bold"), text_color="#d1cfc0")
    title_label.pack(pady=10)
    
    # ---- Add new category section ----
    add_category_frame = CTkFrame(file_types_window)
    add_category_frame.pack(pady=15, padx=20, fill="x")
    
    add_title = CTkLabel(add_category_frame, text="Add New Category",
                          font=("Arial", 16, "bold"), text_color="#d1cfc0")
    add_title.pack(pady=5)
    
    # Category name entry
    category_label = CTkLabel(add_category_frame, text="Folder Name:",
                              font=("Arial", 14, "bold"), text_color="#d1cfc0")
    category_label.pack(pady=2)
    
    new_category_entry = CTkEntry(add_category_frame, font=("Arial", 12, "bold"), width=400)
    new_category_entry.pack(pady=5)
    
    # File extensions entry
    extensions_label = CTkLabel(add_category_frame, text="File Extensions (comma separated):",
                                font=("Arial", 14, "bold"), text_color="#d1cfc0")
    extensions_label.pack(pady=2)
    
    new_extensions_entry = CTkEntry(add_category_frame, font=("Arial", 12, "bold"), width=400)
    new_extensions_entry.pack(pady=5)
    
    # Function to add a new category from the dialog
    def add_category_from_dialog():
        category = new_category_entry.get().strip()
        extensions = new_extensions_entry.get().strip().split(",")
        
        if not category:
            messagebox.showerror("Error", "Please enter a category name.")
            return
        
        if not extensions or all(ext.strip() == "" for ext in extensions):
            messagebox.showerror("Error", "Please enter at least one file extension.")
            return
        
        extensions = [ext.strip().lower() for ext in extensions if ext.strip()]
        
        # Check if extensions have dots and add if needed
        extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in extensions]
        
        # Get current JSON from the text box to ensure we're working with the latest version
        try:
            current_json_text = file_types_text.get("1.0", END).strip()
            current_json = json.loads(current_json_text)
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Current JSON in editor is invalid. Please fix it first.")
            return
        
        # Check if the category already exists
        if category in current_json:
            if messagebox.askyesno("Category Exists", 
                                  f"Category '{category}' already exists. Do you want to add these extensions to it?"):
                # Add extensions to existing category
                current_json[category].extend([ext for ext in extensions if ext not in current_json[category]])
            else:
                return
        else:
            # Add new category
            current_json[category] = extensions
        
        # Update the text box with the new JSON
        updated_json_text = json.dumps(current_json, indent=4)
        file_types_text.delete("1.0", END)
        file_types_text.insert("1.0", updated_json_text)
        
        # Clear the input fields
        new_category_entry.delete(0, END)
        new_extensions_entry.delete(0, END)
        
        messagebox.showinfo("Success", f"Category information updated. Click 'Save Changes' to apply.")
    
    # Add button
    add_button = CTkButton(add_category_frame, text="Add Category", font=("Arial", 14, "bold"),
                           command=add_category_from_dialog, fg_color="#f76f53", text_color='#1f1f1f')
    add_button.pack(pady=10)
    
    # ---- JSON editor section ----
    editor_label = CTkLabel(file_types_window, text="Manual JSON Editing:",
                            font=("Arial", 16, "bold"), text_color="#d1cfc0")
    editor_label.pack(pady=5)
    
    instruction_text = "You can directly edit the JSON structure below. Make sure to maintain proper JSON format."
    instruction_label = CTkLabel(file_types_window, text=instruction_text,
                                font=("Arial", 12), text_color="#d1cfc0")
    instruction_label.pack()
    
    # Create a text box to display and edit the JSON
    file_types_text = CTkTextbox(file_types_window, width=600, height=300, 
                                font=("Arial", 14, "bold"),
                                text_color='#1f1f1f', fg_color='#d1cfc0')
    file_types_text.insert(END, json_text)
    file_types_text.pack(pady=15, padx=20, fill="both", expand=True)

    # Allow the user to edit the JSON content
    file_types_text.configure(state="normal")

    def save_json():
        # Get the edited content from the text box
        new_json_data = file_types_text.get("1.0", END).strip()
        
        # Try to load the edited JSON to ensure it's valid
        try:
            parsed_json = json.loads(new_json_data)  # Validate JSON
            with open("file_types.json", "w") as f:
                json.dump(parsed_json, f, indent=4)
                
            # Update the global variables with new values
            global file_categories, directories
            file_categories = parsed_json
            directories = {ext: category for category, exts in file_categories.items() for ext in exts}
                
            messagebox.showinfo("Success", "Successfully saved changes to file categories.")
            file_types_window.destroy()  # Close the window after saving
        except json.JSONDecodeError as e:
            messagebox.showerror("JSON Error", f"Invalid JSON format: {str(e)}")

    # Button container frame
    button_frame = CTkFrame(file_types_window)
    button_frame.pack(pady=10, fill="x")
    
    # Save button to save the changes
    save_button = CTkButton(button_frame, text="Save Changes", font=("Arial", 15, "bold"),
                           command=save_json, fg_color="#f76f53", text_color='#1f1f1f')
    save_button.pack(side="left", padx=20, pady=10, expand=True)

    # Close button to close the editor without saving
    close_button = CTkButton(button_frame, text="Cancel", font=("Arial", 15, "bold"),
                            command=file_types_window.destroy, fg_color="#d1cfc0", text_color='#1f1f1f')
    close_button.pack(side="right", padx=20, pady=10, expand=True)
    
manage_categories_btn = CTkButton(window, text="Manage File Categories", font=("Arial", 15, 'bold'), 
                                command=show_file_types, fg_color="#f76f53", text_color='#1f1f1f')
manage_categories_btn.pack(pady=20)
  
window.mainloop()