from FileManager import FileManager

if __name__ == '__main__':
    file_manager = FileManager()
    file_manager.load_squirrels_data("./data/squirrel-data.csv")
    file_manager.load_parks_data("./data/park-data.csv")
