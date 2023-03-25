import sqlite3


class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, column_names_and_types):
        # generate the SQL statement to create the table
        create_table_stmt = f"CREATE TABLE {table_name} ("
        for column_name, column_type in column_names_and_types.items():
            create_table_stmt += f"{column_name} {column_type}, "
        create_table_stmt = create_table_stmt[:-2] + ")"

        # execute the SQL statement to create the table
        self.cursor.execute(create_table_stmt)

    def insert_data(self, table_name, data):
        # generate the SQL statement to insert data into the table
        insert_data_stmt = f"INSERT INTO {table_name} VALUES ("
        for value in data.values():
            insert_data_stmt += f"'{value}', "
        insert_data_stmt = insert_data_stmt[:-2] + ")"

        # execute the SQL statement to insert data into the table
        self.cursor.execute(insert_data_stmt)
        self.conn.commit()

    def select_data(self, table_name, column_names=None, where_clause=None):
        # generate the SQL statement to select data from the table
        select_data_stmt = f"SELECT "
        if column_names:
            select_data_stmt += ", ".join(column_names)
        else:
            select_data_stmt += "*"
        select_data_stmt += f" FROM {table_name}"
        if where_clause:
            select_data_stmt += f" WHERE {where_clause}"

        # execute the SQL statement to select data from the table
        self.cursor.execute(select_data_stmt)
