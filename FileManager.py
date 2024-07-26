from pyspark.sql import SparkSession
from DatabaseManager import DatabaseManager


class FileManager:
    def __init__(self):
        self.spark_session = SparkSession.builder.appName("squirrel-data").getOrCreate()
        self.db_manager = DatabaseManager()

    def __load_csv(self, file_path):
        # TODO: validate if file exists
        data_frame = self.spark_session.read.csv(file_path, header=True, inferSchema=True)
        return data_frame

    def load_squirrels_data(self, file_path):
        data_frame = self.__load_csv(file_path)

        # Store Parks data
        parks_values = data_frame.select("Park ID").distinct().collect()
        parks = [{"id": row["Park ID"]} for row in parks_values]
        print("- Parks data: ", parks)
        self.db_manager.store_data("parks", "id", parks)

        # Store Colors data
        colors_values = data_frame.select("Primary Fur Color").distinct().collect()
        colors = [{"name": row["Primary Fur Color"]} for row in colors_values if row["Primary Fur Color"]]
        print("- Colors data: ", colors)
        self.db_manager.store_data("colors", "id", colors)

        # Store Squirrels data
        squirrels_values = data_frame.select(["Squirrel ID", "Activities", "Park ID", "Primary Fur Color"]).distinct().collect()
        colors_ids_dict = {row["name"]: row["id"] for row in self.db_manager.get_data("colors", get_distinct=True)}
        squirrels = [{
            "id": row["Squirrel ID"],
            "activities": row["Activities"],
            "park_id": row["Park ID"],
            "primary_fur_color_id": colors_ids_dict[row["Primary Fur Color"]] if row["Primary Fur Color"] else None
        } for row in squirrels_values]
        print("- Squirrels data: ", squirrels)
        self.db_manager.store_data("squirrels", "id", squirrels, update_on_conflict=True)

        print("=> Parks, Colors and Squirrels data was loaded and stored")

    def load_parks_data(self, file_path):
        data_frame = self.__load_csv(file_path)

        # Store Areas data
        areas_values = data_frame.select(["Area ID", "Area Name"]).distinct().collect()
        areas = [{"id": row["Area ID"], "name": row["Area Name"]} for row in areas_values]
        print("- Areas data: ", areas)
        self.db_manager.store_data("areas", "id", areas, update_on_conflict=True)

        # Store Parks data
        parks_values = data_frame.select(["Park Name", "Park ID", "Other Animal Sightings", "Area ID"]).distinct().collect()

        def format_id_number(value):
            return str(int(value)) if value == int(value) else str(value)

        parks = [{
            "id": format_id_number(row["Park ID"]),
            "name": row["Park Name"],
            "area_id": row["Area ID"],
            "other_animal_sightings": row["Other Animal Sightings"]
        } for row in parks_values]
        print("-Parks data: ", parks)
        self.db_manager.store_data("parks", "id", parks, update_on_conflict=True)
        print("=> Areas and Parks data was loaded and stored")


if __name__ == '__main__':
    file_manager = FileManager()
    file_manager.load_squirrels_data("./data/squirrel-data.csv")
    file_manager.load_parks_data("./data/park-data.csv")
