import os
import json
import re
import uuid

CONTACT_FILE = 'contacts.json'


class Contact:
    def __init__(self, contact_id, name, phone, email):
        self.contact_id = contact_id
        self.name = name
        self.phone = phone
        self.email = email

    def to_dict(self):
        return {
            "contact_id": self.contact_id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email
        }

    @staticmethod
    def is_valid_phone(phone):
        return re.fullmatch(r"\+?\d{10,15}", phone) is not None

    @staticmethod
    def is_valid_email(email):
        return re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email) is not None


class ContactManager:
    def __init__(self):
        self.contacts = self.load_contacts()

    def load_contacts(self):
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

    def save_contacts(self):
        try:
            with open(CONTACT_FILE, 'w') as file:
                json.dump(self.contacts, file, indent=4)
        except Exception as e:
            print(f"Error: Failed to save contacts. Details: {e}")

    def add_contact(self):
        name = input("Enter contact name: ").strip()
        if not name:
            print("Error: Contact name cannot be empty!")
            return

        phone = input("Enter contact phone number: ").strip()
        if not Contact.is_valid_phone(phone):
            print("Error: Invalid phone number! (Expected: +CountryCode PhoneNumber, e.g., +1234567890 or 1234567890)")
            return

        email = input("Enter contact email: ").strip()
        if not Contact.is_valid_email(email):
            print("Error: Invalid email address!")
            return

        contact_id = str(uuid.uuid4())
        if name in self.contacts:
            print("Error: Contact with this name already exists!")
            return

        self.contacts[name] = Contact(contact_id, name, phone, email).to_dict()
        self.save_contacts()
        print(f"Contact {name} added successfully.")

    def search_contact(self):
        name = input("Enter the name of the contact to search: ").strip()
        if not name:
            print("Error: Name cannot be empty!")
            return

        if name in self.contacts:
            contact = self.contacts[name]
            print(f"ID: {contact['contact_id']}")
            print(f"Name: {contact['name']}")
            print(f"Phone: {contact['phone']}")
            print(f"Email: {contact['email']}")
        else:
            print(f"Error: No contact found with the name '{name}'.")

    def update_contact(self):
        name = input("Enter the name of the contact to update: ").strip()
        if not name:
            print("Error: Name cannot be empty!")
            return

        if name in self.contacts:
            contact = self.contacts[name]
            phone = input(
                f"Enter new phone number (current: {contact['phone']}): ").strip()
            if phone and not Contact.is_valid_phone(phone):
                print("Error: Invalid phone number!")
                return

            email = input(
                f"Enter new email (current: {contact['email']}): ").strip()
            if email and not Contact.is_valid_email(email):
                print("Error: Invalid email address!")
                return

            contact['phone'] = phone if phone else contact['phone']
            contact['email'] = email if email else contact['email']
            self.save_contacts()
            print(f"Contact {name} updated successfully.")
        else:
            print(f"Error: No contact found with the name '{name}'.")

    def delete_contact(self):
        name = input("Enter the name of the contact to delete: ").strip()
        if not name:
            print("Error: Name cannot be empty!")
            return

        if name in self.contacts:
            confirm = input(
                f"Are you sure you want to delete {name}? (y/n): ").strip().lower()
            if confirm == 'y':
                del self.contacts[name]
                self.save_contacts()
                print(f"Contact {name} deleted successfully.")
            else:
                print("Deletion canceled.")
        else:
            print(f"Error: No contact found with the name '{name}'.")


def main():
    manager = ContactManager()

    while True:
        print("\n1. Add Contact")
        print("2. Search Contact")
        print("3. Update Contact")
        print("4. Delete Contact")
        print("5. Exit")
        choice = input("Choose an option: ").strip()

        if choice == '1':
            manager.add_contact()
        elif choice == '2':
            manager.search_contact()
        elif choice == '3':
            manager.update_contact()
        elif choice == '4':
            manager.delete_contact()
        elif choice == '5':
            print("Exiting Contact Management System. Goodbye!")
            break
        else:
            print("Error: Invalid choice. Please try again.")


if __name__ == '__main__':
    main()
