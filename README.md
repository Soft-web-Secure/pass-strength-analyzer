# pass-strength-analyzer
Advanced password strength assessment tool with real-time validation against keyboard patterns, common vulnerabilities, and NIST-aligned entropy scoring.

# 🔐 Password Security Analyzer

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20|%20Linux%20|%20macOS-lightgrey.svg)]()

> Offline password strength assessment tool with real-world attack vector simulation

## 🎯 Overview

**Password Security Analyzer** evaluates password strength using professional security criteria, including detection of:

- ⌨️ **Keyboard walking patterns** (`qweasdzxc`, `poi;lk.,m`, `qazwsxedc`)
- 📅 **Date patterns** (birthdays, years, DDMMYYYY)
- 🔁 **Repetitive sequences** (`aaaaaa`, `123123123`)
- 📈 **Alphabetical/numerical sequences** (`abcdefg`, `123456789`)
- 🧩 **Common weak patterns** (dictionary-based detection)
- 📊 **Entropy scoring** (1–10 scale aligned with NIST guidelines)

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔍 **Real-time validation** | Instant feedback on password entry |
| 🎲 **Secure generator** | Built-in password generator (minimum score 8/10) |
| 📋 **No telemetry** | Fully offline – your passwords never leave your device |
| 🎨 **Modern UI** | Clean interface with ttkbootstrap theming |
| 📁 **Portable** | Single `.exe` – no installation required |
