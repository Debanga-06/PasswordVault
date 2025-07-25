
# Install Dependencies & Imports

!pip install cryptography

import json
import os
import secrets
import string
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from datetime import datetime

print("✅ Dependencies installed and imported!")

# PassVault Class Definition

class PassVaultColab:
    def __init__(self):
        self.vault_file = "passvault_colab.json"
        self.key_file = "vault_colab.key"
        self.fernet = None
        self.session_authenticated = False

    def generate_key_from_password(self, password: str, salt: bytes = None) -> tuple:
        """Generate encryption key from master password"""
        if salt is None:
            salt = os.urandom(16)

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt

    def setup_master_password(self):
        """Setup master password for first-time use"""
        print("🔒 Welcome to PassVault (Colab Edition)!")
        print("Setting up your master password...")

        while True:
            password = input("Create a master password (min 6 chars): ")
            confirm = input("Confirm master password: ")

            if password == confirm and len(password) >= 6:
                break
            elif len(password) < 6:
                print("❌ Password must be at least 6 characters long!")
            else:
                print("❌ Passwords don't match!")

        # Generate key and salt
        key, salt = self.generate_key_from_password(password)
        self.fernet = Fernet(key)

        # Store salt and password hash
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        key_data = {
            "salt": base64.b64encode(salt).decode(),
            "password_hash": password_hash
        }

        with open(self.key_file, 'w') as f:
            json.dump(key_data, f)

        # Create empty vault
        self.save_vault({})
        print("✅ Master password set successfully!")
        self.session_authenticated = True
        return True

    def authenticate(self):
        """Authenticate user with master password"""
        if self.session_authenticated:
            return True

        if not os.path.exists(self.key_file):
            return self.setup_master_password()

        with open(self.key_file, 'r') as f:
            key_data = json.load(f)

        salt = base64.b64decode(key_data["salt"])
        stored_hash = key_data["password_hash"]

        attempts = 3
        while attempts > 0:
            password = input("Enter master password: ")
            password_hash = hashlib.sha256(password.encode()).hexdigest()

            if password_hash == stored_hash:
                key, _ = self.generate_key_from_password(password, salt)
                self.fernet = Fernet(key)
                print("✅ Authentication successful!")
                self.session_authenticated = True
                return True
            else:
                attempts -= 1
                if attempts > 0:
                    print(f"❌ Incorrect password! {attempts} attempts remaining.")
                else:
                    print("❌ Too many failed attempts.")
                    return False

        return False

    def load_vault(self):
        """Load and decrypt vault data"""
        if not os.path.exists(self.vault_file):
            return {}

        try:
            with open(self.vault_file, 'rb') as f:
                encrypted_data = f.read()

            if not encrypted_data:
                return {}

            decrypted_data = self.fernet.decrypt(encrypted_data)
            return json.loads(decrypted_data.decode())
        except Exception as e:
            print(f"❌ Error loading vault: {e}")
            return {}

    def save_vault(self, data):
        """Encrypt and save vault data"""
        try:
            json_data = json.dumps(data, indent=2)
            encrypted_data = self.fernet.encrypt(json_data.encode())

            with open(self.vault_file, 'wb') as f:
                f.write(encrypted_data)
            return True
        except Exception as e:
            print(f"❌ Error saving vault: {e}")
            return False

    def generate_password(self, length=12, include_symbols=True):
        """Generate a secure random password"""
        chars = string.ascii_letters + string.digits
        if include_symbols:
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"

        password = ''.join(secrets.choice(chars) for _ in range(length))
        return password

    def check_password_strength(self, password):
        """Basic password strength checker"""
        score = 0
        feedback = []

        if len(password) >= 8:
            score += 1
        else:
            feedback.append("Use at least 8 characters")

        if any(c.islower() for c in password):
            score += 1
        else:
            feedback.append("Include lowercase letters")

        if any(c.isupper() for c in password):
            score += 1
        else:
            feedback.append("Include uppercase letters")

        if any(c.isdigit() for c in password):
            score += 1
        else:
            feedback.append("Include numbers")

        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            score += 1
        else:
            feedback.append("Include special characters")

        strength_levels = ["Very Weak", "Weak", "Fair", "Good", "Strong"]
        strength = strength_levels[min(score, 4)]

        return strength, feedback

print("✅ PassVault class defined!")

# Initialize Vault & Authentication

# Create vault instance
vault = PassVaultColab()

print("🔒 PassVault - Google Colab Edition")
print("=" * 50)
print("⚠️ IMPORTANT COLAB NOTES:")
print("• Passwords will be visible when typing (Colab limitation)")
print("• Files are temporary - download them to save permanently")
print("=" * 50)

# Authenticate
if vault.authenticate():
    print("\n✅ Vault initialized successfully!")
else:
    print("❌ Authentication failed!")

# Add Password Function

def add_password():
    """Add a new password entry"""
    if not vault.session_authenticated:
        print("❌ Please authenticate first by running Block 3!")
        return

    print("\n➕ Add New Password Entry")

    website = input("Website/Service name: ").strip()
    if not website:
        print("❌ Website name cannot be empty!")
        return

    username = input("Username/Email: ").strip()

    # Option to generate password
    choice = input("Generate secure password? (y/n): ").lower()
    if choice == 'y':
        length = input("Password length (default 12): ").strip()
        length = int(length) if length.isdigit() else 12

        symbols = input("Include symbols? (y/n): ").lower() == 'y'
        password = vault.generate_password(length, symbols)
        print(f"Generated password: {password}")
    else:
        print("⚠️ Note: Your password will be visible in Colab")
        password = input("Enter password: ")

    # Check password strength
    strength, feedback = vault.check_password_strength(password)
    print(f"Password strength: {strength}")
    if feedback:
        print("Suggestions:", ", ".join(feedback))

    # Save to vault
    vault_data = vault.load_vault()

    if website in vault_data:
        overwrite = input(f"Entry for '{website}' exists. Overwrite? (y/n): ")
        if overwrite.lower() != 'y':
            print("❌ Operation cancelled.")
            return

    vault_data[website] = {
        "username": username,
        "password": password,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    if vault.save_vault(vault_data):
        print("✅ Password saved successfully!")
    else:
        print("❌ Failed to save password!")

print("📝 add_password() function ready!")
print("Usage: add_password()")

# Get Password Function

def get_password():
    """Retrieve stored passwords"""
    if not vault.session_authenticated:
        print("❌ Please authenticate first by running Block 3!")
        return

    print("\n🔍 Retrieve Password")

    vault_data = vault.load_vault()
    if not vault_data:
        print("❌ No passwords stored yet!")
        return

    search = input("Enter website name or username to search: ").strip().lower()

    matches = []
    for website, data in vault_data.items():
        if (search in website.lower() or
            search in data.get("username", "").lower()):
            matches.append((website, data))

    if not matches:
        print("❌ No matching entries found!")
        return

    print(f"\n📋 Found {len(matches)} match(es):")
    for i, (website, data) in enumerate(matches, 1):
        print(f"\n{i}. Website: {website}")
        print(f"   Username: {data.get('username', 'N/A')}")
        print(f"   Created: {data.get('created', 'Unknown')}")

        show_pass = input("   Show password? (y/n): ").lower()
        if show_pass == 'y':
            print(f"   Password: {data['password']}")

print("🔍 get_password() function ready!")
print("Usage: get_password()")

# List All Passwords Function

def list_all_passwords():
    """List all stored accounts"""
    if not vault.session_authenticated:
        print("❌ Please authenticate first by running Block 3!")
        return

    print("\n📋 All Stored Accounts")

    vault_data = vault.load_vault()
    if not vault_data:
        print("❌ No passwords stored yet!")
        return

    print(f"Total accounts: {len(vault_data)}\n")
    for i, (website, data) in enumerate(vault_data.items(), 1):
        print(f"{i}. {website}")
        print(f"   Username: {data.get('username', 'N/A')}")
        print(f"   Created: {data.get('created', 'Unknown')}")
        print()

print("📋 list_all_passwords() function ready!")
print("Usage: list_all_passwords()")

# Generate Password Function

def generate_password_only():
    """Generate password without saving"""
    print("\n🎲 Password Generator")

    length = input("Password length (default 12): ").strip()
    length = int(length) if length.isdigit() else 12

    symbols = input("Include symbols? (y/n): ").lower() == 'y'

    password = vault.generate_password(length, symbols)
    print(f"\nGenerated password: {password}")

    strength, feedback = vault.check_password_strength(password)
    print(f"Strength: {strength}")
    if feedback:
        print("Suggestions:", ", ".join(feedback))

def quick_generate(length=12, symbols=True):
    """Quick password generation"""
    password = vault.generate_password(length, symbols)
    print(f"Password: {password}")
    return password

print("🎲 Password generation functions ready!")
print("Usage: generate_password_only() or quick_generate()")

# Delete Password Function

def delete_password():
    """Delete a password entry"""
    if not vault.session_authenticated:
        print("❌ Please authenticate first by running Block 3!")
        return

    print("\n🗑️ Delete Password Entry")

    vault_data = vault.load_vault()
    if not vault_data:
        print("❌ No passwords stored yet!")
        return

    website = input("Enter website name to delete: ").strip()

    if website not in vault_data:
        print("❌ Website not found!")
        return

    print(f"Entry to delete:")
    print(f"Website: {website}")
    print(f"Username: {vault_data[website].get('username', 'N/A')}")

    confirm = input("Type 'DELETE' to confirm deletion: ")
    if confirm == 'DELETE':
        del vault_data[website]
        if vault.save_vault(vault_data):
            print("✅ Entry deleted successfully!")
        else:
            print("❌ Failed to delete entry!")
    else:
        print("❌ Deletion cancelled.")

print("🗑️ delete_password() function ready!")
print("Usage: delete_password()")

# Utility Functions

def show_vault_status():
    """Show vault status and files"""
    print(f"\n📊 Vault Status:")
    print(f"Authenticated: {vault.session_authenticated}")

    if vault.session_authenticated:
        vault_data = vault.load_vault()
        print(f"Total entries: {len(vault_data)}")

        if vault_data:
            print("Stored accounts:")
            for website in vault_data.keys():
                print(f"  • {website}")

    # Show files
    print(f"\n📁 Vault Files:")
    vault_files = [f for f in os.listdir('.') if f.startswith('vault') or f.startswith('passvault')]
    if vault_files:
        for f in vault_files:
            size = os.path.getsize(f)
            print(f"  {f} ({size} bytes)")
    else:
        print("  No vault files found")

def download_files():
    """Download vault files for backup"""
    print("\n💾 Download Instructions:")
    print("1. Check the file manager on the left sidebar")
    print("2. Right-click on vault files and select 'Download'")
    print("\nImportant: Save these files to restore your vault later!")

    show_vault_status()

    # Create a backup info file
    with open("BACKUP_INFO.txt", "w") as f:
        f.write("PassVault Backup Files\n")
        f.write("=" * 30 + "\n")
        f.write("Files to backup:\n")
        f.write("1. passvault_colab.json (encrypted passwords)\n")
        f.write("2. vault_colab.key (encryption key info)\n")
        f.write("\nTo restore:\n")
        f.write("1. Upload both files to a new Colab session\n")
        f.write("2. Run the PassVault code blocks\n")
        f.write("3. Use your master password to authenticate\n")

    print("✅ Created BACKUP_INFO.txt with instructions")

print("🛠️ Utility functions ready!")
print("Usage: show_vault_status(), download_files()")

# Quick Usage Guide

def show_help():
    """Show available functions"""
    print("\n🔒 PassVault - Available Functions:")
    print("=" * 40)
    print("📝 add_password()           - Add new password")
    print("🔍 get_password()           - Find & retrieve password")
    print("📋 list_all_passwords()     - Show all accounts")
    print("🎲 generate_password_only() - Generate password only")
    print("🎲 quick_generate()         - Quick password generation")
    print("🗑️ delete_password()        - Delete password entry")
    print("📊 show_vault_status()      - Show vault status")
    print("💾 download_files()         - Backup vault files")
    print("❓ show_help()              - Show this help")
    print("=" * 40)
    print("\n💡 Quick Start:")
    print("1. add_password()      # Add your first password")
    print("2. list_all_passwords() # See what's stored")
    print("3. get_password()      # Retrieve a password")

show_help()
