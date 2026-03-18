# Logger

A minimal Windows keylogger / activity logger written in Python.  
Compiled to a single .exe file for fast, local execution.  
No network communication. No persistence. No background process after it finishes.

## How it actually works

The repository contains two main files:

- `Log.py` — the only file that needs to be converted to .exe  
  This is the program that runs on the target machine, captures data for a short time, encrypts it, and writes the encrypted output to a file in the same directory.

- `decoder.py` — runs on your own computer  
  Used to decrypt and convert the logged data into readable text / readable format.

The logger does **not** produce readable output by itself.  
You must use `decoder.py` afterwards to make sense of the collected data.

## Recommended (lowest-trace) usage method

To minimize recoverable traces on the target system:

1. Compile `Log.py` to `logger.exe` (using PyInstaller, Nuitka, etc. — one-file mode recommended)
2. Put only the `logger.exe` file on a USB drive (any location on the drive is fine)
3. Insert the USB into the target Windows computer
4. Double-click and run `logger.exe` **directly from the USB**
5. Wait ~3–5 seconds — the program captures, encrypts, writes the file to the USB, and exits
6. Safely remove the USB drive

**Total time you're physically interacting with the machine:** usually 12–20 seconds  
**Result:** No files are written to the target computer's hard drive or SSD.  
The encrypted log file stays exclusively on the USB.

Running the .exe from the local disk (Desktop, Downloads, Temp folder, etc.) will leave recoverable file system artifacts (MFT entries, USN journal, prefetch, etc.). The USB method is the only approach that avoids writing anything to the host.

## Technical details

| Property              | Value / Status                          |
|-----------------------|-----------------------------------------|
| Platform              | Windows (10/11 tested)                  |
| Admin rights required | No                                      |
| Network activity      | None                                    |
| Persistence           | None — runs once and exits              |
| Active runtime        | ~3–5 seconds after launch               |
| Output                | Single encrypted file on the USB        |
| Decryption            | Requires `decoder.py` on your machine   |
| File size (compiled)  | Usually 200–400 KB (depends on packer)  |

## Important notes

- This is **not** a persistent monitoring tool  
- This is **not** remotely controlled  
- This is **not** stealthy in memory / process list while running  
- It is designed for very short, physical-access-only collection windows

## Legal & ethical warning

This software may only be used:

- on computers **you own**  
- on systems where you have **explicit written permission** from the owner  
- in authorized security testing, red teaming, or research environments

Using this tool on someone else's computer without consent is illegal in virtually every jurisdiction (unauthorized access, interception of electronic communications, computer fraud/abuse statutes, etc.).

You are solely responsible for how you use this code.

Operate only within the law.
