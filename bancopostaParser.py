import camelot
import pandas as pd
import matplotlib.pyplot as plt

class BancopostaParser:
    def __init__(self, input_path: str):
        self.path = input_path  
        #The columns are hardcoded because the table is always the same in terms of width, this improves the extraction of the tables
        self.pdf = camelot.read_pdf(self.path, flavor='stream', pages='all', columns = ['30,79,128,224,319'])
        self.num_pages = len(self.pdf)
        self.pages = []
        # Get all tables from all pages
        for i in range(self.num_pages):
            self.pages.append(self.get_page(i))
        # Remove first row from first page
        self.pages[0] = self.pages[0].iloc[1:]
        # Drop rows with empty values in the first column
        for i in range(self.num_pages):
            # Drop the first column (it's empty)
            self.pages[i] = self.pages[i].iloc[:,1:]
            self.pages[i] = self.pages[i][self.pages[i].iloc[:, 0].notnull()]
            self.pages[i].reset_index(drop=True, inplace=True)
        self.df = pd.concat(self.pages)
        #Drop the second and last column and last two rows
        self.df = self.df.iloc[:-3, [0,2,3,4]]
        # Drop rows where the first column is empty -> ones with only description
        self.df = self.df[self.df.iloc[:, 0] != ""]
        # Convert strings to datetime objects -> used to filter by date
        self.df.iloc[:, 0] = pd.to_datetime(self.df.iloc[:, 0], format='%d/%m/%y', errors='coerce').dt.date
        #reset index
        self.df.reset_index(drop=True, inplace=True)
        # Rename columns: Data, Uscite, Entrate, Causale
        self.df.columns = ['Data', 'Uscite', 'Entrate', 'Causale']

    def get_page(self, page: int):
        return self.pdf[page].df
    
    def get_df(self):
        return self.df
    
    def export_csv(self, filename: str):
        try:
            self.df.to_csv(filename + ".csv", index=False)
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
    
    def export_excel(self, filename: str):
        try:
            self.df.to_excel(filename + ".xlsx", index=False)
        except Exception as e:
            print(f"Error exporting to Excel: {e}")
    
    def filter_by_date(self, start_date: str, end_date: str, date_column=0, path = "./",export = False) -> pd.DataFrame:
        # Ensure start_date and end_date are datetime.date objects
        try:
            start_date = pd.to_datetime(start_date, format='%d/%m/%y').date()
            end_date = pd.to_datetime(end_date, format='%d/%m/%y').date()
        except Exception as e:
            print(f"Error converting dates: {e}")
            return None
        # Filter by date
        try:
            filtered = self.df[(self.df.iloc[:, date_column] >= start_date) & (self.df.iloc[:, date_column] <= end_date)]
        except Exception as e:
            print(f"Error filtering by date: {e}")
            return None
        if export:   
            filtered.to_excel(path + start_date.strftime('%d-%m-%y') + "_" + end_date.strftime('%d-%m-%y') + ".xlsx", index=False)
        return filtered
    
    def preview_contour(self, page = 0):
        camelot.plot(self.pdf[page], kind='grid').show()
        plt.show()
    
