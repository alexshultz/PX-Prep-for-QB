import csv
import pandas as pd
import argparse
from typing import Dict, List
import os
from pandas import to_datetime  # Add this to your imports if needed

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
    """
    Convert a monetary value to float, handling various input formats.
    
    Args:
        value: Input value that could be string (e.g. '$1,234.56'), float, int, 
              pandas.Series, or None/NaN
    
    Returns:
        float: Cleaned monetary amount
        
    Examples:
        >>> clean_amount('$1,234.56')
        1234.56
        >>> clean_amount(1234.56)
        1234.56
        >>> clean_amount(pd.NA)
        0.0
    """
    if isinstance(value, (float, int)):
        return float(value)
    if pd.isna(value):
        return 0.0
    if isinstance(value, pd.Series):
        return value.apply(lambda x: clean_amount(x)).sum()
    return float(value.replace('$', '').replace(',', ''))

def process_sales_data(input_csv: str, output_csv: str) -> None:
    """
    Process Square POS sales data and write formatted output for QuickBooks.
    
    Reads transaction data, groups by date and category, calculates daily totals,
    and writes records in QuickBooks import format.
    
    Args:
        input_csv: Path to input CSV file from Square
        output_csv: Path where formatted output CSV will be written
        
    Categories are mapped as follows:
    - 'Admission' -> POS:admissions
    - 'Donation' -> POS:donation
    - All others -> POS:sales (gift shop items)
    
    Sales tax is accumulated daily and output as POS:tax
    """
    try:
        # Read the input CSV
        df = pd.read_csv(input_csv)
        
        # Convert monetary columns to float first
        df['Net Sales'] = df['Net Sales'].apply(clean_amount)
        df['Tax'] = df['Tax'].apply(clean_amount)
        
        # Convert Date column to datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Map categories to our four output categories
        df['ProcessedCategory'] = df['Category'].apply(
            lambda x: 'Admission' if x == 'Admission'
                     else 'Donation' if x == 'Donation'
                     else 'gift sale'
        )
        
        # Group by Date and ProcessedCategory, sum Net Sales and Tax
        # Using numeric aggregation instead of string concatenation
        grouped_data = df.groupby(['Date', 'ProcessedCategory'], as_index=False).agg({
            'Net Sales': 'sum',
            'Tax': 'sum'
        })
        
        # Get unique dates
        dates = sorted(grouped_data['Date'].unique())

        with open(output_csv, 'w', newline='') as output_file:
            writer = csv.writer(output_file)
            writer.writerow(HEADER)
            
            for date in dates:
                date_data = grouped_data[grouped_data['Date'] == date]
                
                # Track total tax for the day
                total_tax = 0
                
                # Process admissions (POS:admissions)
                admission_data = date_data[date_data['ProcessedCategory'] == 'Admission']
                if not admission_data.empty:
                    net_amount = admission_data['Net Sales'].iloc[0]
                    write_record(writer, str(date.date()), 'Admission', net_amount)
                    total_tax += admission_data['Tax'].iloc[0]
                
                # Process gift sales (POS:sales)
                gift_sales = date_data[date_data['ProcessedCategory'] == 'gift sale']
                if not gift_sales.empty:
                    net_amount = gift_sales['Net Sales'].sum()
                    write_record(writer, str(date.date()), 'gift sale', net_amount)
                    total_tax += gift_sales['Tax'].sum()
                
                # Process sales tax (POS:tax)
                if total_tax > 0:
                    write_record(writer, str(date.date()), 'sales tax', total_tax)
                
                # Process donations (POS:donation)
                donation_data = date_data[date_data['ProcessedCategory'] == 'Donation']
                if not donation_data.empty:
                    amount = donation_data['Net Sales'].iloc[0]
                    write_record(writer, str(date.date()), 'Donation', amount)
                
    except Exception as e:
        print(f"An error occurred while processing the file: {e}")

def write_record(writer: csv.writer, date: str, category: str, amount: float) -> None:
    """
    Write a single record to the QuickBooks import CSV.
    
    Args:
        writer: CSV writer object
        date: Transaction date in YYYY-MM-DD format
        category: Transaction category (Admission, gift sale, sales tax, or Donation)
        amount: Transaction amount
        
    Writes a row with QuickBooks import fields including deposit account,
    date, memo, received from, category codes, and amount.
    """
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