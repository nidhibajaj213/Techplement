import os
import json

CONTACT_FILE = 'contacts.json'

# Function to load contacts from file


def load_contacts():
    try:
        if not os.path.exists(CONTACT_FILE):
            return {}
        with open(CONTACT_FILE, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("Error: Could not decode the contacts file. It might be corrupted.")
        return {}
    except Exception as e:
        print(f"Error: Failed to load contacts. Details: {e}")
        return {}

# Function to save contacts to file


def save_contacts(contacts):
    try:
        with open(CONTACT_FILE, 'w') as file:
            json.dump(contacts, file, indent=4)
    except Exception as e:
        print(f"Error: Failed to save contacts. Details: {e}")

# Function to add a new contact


def add_contact(contacts):
    name = input("Enter contact name: ").strip()
    if not name:
        print("Error: Contact name cannot be empty!")
        return
    if name in contacts:
        print("Error: Contact with this name already exists!")
        return

    phone = input("Enter contact phone number: ").strip()
    if not phone.isdigit():
        print("Error: Phone number must contain only digits!")
        return

    email = input("Enter contact email: ").strip()
    if '@' not in email or '.' not in email:
        print("Error: Invalid email address!")
        return

    contacts[name] = {"phone": phone, "email": email}
    save_contacts(contacts)
    print(f"Contact {name} added successfully.")

# Function to search for a contact by name


def search_contact(contacts):
    name = input("Enter the name of the contact to search: ").strip()
    if not name:
        print("Error: Name cannot be empty!")
        return

    if name in contacts:
        print(f"Name: {name}")
        print(f"Phone: {contacts[name]['phone']}")
        print(f"Email: {contacts[name]['email']}")
    else:
        print(f"Error: No contact found with the name '{name}'.")

# Function to update an existing contact


def update_contact(contacts):
    name = input("Enter the name of the contact to update: ").strip()
    if not name:
        print("Error: Name cannot be empty!")
        return

    if name in contacts:
        phone = input(
            f"Enter new phone number (current: {contacts[name]['phone']}): ").strip()
        if not phone.isdigit():
            print("Error: Phone number must contain only digits!")
            return

        email = input(
            f"Enter new email (current: {contacts[name]['email']}): ").strip()
        if '@' not in email or '.' not in email:
            print("Error: Invalid email address!")
            return

        contacts[name] = {"phone": phone, "email": email}
        save_contacts(contacts)
        print(f"Contact {name} updated successfully.")
    else:
        print(f"Error: No contact found with the name '{name}'.")

# Main function to run the contact management system


def main():
    contacts = load_contacts()
    while True:
        print("\n1. Add Contact")
        print("2. Search Contact")
        print("3. Update Contact")
        print("4. Exit")
        choice = input("Choose an option: ").strip()

        if choice == '1':
            add_contact(contacts)
        elif choice == '2':
            search_contact(contacts)
        elif choice == '3':
            update_contact(contacts)
        elif choice == '4':
            print("Exiting Contact Management System. Goodbye!")
            break
        else:
            print("Error: Invalid choice. Please try again.")


if __name__ == '__main__':
    main()
