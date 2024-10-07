import csv
import pandas as pd
import argparse
from typing import Dict, List
import os

# Constants
DEPOSIT_TO = "POS Clearing"
MEMO = "gross sales"
RECEIVED_FROM = "POS"
FROM_ACCOUNT = "POS Income"
TAX_RATE = 0.086

HEADER = [
    "Deposit To", "Date", "Memo", "Received From", "From Account", 
    "Line Memo", "Check No.", "Pmt Meth.", "Class", "Amount", 
    "Less Cash Back", "Cash back Accnt.", "Cash back Memo"
]

# Dictionaries for memo and class codes
LINE_MEMOS: Dict[str, str] = {
    "Admission": "admission",
    "gift sale": "gift sale",
    "sales tax": "sales tax",
    "Donation": "donation"
}
CLASS_CODES: Dict[str, str] = {
    "Admission": "POS:admissions",
    "gift sale": "POS:sales",
    "sales tax": "POS:tax",
    "Donation": "POS:donation"
}

def clean_amount(value: any) -> float:
    """Convert string amount to float, removing any non-numeric characters."""
    if isinstance(value, (float, int)):
        return float(value)
    if pd.isna(value):
        return 0.0
    if isinstance(value, pd.Series):
        return value.apply(lambda x: clean_amount(x)).sum()
    return float(value.replace('$', '').replace(',', ''))

def process_sales_data(input_csv: str, output_csv: str) -> None:
    """Process sales data from input CSV and write formatted output to another CSV."""
    try:
        input_df = pd.read_csv(input_csv)
        dates = input_df.columns[1:]

        with open(output_csv, 'w', newline='') as output_file:
            writer = csv.writer(output_file)
            writer.writerow(HEADER)
            
            for date in dates:
                date_data = input_df[['Category', date]].set_index('Category')[date]
                admissions_sales_tax = process_admissions(writer, date, date_data)
                gift_sales_tax = process_gift_sales(writer, date, date_data)
                process_sales_tax(writer, date, admissions_sales_tax + gift_sales_tax)
                process_donations(writer, date, date_data)
    except Exception as e:
        print(f"An error occurred while processing the file: {e}")                

def process_admissions(writer: csv.writer, date: str, date_data: pd.Series) -> float:
    """Process admissions data."""
    sales_tax = 0
    amount = clean_amount(date_data.get('Admission', 0))
    if amount > 0:
        net_amount = amount / (1 + TAX_RATE)
        sales_tax = amount - net_amount
        write_record(writer, date, 'Admission', net_amount)
    return sales_tax

def process_gift_sales(writer: csv.writer, date: str, date_data: pd.Series) -> float:
    """Process gift sales and associated sales tax."""
    sales_tax = 0
    gift_sales_series = date_data[~date_data.index.isin(['Admission', 'Donation'])]
    if not gift_sales_series.empty:
        gift_sales_total = sum(clean_amount(value) for value in gift_sales_series)
        if gift_sales_total > 0:
            write_record(writer, date, 'gift sale', gift_sales_total)
            sales_tax = gift_sales_total * TAX_RATE
    return sales_tax

def process_sales_tax(writer: csv.writer, date: str, total_sales_tax) -> None:
    """Process sales tax data."""
    if total_sales_tax > 0:
        write_record(writer, date, 'sales tax', total_sales_tax)

def process_donations(writer: csv.writer, date: str, date_data: pd.Series) -> None:
    """Process donations data."""
    amount = clean_amount(date_data.get('Donation', 0))
    if amount > 0:
        write_record(writer, date, 'Donation', amount)

def write_record(writer: csv.writer, date:str, category: str, amount: float) -> None:
    """Write a record to the CSV file."""
    writer.writerow([
        DEPOSIT_TO, date, MEMO, RECEIVED_FROM, FROM_ACCOUNT,
        LINE_MEMOS[category], None, None, CLASS_CODES[category],
        round(amount, 2), None, None, None
    ])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process POS sales data and generate a formatted CSV output.")
    parser.add_argument("input_csv", help="The input CSV file containing sales data.")
    parser.add_argument("-o", "--output", help="The output CSV file to write the processed data. If not provided, it defaults to input_filename_output.csv.")
    
    args = parser.parse_args()

    # Generate default output file name if not provided
    if args.output:
        output_csv = args.output
    else:
        base_name = os.path.splitext(args.input_csv)[0]
        output_csv = f"{base_name}_output.csv"

    process_sales_data(args.input_csv, output_csv)