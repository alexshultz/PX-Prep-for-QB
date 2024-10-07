# PX-Prep-for-QB

**PX-Prep-for-QB** is a set of Python scripts designed to process Point-of-Sale (POS) and bank transaction data for easy import into QuickBooks. These scripts automate the formatting, calculation, and categorization of sales and transaction data, ensuring that it is ready for financial reporting.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Setting up the Conda Environment](#setting-up-the-conda-environment)
4. [Scripts Overview](#scripts-overview)
    - [px_prep_bank_data.py](#px_prep_bank_datapy)
    - [pos_sales_processor.py](#pos_sales_processorpy)
5. [Usage](#usage)
    - [Running `px_prep_bank_data.py`](#running-px_prep_bank_datapy)
    - [Running `pos_sales_processor.py`](#running-pos_sales_processorpy)
6. [License](#license)

---

## Project Overview

PX-Prep-for-QB is built for organizations that use POS systems and need to prepare the data for seamless import into QuickBooks. The project includes two main scripts:

1. **`px_prep_bank_data.py`**: Processes bank transaction data, filters Square Inc. transactions, and formats them for QuickBooks import.
2. **`pos_sales_processor.py`**: Processes POS sales data, calculates sales tax, and generates a structured CSV file ready for QuickBooks.

---

## Features

- **Bank Data Processing**: Filters transactions and groups them by day for easier reporting.
- **POS Sales Processing**: Automatically calculates sales tax and organizes sales categories such as admissions, donations, and gift sales.
- **Configurable Output**: Both scripts allow flexible output file and folder naming, either manually specified or automatically generated.
- **Easy-to-Use**: Designed to be run as simple command-line scripts, making it easy to integrate into your workflow.

---

## Installation

### Prerequisites

Before using this project, you need:

- **Conda** (package management system and environment manager)
- **Python 3.x** (installed within a Conda environment)

### Setting up the Conda Environment

To install and run PX-Prep-for-QB, follow these steps:

1. **Clone the Repository**:
2. 
    ````bash
    git clone https://github.com/yourusername/PX-Prep-for-QB.git
    cd PX-Prep-for-QB
    ````

2. **Create and activate a Conda environment**:
    You already have a Conda environment `qb` created with Python 3 installed:
    
    ````bash
    conda create --name qb python=3
    ````
    Activate the environment:
    ````bash
    conda activate qb
    ````

3. **Install the required dependencies**:
    The project uses `pandas` for data processing. Install the dependencies listed in the `requirements.txt`:
    
    ````bash
    pip install -r requirements.txt
    ````

---

## Scripts Overview

### `px_prep_bank_data.py`

#### Purpose:
This script processes bank transaction data, specifically filtering transactions from Square Inc., and outputs them in a format suitable for import into QuickBooks.

#### Key Features:
- Filters transactions where `Credit` is not null and the description starts with `Square Inc`.
- Saves each day’s transactions in a separate CSV file.
- Flexible output folder specification, either manually set or auto-generated.

---

### `pos_sales_processor.py`

#### Purpose:
This script processes POS sales data, calculates the appropriate sales tax, and outputs formatted sales data into a CSV file ready for QuickBooks import.

#### Key Features:
- Handles different categories like admissions, gift sales, donations, and sales tax.
- Automatically calculates and processes sales tax for each category.
- Option to specify output file, or the script will generate a default output file.

---

## Usage

Once the environment is set up and the required dependencies are installed, you can run the scripts using the following instructions:

### Running `px_prep_bank_data.py`

#### Command-Line Usage:

````bash
python px_prep_bank_data.py <input_file> [-o <output_folder>] [-t <template_file>]
````

#### Parameters:

- `<input_file>`: The path to the CSV file containing bank transaction data.
- `-o`, `--output`: (Optional) The output folder where the processed CSV files will be saved. If not provided, the script will create a folder with the name of the input file and append `_output`.
- `-t`, `--template`: (Optional) The path to the template CSV file that defines the output structure. Defaults to `table_template.csv` in the working directory.

#### Example:

````bash
python px_prep_bank_data.py transactions.csv -o ./output_folder -t ./template_file.csv
````

This will process the `transactions.csv` file, save the output in `output_folder`, and use `template_file.csv` to structure the output.

---

### Running `pos_sales_processor.py`

#### Command-Line Usage:

````bash
python pos_sales_processor.py <input_csv> [-o <output_csv>]
````

#### Parameters:

- `<input_csv>`: The path to the CSV file containing sales data.
- `-o`, `--output`: (Optional) The output CSV file to write the processed data. If not provided, it defaults to `<input_file>_output.csv`.

#### Example:

````bash
python pos_sales_processor.py sales_data.csv -o formatted_output.csv
````

This will process the `sales_data.csv` file and save the formatted output to `formatted_output.csv`.

---

## License

This project is licensed under the **CC0 1.0 Universal (CC0 1.0) Public Domain Dedication**. This means that the code is released into the public domain, and you are free to use, modify, and distribute it without any restrictions.

For more information, see the [LICENSE](LICENSE) file or visit the [Creative Commons website](https://creativecommons.org/publicdomain/zero/1.0/).

---

### Additional Notes

- You may need to customize the template CSV file used in `px_prep_bank_data.py` based on the structure required by your QuickBooks import.
- Test the output files with a small dataset before using them with your actual QuickBooks data to ensure the formats are correct.

Feel free to contribute or raise any issues you encounter while using PX-Prep-for-QB!

>
