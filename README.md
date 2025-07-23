# 🔐 PassVault – Offline Password Manager (Python + Google Colab)

PassVault is a simple yet powerful **offline password manager** built using Python in **Google Colab**. It securely stores and retrieves user credentials using **AES encryption (Fernet)** and stores them in a local file (`vault.json`). Designed for privacy and portability, it runs fully in Colab without requiring any web deployment or third-party storage.

---

## 📌 Features

- 🔑 Add, retrieve, update, and delete account passwords
- 🔐 Encrypt and decrypt credentials with `cryptography` (Fernet)
- 🧠 Built-in strong password generator
- 💾 Save and load vault data to/from Google Drive or local JSON
- ✅ Fully runs in [Google Colab](https://colab.research.google.com) — no installation needed

---

## 🎯 Real-World Use Cases

- Manage personal passwords offline, without using cloud storage
- Learn Python encryption, file handling, and logic building
- Start with CLI logic and later extend to a Flask/Django web app

---

## 🛠️ Tech Stack

| Component       | Tool/Library                          |
|----------------|----------------------------------------|
| Language        | Python 3.x                             |
| IDE             | Google Colab                          |
| Encryption      | [cryptography – Fernet](https://cryptography.io/en/latest/) |
| Storage         | JSON / Google Drive                   |
| UI              | Command Line / IPython Widgets (optional) |

---

## 🚀 Getting Started

1. **Open the Project Notebook**
   - [Click here to open in Colab](https://colab.research.google.com/drive/1K7H-jvWTR8NsuAUcspwQbLhGVoIV5uT9?usp=sharing)

2. **Install Dependencies**
   ```python
   !pip install cryptography
   ```

3. **Run the Cells**
   - Generate encryption key
   - Add, view, or update password records
   - Save and export the encrypted vault file

---

## 🔒 Security Notice

- All passwords are encrypted with AES (via Fernet).
- The encryption key is unique per session — export it for future use!
- Data is not transmitted to any server. Full offline security.

---

## 📁 Sample File Structure

```
PassVault/
├── PassVault.ipynb          # Main Google Colab notebook
├── vault.json               # Encrypted password storage (generated)
├── key.key                  # Encryption key (export manually)
├── LICENSE                  # License
├── README.md               # Project description and instructions
```

---

## 📚 Learning Resources

- [Cryptography (Python)](https://cryptography.io/en/latest/)
- [Fernet Encryption](https://cryptography.io/en/latest/fernet/)
- [Google Colab Documentation](https://colab.research.google.com/)
- [Text-based CLI Projects in Python](https://realpython.com/tutorials/cli/)

---

## 🧠 Future Enhancements

- Web version with Flask + HTML frontend
- SQLite-based storage
- User authentication via master password
- Password strength meter

---

## 📜 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for more information.

---

## 🙋‍♀️ Author

**Debanga**  
Student | Python Developer | Passionate about Privacy  
[GitHub Profile](https://github.com/Debanga-06)
