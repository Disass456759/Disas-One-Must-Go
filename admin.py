# Name: 
# Student Number: 

# Programming Principles Project – Admin Program
# Semester 2, 2025

import json
import os

# ==============================
# Helper Functions
# ==============================

def input_something(prompt):
    """
    Prompt the user until a non-empty string is entered.
    Leading/trailing spaces are removed.
    """
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be blank. Please try again.")


def input_int(prompt, max_value):
    """
    Prompt the user until a valid integer between 1 and max_value is entered.
    Returns the integer.
    """
    while True:
        user_input = input(prompt)
        if not user_input.isdigit():
            print("Invalid input. Please enter a number.")
            continue
        num = int(user_input)
        if 1 <= num <= max_value:
            return num
        print(f"Please enter a number between 1 and {max_value}.")


def save_data(data):
    """
    Save the data list to 'data.txt' in JSON format.
    """
    try:
        with open("data.txt", "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error saving data: {e}")


def load_data():
    """
    Load categories data from 'data.txt'.
    If file does not exist or contains invalid data, return empty list.
    """
    if os.path.exists("data.txt"):
        try:
            with open("data.txt", "r") as file:
                loaded_data = json.load(file)
                if isinstance(loaded_data, list):
                    return loaded_data
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    return []


# ==============================
# Main Program
# ==============================

def main():
    data = load_data()
    print('Welcome to the "One Must Go" Admin Program.')

    while True:
        # Display menu
        print('\nChoose an action:')
        print('[a] Add category')
        print('[l] List categories')
        print('[s] Search categories')
        print('[v] View category options')
        print('[d] Delete category')
        print('[q] Quit program')
        choice = input('> ').lower().strip()

        # --------------------------
        # ADD category
        # --------------------------
        if choice == 'a':
            category_name = input_something("Enter a category name: ").lower()

            # Check for duplicates
            if any(c["category"].lower() == category_name for c in data):
                print(f'The category "{category_name}" already exists.')
                continue

            # Input 4 unique options
            options = []
            print("Enter 4 options for this category:")
            while len(options) < 4:
                option = input_something(f"Option {len(options)+1}: ")
                if option.lower() in [o.lower() for o in options]:
                    print("That option already exists. Enter a different one.")
                    continue
                options.append(option)

            # Append new category
            data.append({"category": category_name, "options": options})
            save_data(data)
            print(f'Category "{category_name}" added successfully.')

        # --------------------------
        # LIST categories
        # --------------------------
        elif choice == 'l':
            if not data:
                print("No categories have been added yet.")
            else:
                print("Current categories:")
                for i, item in enumerate(data, 1):
                    print(f"{i}. {item['category'].title()}")

        # --------------------------
        # SEARCH categories
        # --------------------------
        elif choice == 's':
            if not data:
                print("No categories available to search.")
                continue

            search_term = input_something("Enter search term: ").lower()
            matches = [item for item in data if search_term in item["category"].lower()]

            if not matches:
                print(f'No categories found containing "{search_term}".')
            else:
                print("Search results:")
                for i, item in enumerate(matches, 1):
                    print(f"{i}. {item['category'].title()}")

        # --------------------------
        # VIEW category options
        # --------------------------
        elif choice == 'v':
            if not data:
                print("No categories available to view.")
                continue

            print("Select a category to view:")
            for i, item in enumerate(data, 1):
                print(f"{i}. {item['category'].title()}")

            category_num = input_int("Enter category number: ", len(data))
            selected = data[category_num - 1]
            print(f'\nCategory: {selected["category"].title()}')
            print("Options:")
            for j, opt in enumerate(selected["options"], 1):
                print(f"{j}. {opt}")

        # --------------------------
        # DELETE category
        # --------------------------
        elif choice == 'd':
            if not data:
                print("No categories available to delete.")
                continue

            print("Select a category to delete:")
            for i, item in enumerate(data, 1):
                print(f"{i}. {item['category'].title()}")

            category_num = input_int("Enter category number: ", len(data))
            deleted = data.pop(category_num - 1)
            save_data(data)
            print(f'Category "{deleted["category"].title()}" deleted successfully.')

        # --------------------------
        # QUIT program
        # --------------------------
        elif choice == 'q':
            save_data(data)
            print("Goodbye! Data has been saved.")
            break

        # --------------------------
        # INVALID choice
        # --------------------------
        else:
            print("Invalid choice. Please enter a, l, s, v, d, or q.")


# Run the program
if __name__ == "__main__":
    main()
