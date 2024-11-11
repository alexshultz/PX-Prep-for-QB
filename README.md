# PX-Prep-for-QB

**PX-Prep-for-QB** helps prepare your Square Point-of-Sale (POS) and bank transaction data for QuickBooks. It automatically organizes your sales data and bank deposits into a format that QuickBooks can understand.

---

## Table of Contents

1. [What Does This Do?](#what-does-this-do)
2. [Before You Start](#before-you-start)
3. [Installation Guide](#installation-guide)
4. [How to Use](#how-to-use)
5. [Getting Help](#getting-help)
6. [License](#license)

---

## What Does This Do?

This tool includes two main parts:

1. **Bank Data Processor** (`px_prep_bank_data.py`): 
   - Finds all your Square deposits in your bank statement
   - Groups them by date
   - Creates QuickBooks-ready deposit records

2. **POS Data Processor** (`px_prep_pos_data.py`):
   - Takes your Square sales data
   - Organizes it into four categories:
     * Admissions
     * Gift Shop Sales
     * Donations
     * Sales Tax
   - Creates daily totals ready for QuickBooks

---

## Before You Start

You'll need:  

1. A computer running Windows, Mac, or Linux  
2. Your Square data:  
 	* Sales data exported from Square  
	* Bank statement showing Square deposits (in CSV format)  
3. Someone to help install the required software (if you're not familiar with Python)

---

## Installation Guide

### Step 1: Install Required Software

1. Download and install Miniconda:
   - Go to: https://docs.conda.io/en/latest/miniconda.html
   - Choose the installer for your system (Windows, Mac, or Linux)
   - Run the installer (accept all default options)

2. After installation, find and open:
   - Windows: "Anaconda Prompt" in the Start Menu
   - Mac/Linux: Terminal application

### Step 2: Set Up the Project

Copy and paste these commands into the Anaconda Prompt/Terminal, pressing Enter after each line:

```bash
# Download the project
git clone https://github.com/yourusername/PX-Prep-for-QB.git

# Go to the project folder
cd PX-Prep-for-QB

# Create a new environment
conda create --name qb python=3

# Activate the environment
conda activate qb

# Install required packages
pip install -r requirements.txt
```

---

## How to Use

### Processing Bank Data

1. Export your bank statement as a CSV file
2. Open Anaconda Prompt/Terminal
3. Type:
```bash
conda activate qb
python px_prep_bank_data.py your_bank_statement.csv
```
4. Find the processed files in the new folder ending with "_output"

### Processing Square Sales Data

1. Export your Square sales data as a CSV file
   * In `squareup.com` look for 
2. Open Anaconda Prompt/Terminal
3. Type:
```bash
conda activate qb
python px_prep_pos_data.py your_square_export.csv
```
4. Find the processed file ending with "_output.csv"

---

## Getting Help

If you run into problems:  

1. Make sure you've activated the environment (`conda activate qb`)
2. Check that your CSV files are in the same folder as the scripts
3. Verify your Square export includes all transaction details
4. Contact your technical support person if you need additional help

---

## License

This is free to use and modify as needed (CC0 1.0 Universal Public Domain Dedication).

---

### Tips
- Always keep backup copies of your original files
- Test with a small amount of data first
- Verify the output in QuickBooks before processing large amounts of data