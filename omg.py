

# This file is provided to you as a starting point for the "omg.py" program of the Project
# of Programming Principles in Semester 2, 2025.  It aims to give you just enough code to help ensure
# that your program is well structured.  Please use this file as the basis of your work.
# You are not required to reference it.

# The "pass" command tells Python to do nothing.  It is simply a placeholder to ensure that the starter file runs smoothly.
# They are not needed in your completed program.  Replace them with your own code as you complete the assignment.

# Import the necessary module(s).
import tkinter as tk
from tkinter import messagebox
import json

class ProgramGUI:
    
    #ProgramGUI class implements the "One Must Go" voting application.
    #It loads categories from data.txt, displays them in a GUI, and records votes.
    

    def __init__(self):
        #Constructor: Load data, set up GUI, and show first category.
        # Attempt to load data from file
        try:
            with open("data.txt", "r") as file:
                self.data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            messagebox.showerror("Error", "Missing or invalid data file.")
            return

        # Check if data is empty
        if not self.data:
            messagebox.showerror("Error", "No categories available in data file.")
            return

        # Initialize main window
        self.root = tk.Tk()
        self.root.title("One Must Go")
        self.root.geometry("500x400")  # Set a fixed window size
        self.root.resizable(False, False)  # Disable resizing for a clean look
        self.root.configure(bg="#f0f0f0")  # Light gray background

        # Current category index
        self.index = 0

        # Title label
        self.title_label = tk.Label(
            self.root,
            text="One Must Go",
            font=("Helvetica", 20, "bold"),
            bg="#f0f0f0",
            fg="#333333"
        )
        self.title_label.pack(pady=(20, 10))

        # Category label
        self.category_label = tk.Label(
            self.root,
            text="",
            font=("Helvetica", 16, "bold"),
            bg="#f0f0f0",
            fg="#3636FD"
        )
        self.category_label.pack(pady=(10, 20))

        # Frame to hold option buttons
        self.options_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.options_frame.pack(pady=10)

        # Progress label (e.g., "Category 1 of 5")
        self.progress_label = tk.Label(
            self.root,
            text="",
            font=("Helvetica", 12, "italic"),
            bg="#f0f0f0",
            fg="#555555"
        )
        self.progress_label.pack(pady=(10, 20))

        # Show the first category
        self.show_category()

        # Start GUI event loop
        self.root.mainloop()

    def show_category(self):
        """Display the current category and create buttons for each option."""
        current = self.data[self.index]
        category_name = current['category'].title()

        # Update category and progress labels
        self.category_label.config(text=category_name)
        self.progress_label.config(text=f"Category {self.index + 1} of {len(self.data)}")

        # Clear previous buttons
        for widget in self.options_frame.winfo_children():
            widget.destroy()

        # Determine button width based on longest option
        max_length = max(len(opt) for opt in current["options"]) + 2

        # Create option buttons
        for opt in current["options"]:
            btn = tk.Button(
                self.options_frame,
                text=opt,
                width=max_length,
                font=("Helvetica", 14),
                bg="#0066cc",
                fg="white",
                activebackground="#0055aa",
                activeforeground="white",
                relief="raised",
                bd=3,
                command=lambda name=opt: self.record_vote(name)
            )
            btn.pack(pady=5)

    def record_vote(self, name):
        #Record the vote for the selected option and proceed to next category
        current = self.data[self.index]

        # Initialize votes if not present
        if "votes" not in current:
            current["votes"] = [0] * len(current["options"])

        # Find option index and increment vote
        opt_index = current["options"].index(name)
        current["votes"][opt_index] += 1

        # Save updated data to file
        try:
            with open("data.txt", "w") as file:
                json.dump(self.data, file, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Error saving data: {e}")
            return

        # Confirmation message
        messagebox.showinfo("Vote Recorded", f'Your vote for "{name}" has been recorded.')

        # Move to next category or finish
        if self.index == len(self.data) - 1:
            # End of all categories
            messagebox.showinfo("End", "You have voted on all categories.")
            self.root.destroy()
        else:
            # Proceed to next category
            self.index += 1
            self.show_category()

# Start the program
gui = ProgramGUI()
