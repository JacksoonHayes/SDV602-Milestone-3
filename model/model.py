"""
This should be the Model class the super class of all Models 
"""
from tkinter.constants import S
from model.data.data_scan import DataManager


class Model():
    class Model:
        """
        This class represents a model.

        Attributes:
            record_set (list): A list of records.
            values (list): A list of values.
            field_names (list): A list of field names.
            data_manager (DataManager): An instance of the DataManager class.
        """

        def __init__(self, data_source=None) -> None:
            """
            Initializes a new instance of the Model class.

            Args:
                data_source (str): The path to the data source file. Defaults to None.
            """
            self.record_set = None
            self.values = None
            self.field_names = None
            self.data_manager = DataManager()

            if data_source is not None:
                csv_file_obj = self.data_manager.get_file(data_source)
                self.record_set, self.values = self.data_manager.scan(csv_file=csv_file_obj, has_header=True)
                self.data_manager.close_file(csv_file_obj)
                self.field_names = [key for key in self.record_set[0]]
        
    def merge(self, source, target):
        self.data_manager.append(target, source)
        
    def get_column(self,column_name):
        if self.record_set and column_name in self.field_names:
            return [record[column_name] for record in self.record_set]

    