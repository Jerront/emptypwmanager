import json
import re
import random
import string
import os

# Caesar cipher encryption and decryption functions (pre-implemented)
def caesar_encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            shifted = ord(char) + shift
            if char.islower():
                if shifted > ord('z'):
                    shifted -= 26
            elif char.isupper():
                if shifted > ord('Z'):
                    shifted -= 26
            encrypted_text += chr(shifted)
        else:
            encrypted_text += char
    return encrypted_text

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

# Password strength checker function (optional)
def is_strong_password(password):
    """
    Password must have:
    - at least 8 characters
    - at least one uppercase letter
    - at least one lowercase letter
    - at least one digit
    - at least one special symbol
    """
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[^A-Za-z0-9]", password):
        return False
    return True

    # ...

# Password generator function (optional)
def generate_password(length):
    chars = string.ascii_letters + string.digits + string.punctuation
    while True:
        pwd = "".join(random.choice(chars) for _ in range(length))
        if is_strong_password(pwd):
            return pwd
  

# Initialize empty lists to store encrypted passwords, websites, and usernames
encrypted_passwords = []
websites = []
usernames = []

# Function to add a new password 
def add_password(website=None, username=None, password=None):
    """
    Two modes:
    (1) Automated test mode: parameters given → add directly
    (2) UI mode: no parameters → ask user for input
    """
    # UI MODE
    if website is None:
        website = input("Enter website: ")
        username = input("Enter username: ")
        password = input("Enter password: ")

        # optional strength check
        if not is_strong_password(password):
            print("Weak password! You may generate a strong one.")
            if input("Generate strong password? (y/n): ").lower() == "y":
                try:
                    length = int(input("Enter password length: "))
                except ValueError:
                    length = 12
                password = generate_password(length)
                print("Generated:", password)

    # Encrypt before storing
    encrypted = caesar_encrypt(password, 3)

    websites.append(website)
    usernames.append(username)
    encrypted_passwords.append(encrypted)

    return True
  

# Function to retrieve a password 
def get_password(website=None):
    """
    Test mode: website param given
    UI mode: ask user
    """
    interactive = False
    if website is None:
        interactive = True
        website = input("Enter website to retrieve: ")

    if website not in websites:
        if interactive:
            print("Website not found.")
        return None, None

    idx = websites.index(website)
    username = usernames[idx]
    password = caesar_decrypt(encrypted_passwords[idx], 3)

    # UI mode prints the result
    if interactive:
        print(f"Username: {username}")
        print(f"Password: {password}")

    return username, password



# Function to save passwords to a JSON file 
def save_passwords(password_list=None, filename="vault.txt"):
    """
    Test mode: test.py provides list + filename
    UI mode: no params → save internal lists into vault.txt
    """
    # test mode → save given list directly
    if password_list is not None:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(password_list, f)
        return True

    # UI mode → build list first
    combined = []
    for i in range(len(websites)):
        combined.append({
            "website": websites[i],
            "username": usernames[i],
            "password": encrypted_passwords[i]
        })

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(combined, f)

    print("Passwords saved.")
    return True


def load_passwords(filename="vault.txt"):
    # test: file missing → return empty list
    if not os.path.exists(filename):
        return []

    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    # fill global lists from file
    websites.clear()
    usernames.clear()
    encrypted_passwords.clear()
    for entry in data:
        websites.append(entry.get("website"))
        usernames.append(entry.get("username"))
        encrypted_passwords.append(entry.get("password"))

    return data
