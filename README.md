# Extracting Zoom Personal Meeting ID (PMI) from a Forensic Disk Image  
*A Live-System DFIR Workflow for Windows E01 Images*

![Badge](https://img.shields.io/badge/DFIR-Zoom%20PMI%20Extraction-blue)

---

## Table of Contents

- [Why the Zoom PMI Matters](#why-the-zoom-pmi-matters)
- [Why You Need a Live System](#why-you-need-a-live-system)
- [Technical Background](#technical-background)
- [Tools and Dependencies](#tools-and-dependencies)
- [Workflow (Step-by-Step)](#workflow-step-by-step)
- [Troubleshooting Tips](#troubleshooting-tips)
- [Ethics and Legal Considerations](#ethics-and-legal-considerations)
- [Contributing](#contributing)
- [Acknowledgements](#acknowledgements)
- [License](#license)

---

## 🧭 Why the Zoom PMI Matters

Zoom assigns every user a **Personal Meeting ID (PMI)** — a static, unique identifier tied to that account. From a forensic standpoint, it serves as:

- **Attribution**: Connects the suspect to meetings they hosted.
- **Timeline Correlation**: Matches session data to other evidence (e.g., emails, chats).
- **Legal Relevance**: Helps validate or challenge claims about meeting attendance or organization.

Extracting this PMI supports forensic investigations involving:

- Insider threats  
- Harassment or fraud over Zoom  
- Compliance audits  
- Identity spoofing

---

## Why You Need a Live System

Zoom encrypts sensitive user data — including the PMI — using **Windows Data Protection API (DPAPI)**, which:

- Links encryption to the **user’s login credentials**
- Secures master keys in `AppData\Roaming\Microsoft\Protect\<SID>\*`
- Only decrypts properly **within the original user context**

This makes **static forensic tools insufficient**.  
To access and decrypt the PMI, we must:

1. Convert the E01 disk image to a bootable VM  
2. Log into the live system using the user’s credentials  
3. Extract decryption keys in memory using tools like **Mimikatz**

---

## Technical Background

Here’s how Zoom secures the PMI:

1. **Secret Key**: Stored in `zoom.us.ini`, DPAPI-encrypted
2. **Encrypted Database**: Stored in `zoomus.enc.db`
3. **Combined String**: PMI and other tokens encrypted using AES (with the secret key)

To decrypt it:
- We extract the **DPAPI master key**
- Use it to unlock the **Zoom secret key**
- Use the secret key to decrypt the **Zoom database**
- Extract the **Base64-encrypted combined string**
- Finally, **derive the AES key** from the user SID and decrypt it

---

## Tools and Dependencies

| Tool         | Use                                  |
|--------------|---------------------------------------|
| FTK Imager   | Convert `.E01` image to raw `.dd`    |
| VBoxManage   | Convert `.dd` to `.vmdk`             |
| VirtualBox   | Boot the VM                          |
| Mimikatz     | Extract DPAPI master key and secrets |
| sqlite3      | Query the Zoom database              |
| Python 3     | Run AES decryption script            |

---

## Workflow (Step-by-Step)

### Step 1: Convert the E01 to a Bootable VM

Use FTK Imager to convert `.E01` to `.dd`, then:

```bash
VBoxManage convertfromraw final_dd.001 final_vm.vmdk --format VMDK
```

Create a new VirtualBox VM and attach `final_vm.vmdk`. Enable **EFI** if needed and boot the machine.

---

### 🔹 Step 2: Log in and Extract DPAPI Master Key

Inside the VM (using the user’s recovered PIN or password), open Mimikatz and run:
- mimikatz # privilege::debug
- mimikatz # sekurlsa::dpapi


This reveals the **DPAPI master key** tied to the user’s SID.

---

### 🔹 Step 3: Extract and Decrypt the Zoom Secret Key

Move the `zoom.us.ini` file into the Mimikatz directory, then run:
- mimikatz # dpapi::decrypt /in:zoom.us.ini /unprotect


Copy the **Base64-decoded secret key** to a secure location.

---

### 🔹 Step 4: Query the Zoom Encrypted Database

From within the live system:
- sqlite3 zoomus.enc.db "SELECT value FROM zoom_kv WHERE key='some_key';"


Export the **encrypted combined string** to a text file.

---

### 🔹 Step 5: Decrypt the Combined String (Reveal the PMI)

Run the Python decryption script:
python decrypt_pmi.py --sid "S-1-5-21-XXXXX"
--secret-key "DECODED_SECRET_KEY"
--combined-string "ENCRYPTED_COMBINED_STRING"


The output will include the **user’s Personal Meeting ID (PMI)**.

---

## 🧩 Troubleshooting Tips

- **No bootable medium?** → Check that the VM disk is attached and EFI is enabled.  
- **Decryption errors?** → Double-check Base64 trimming and correct SID.  
- **Mimikatz fails?** → Use `privilege::debug` before DPAPI commands.

---

## ⚖️ Ethics and Legal Considerations

- ✅ Ensure legal authority before decrypting any user data  
- 📝 Log and document every step for chain-of-custody  
- 🧪 Isolate the VM from external networks to avoid contamination or leakage  
- 🔐 Only use Mimikatz in authorized forensic contexts

---

## 🤝 Contributing

Have an idea, fix, or script to improve this workflow?  
Feel free to **fork**, **contribute**, or **submit pull requests**.

---

## 🙏 Acknowledgements

- [gentilkiwi / Mimikatz](https://github.com/gentilkiwi/mimikatz)  
- [University of Baltimore](https://www.ubalt.edu/) – Cyber Forensics Program  
- [Prudential Associates](https://www.prudentialassociates.com/) – Real-world DFIR Environment

---

## 📜 License

This repository is intended for **educational and research purposes only**.  
Please attribute the author if used in derivative works or investigations.

---

**Author:**  
**Daniel Kwaku Ntiamoah Addai**  
Graduate Research Assistant – *University of Baltimore*  
Senior DFIR Specialist – *Prudential Associates*





