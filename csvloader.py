import csv


class CSVLoader:
    '''
    A helper class to read and write to CSV files
    '''

    # Directory where sheets are stored
    sheetDir = "./CSVs/"
    
    def __init__(self, name):
        self.name = name
        self.fieldNames = []
        
    # Read from the CSV file
    def read(self):
        with open(self.sheetDir + self.name, newline='') as f:
            # Get list of field names from first line in CSV
            self.fieldNames = next(csv.reader(f))
            # Create an empty list to represent the sheet
            # Each element is a row (dictionary)
            self.sheet = []
            # Generate a reader that returns a dictionary for each row
            reader = csv.DictReader(f, self.fieldNames)
            for row in reader:
                # Populate sheet list
                self.sheet.append(row)

    # Write to CSV file
    def write(self):
        with open(self.sheetDir + self.name, 'w', newline='') as f:
            # Make sure fieldNames is initialized
            if self.fieldNames == []:
                raise BaseException("Field Names not initalized.")
            else:
                # Generate a writer object
                writer = csv.DictWriter(f, self.fieldNames)
                writer.writeheader()
                writer.writerows(self.sheet)

    # Return dictionary for i-th row
    def getRow(self, i):
        return self.sheet[i]

    def getRows(self):
        return self.sheet

    def findRow(self, key, value):
        for row in self.sheet:
            if row[key] == value:
                return row
        return None

# Some sample code
try:
    loader = CSVLoader("sheet.csv")
    loader.read()
    print(loader.findRow("Serial Number", "2215JBM01778")["IP Address"])
except Exception as exception:
        print("Encountered error: " + str(exception))
