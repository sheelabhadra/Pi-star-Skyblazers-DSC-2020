import time
import argparse
from tqdm import tqdm
import pandas as pd


class DataCompressor(object):
    """docstring for DataCompressor"""
    def __init__(self, csv_file_path, excel_file_path, pickle_file_path):
        super(DataCompressor, self).__init__()
        self.csv_file_path = csv_file_path
        self.excel_file_path = excel_file_path
        self.pickle_file_path = pickle_file_path
        self.data_dict = {}
        self.category_cols = []
        self.numeric_cols = []
        self.date_cols = []


    def create_data_dict(self, chunk_size):
        def count_rows(exclude_header=True):
            with open(self.csv_file_path) as fp:
                count = 0
                for _ in fp:
                    count += 1

            return count - 1 if exclude_header else count

        total_rows = count_rows()
        it = total_rows//chunk_size + 1

        for i in tqdm(range(it)):
            if i == it - 1:
                self.data_dict["chunk_{}".format(i)] = pd.read_csv(self.csv_file_path, 
                    skiprows=i*chunk_size, nrows=(total_rows - i*chunk_size), low_memory=False)
            else:
                self.data_dict["chunk_{}".format(i)] = pd.read_csv(self.csv_file_path, 
                    skiprows=i*chunk_size, nrows=chunk_size, low_memory=False)
            if i == 0:
                col_names = self.data_dict["chunk_{}".format(i)].columns
            else:
                self.data_dict["chunk_{}".format(i)].columns = col_names

        for i in range(it):
            print("chunk_{} shape = {}.".format(i, self.data_dict["chunk_{}".format(i)].shape))


    def read_column_types(self):
        df = pd.read_excel(self.excel_file_path)
        for _, row in df.iterrows():
            if row['TYPE'] == 'Nominal' or row['TYPE'] == 'Ordinal' or row['TYPE'] == 'Binary':
                self.category_cols.append(row['ATTRIBUTE'])
            if row['TYPE'] == 'Interval':
                self.numeric_cols.append(row['ATTRIBUTE'])
            if row['TYPE'] == 'yyyymmdd':
                self.date_cols.append(row['ATTRIBUTE'])


    def add_column_names(self, cols, col_type="Category"):
        if col_type == "Category":
            self.category_cols.extend(cols)
        if col_type == "Numeric":
            self.numeric_cols.extend(cols)
        if col_type == "Datetime":
            self.date_cols.extend(cols)


    def compress_dataset(self):
        def convert_nan(df, cols):
            for col in cols:
                df[col].fillna(-9999, inplace=True)
        
        def convert_to_categorical(df, cols):
            for col in cols:
                df[col].astype('category', inplace=True)
        
        def convert_to_integer(df, cols):
            for col in cols:
                df[col] = pd.to_numeric(df[col], downcast='integer', errors='ignore')
        
        def convert_to_datetime(df, cols):
            for col in cols:
                df[col] = pd.to_datetime(df[col])
        
        n_keys = len(self.data_dict.keys())
        dfs = []
        for i in tqdm(range(n_keys)):
            df = self.data_dict['chunk_{}'.format(i)].copy()
            df.rename(columns={'Route': 'ROUTE'}, inplace=True)
            convert_nan(df, self.category_cols + self.numeric_cols)
            convert_to_integer(df, self.numeric_cols)
            convert_to_datetime(df, self.date_cols)
            dfs.append(df)
        
        del self.data_dict
        print("Concatenating chunks!")
        compressed_df = pd.concat(dfs)
        compressed_df.reset_index(drop=True, inplace=True)
        convert_to_categorical(compressed_df, self.category_cols)
        print("Final dataframe shape: {}".format(compressed_df.shape))
        del dfs
        
        print("Saving as pickle file!")
        compressed_df.to_pickle(self.pickle_file_path)
        del compressed_df


parser = argparse.ArgumentParser()
parser.add_argument('-csv', '--csv-file-path', help='Path to CSV file',
    default='../data/FlightDelays.csv', type=str)
parser.add_argument('-xls', '--xls-file-path', help='Path to excel file containing column descriptions',
    default='../data/FlightDataDescription.xlsx', type=str)
parser.add_argument('-pkl', '--pkl-file-path', help='Path to pickle file',
    default='../data/flight_delays.pkl', type=str)
args = parser.parse_args()

dc = DataCompressor(args.csv_file_path, args.xls_file_path, args.pkl_file_path)
start = time.time()
print("====== Creating data dictionary ======")
dc.create_data_dict(chunk_size=1000000)
print("Data dictionary created in {} s.".format(time.time() - start))
dc.read_column_types()
dc.add_column_names(cols=['CARRIER', 'QUARTER', 'MONTH', 'DAY_OF_MONTH', 'DAY_OF_WEEK'], col_type="Category")
print("========= Compressing data ===========")
dc.compress_dataset()
print("Done! Total compression time: {} s.".format(time.time() - start))
print("======================================")
