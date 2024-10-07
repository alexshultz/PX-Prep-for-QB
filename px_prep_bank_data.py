import pandas as pd
import os
import sys
import argparse

class BankDataProcessor:
    def __init__(self, input_file, output_folder=None, template_file="table_template.csv"):
        self.input_file = input_file
        self.template_file = template_file
        self.output_folder = output_folder or self._generate_output_folder()

        # Create output folder if it doesn't exist
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
            print(f"Created output directory: {self.output_folder}")

    def _generate_output_folder(self):
        """Generate output folder based on the input file name if no folder is provided."""
        input_file_name = os.path.splitext(os.path.basename(self.input_file))[0]
        return f"{input_file_name}_output"

    def load_data(self):
        """Load input CSV and template CSV."""
        try:
            self.df = pd.read_csv(self.input_file)
            self.template_df = pd.read_csv(self.template_file, header=None)
        except Exception as e:
            print(f"Error reading the file: {e}")
            sys.exit(1)

    def filter_and_sort_data(self):
        """Filter and sort the bank data based on the criteria."""
        # Convert 'Date' to datetime format
        self.df['Date'] = pd.to_datetime(self.df['Date'])

        # Filter rows where 'Credit' is not null and 'Description' starts with 'Square Inc'
        self.df_filtered = self.df[self.df['Credit'].notna() & self.df['Description'].str.startswith('Square Inc')]

        # Sort by 'Date' and 'Credit'
        self.df_sorted = self.df_filtered.sort_values(['Date', 'Credit'])

    def prepare_output_structure(self):
        """Prepare the output DataFrame structure based on the template."""
        self.output_columns = self.template_df.iloc[0].tolist()
        self.input_mapping = self.template_df.iloc[1].tolist()
        self.constant_values = self.template_df.iloc[2].tolist()

    def save_batches(self):
        """Group and save the filtered data into batches based on unique dates."""
        file_count = 0

        while not self.df_sorted.empty:
            output_data = []
            indices_to_remove = []

            # Add one record per day to the output data
            for index, row in self.df_sorted.iterrows():
                if row['Date'] not in [r[0] for r in output_data]:
                    output_row = []
                    for i in range(len(self.output_columns)):
                        if pd.notna(self.input_mapping[i]):
                            output_row.append(row[self.input_mapping[i]])
                        elif pd.notna(self.constant_values[i]):
                            output_row.append(self.constant_values[i])
                        else:
                            output_row.append(None)
                    output_data.append((row['Date'], output_row))
                    indices_to_remove.append(index)

            # Create a DataFrame for the current batch
            output_df = pd.DataFrame([r[1] for r in output_data], columns=self.output_columns)

            # Save the current batch to a file
            output_file_name = os.path.join(self.output_folder, f'formatted_deposits_{file_count}.csv')
            output_df.to_csv(output_file_name, index=False)
            print(f"Saved {output_file_name}")

            # Remove processed rows from df_sorted
            self.df_sorted = self.df_sorted.drop(indices_to_remove)
            file_count += 1

        print("All records have been processed.")

    def process(self):
        """Run the entire processing pipeline."""
        self.load_data()
        self.filter_and_sort_data()
        self.prepare_output_structure()
        self.save_batches()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process bank transactions CSV file.")
    parser.add_argument("input_file", help="Path to the input CSV file.")
    parser.add_argument("-o", "--output", help="Path to the output folder (optional). If not provided, a folder with '_output' will be created.")
    parser.add_argument("-t", "--template", default="table_template.csv", help="Path to the CSV template file (optional). Defaults to 'table_template.csv'.")

    args = parser.parse_args()

    # Create the processor instance and run the processing pipeline
    processor = BankDataProcessor(input_file=args.input_file, output_folder=args.output, template_file=args.template)
    processor.process()