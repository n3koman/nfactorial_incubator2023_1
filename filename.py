import pymongo
import csv
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

while True:
    db_list = client.list_database_names()

    print(f"Available Databases: {db_list}")

    db_name = input("Enter a database name or type 'new' to create a new database: ")

    if db_name == "new":
        db_name = input("Enter a new database name: ")
        db = client[db_name]
        print(f"Database '{db_name}' created successfully!")
    elif db_name in db_list:
        db = client[db_name]
        print(f"Switched to database '{db_name}'")
    else:
        print(f"Database '{db_name}' does not exist!")
        create_new = input("Do you want to create a new database with this name? (y/n): ")

        if create_new.lower() == "y":
            db = client[db_name]
            print(f"Database '{db_name}' created successfully!")
        else:
            continue

    while True:
        col_names = db.list_collection_names()
        print(f"\nCurrent Database: {db_name}")
        print(f"Available Collections: {col_names}")
        col_name = input("Enter a collection name or type 'new' to create a new collection: ")
        if col_name == "new":
            col_name = input("Enter a new collection name: ")
            mycol = db[col_name]
            print(f"Collection '{col_name}' created successfully!")
        elif col_name in col_names:
            mycol = db[col_name]
            print(f"Switched to collection '{col_name}'")
        elif col_name not in col_names:
            print(f"Collection '{col_name}' does not exist!")
            create_new = input("Do you want to create a new collection with this name? (y/n): ")

            if create_new.lower() == "y":
                mycol = db[col_name]
                print(f"Collection '{col_name}' created successfully!")
            else:
                continue

        #insert data
        def insert_data():
            num_docs = int(input("Enter the number of documents to insert : "))
            docs = []
            for i in range(num_docs):
                print(f"Enter the fields for document #{i+1} without comma (For example: name age city): ")
                doc = {}
                for field in input().split():
                    value = input(f"Enter {field}: ")
                    doc[field] = value
                docs.append(doc)
            result = mycol.insert_many(docs)
            print("Data inserted successfully.")

        #view data
        def view_data():
            cursor = mycol.find()
            for document in cursor:
                print(document)

        #update data
        def update_data():
            try:
                filter_field = input("Enter the name of the field to filter by: ")
                filter_value = input("Enter the value to filter by: ")
                filter_query = {filter_field: filter_value}

                update_field = input("Enter the name of the field to update: ")
                update_value = input("Enter the new value: ")
                update_query = {"$set": {update_field: update_value}}

                result = mycol.update_many(filter_query, update_query)
                return result.modified_count
            except Exception as e:
                print(f"An error occurred while updating data: {e}")
                return 0

        #delete data
        def delete_data():
            try: 
                filter_field = input("Enter the name of the field to filter by: ")
                filter_value = input("Enter the value to filter by: ")
                filter_query = {filter_field: filter_value}

                result = mycol.delete_many(filter_query)
                print(f"{result.deleted_count} documents deleted")
            except Exception as e:
                print(f"An error occurred while deleting data: {e}")

        #retrieve data
        def retrieve_data():
            try:
                filter_field = input("Enter the name of the field to filter by: ")
                filter_value = input("Enter the value to filter by: ")
                filter_query = {filter_field: filter_value}

                sort_field = input("Enter the name of the field to sort by (optional): ")
                sort_direction = int(input("Enter the sort direction (1 for ascending, -1 for descending): ")) if sort_field else None
                sort_query = {sort_field: sort_direction} if sort_field else None

                projection_fields = input("Enter a comma-separated list of fields to project (optional): ")
                projection_query = {field: 1 for field in projection_fields.split(',')} if projection_fields else None

                result = mycol.find(filter_query, projection_query).sort(sort_query) if sort_query else mycol.find(filter_query, projection_query)
                for document in result:
                    print(document)
            except Exception as e:
                print(f"An error occurred while retrieving data: {e}")

        #save data
        def save_data():
            data = list(mycol.find())
            if len(data) == 0:
                print("No data found to save")
                return
            with open(f"{db_name}_{col_name}.csv", mode='w', newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(data[0].keys())
                for row in data:
                    writer.writerow(row.values())
            print("Data saved in CSV format")

        while True:
            print("Choose an action:")
            print("1. Insert data")
            print("2. View data")
            print("3. Update data")
            print("4. Delete data")
            print("5. Retrieve data")
            print("6. Save data")
            print("7. Choose another collection")

            choice = int(input("Enter choice: "))

            if choice == 1:
                insert_data()
            elif choice == 2:
                view_data()
            elif choice == 3:
                update_data()
            elif choice == 4:
                delete_data()
            elif choice == 5:
                retrieve_data()
            elif choice == 6:
                save_data()
            elif choice == 7:
                break
            else:
                print("Invalid choice.")
        change_db = input("Do you want to change database? (y/n): ")
        if change_db.lower() == "y":
            break
        else:
            continue
    
