from csv import DictReader


class DumpDB:
    """class for creating objects representing the database dump and methods
    for working with it"""

    def __init__(self):
        self.dump_db = []

    def load_from_csv(self, path_to_csv_file):
        """loads data from a csv file"""

        with open(path_to_csv_file, 'r') as file:
            reader = DictReader(file)
            for row in reader:
                item = {key: value for key, value in row.items()}
                item['id'] = int(item['id'])
                self.dump_db.append(item)

    def select_fields(self, field_name, filter=None):
        """returns a list of field values filtered by function filter"""

        if filter is None:
            filter = lambda x: True

        return [item[field_name] for item in self.dump_db if filter(item[field_name])]

    def select_items(self, field_name, filter=None):
        """returns a list of items filtered by field_name"""

        if filter is None:
            filter = lambda x: True

        return [item for item in self.dump_db if filter(item[field_name])]
