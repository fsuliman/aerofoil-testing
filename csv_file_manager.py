import csv
import time

class CSVFileManager:
    def __init__(self):
        self.file_obj = None
        self.independent_var_name_in_header = None

    def new_csv_file(self, file_name, independent_var_name_in_header):
        if self.file_obj != None:
            self.file_obj.close()
            print(f"Closed {self.file_name} in preparation for operating on a new file")
        self.file_name = file_name
        self.file_obj = open(self.file_name, 'w', encoding = 'utf-8', newline="")
        self.independent_var_name_in_header = independent_var_name_in_header
        csv_writer = csv.writer(self.file_obj, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        csv_writer.writerow([self.independent_var_name_in_header, "Reading", "Timestamp"])
        print(f"Opened new file {self.file_name} for writing")

    def open_csv_file_for_append(self, file_name):
        if self.file_obj != None:
            self.file_obj.close()
            print(f"Closed {self.file_name} in preparation for opening a new file")
        self.file_name = file_name
        self.file_obj = open(self.file_name, 'a+', encoding = 'utf-8', newline="")
        self.file_obj.seek(0,2)
        print(f"Opened {self.file_name} for appending")

    def close_csv_file(self):
        if self.file_obj != None:
            self.file_obj.close()
            self.file_obj = None
            print(f"Closed {self.file_name}")
            
    def get_csv_file_object(self):
        if self.file_obj != None:
            return(self.file_obj)
        else:
            return None    

    def write_csv_file(self, data):
        if self.file_obj != None:
            csv_writer = csv.writer(self.file_obj, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            # add a timestamp to the reading data
            data.append(time.strftime("%Y-%m-%d %H:%M:%S"))
            csv_writer.writerow(data)
            print(f"Wrote {data} to {self.file_name}")
    
    def sniff_independent_var_name_in_header(self):
        if self.file_obj != None:
            curr_position = self.file_obj.tell()
            self.file_obj.seek(0,0)
            sniffed_independent_var_name_in_header = csv.reader(self.file_obj).__next__()[0]
            self.file_obj.seek(curr_position,0)
            print(f"Sniffed independent variable header name: {sniffed_independent_var_name_in_header}")
            return sniffed_independent_var_name_in_header
        else:
            return ""
        
        
""" Test code"""
def main():
    csv_file_manager = CSVFileManager()
    csv_file_manager.new_csv_file("test-1.csv", "Airspeed")
    csv_file_manager.write_csv_file([100, 0.1])
    csv_file_manager.write_csv_file([200, 0.2])
    csv_file_manager.close_csv_file()

    csv_file_manager.open_csv_file_for_append("test-1.csv")
    csv_file_manager.write_csv_file([300, 0.3])
    csv_file_manager.write_csv_file([400, 0.4])
    csv_file_manager.close_csv_file()

    csv_file_manager.open_csv_file_for_append("test-1.csv")
    csv_file_manager.write_csv_file([500, 0.5])
    csv_file_manager.write_csv_file([600, 0.6])
    csv_file_manager.close_csv_file()

    csv_file_manager = CSVFileManager()
    csv_file_manager.new_csv_file("test-2.csv", "Camber/Shape ID")
    csv_file_manager.write_csv_file(["D-12", 0.1])
    csv_file_manager.write_csv_file(["D-13", 0.2])
    csv_file_manager.close_csv_file()

    csv_file_manager.open_csv_file_for_append("test-2.csv")
    csv_file_manager.write_csv_file(["D-14", 0.3])
    csv_file_manager.write_csv_file(["D-15", 0.4])
    csv_file_manager.close_csv_file()

if __name__ == "__main__":
    main()