import mysql.connector
import glob
import json
import csv
from io import StringIO
import itertools
import datetime


class database:

    def __init__(self, purge=False):

        # Grab information from the configuration file
        self.database = 'db'
        self.host = '127.0.0.1'
        self.user = 'master'
        self.port = 3306
        self.password = 'master'

    def query(self, query="SELECT CURDATE()", parameters=None):

        cnx = mysql.connector.connect(host=self.host, user=self.user, password=self.password, port=self.port,
                                      database=self.database, charset='latin1')

        if parameters is not None:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query, parameters)
        else:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query)

        # Fetch one result
        row = cur.fetchall()
        cnx.commit()

        if "INSERT" in query:
            cur.execute("SELECT LAST_INSERT_ID()")
            row = cur.fetchall()
            cnx.commit()
        cur.close()
        cnx.close()
        return row

    def about(self, nested=False):
        query = """select concat(col.table_schema, '.', col.table_name) as 'table',
                          col.column_name                               as column_name,
                          col.column_key                                as is_key,
                          col.column_comment                            as column_comment,
                          kcu.referenced_column_name                    as fk_column_name,
                          kcu.referenced_table_name                     as fk_table_name
                    from information_schema.columns col
                    join information_schema.tables tab on col.table_schema = tab.table_schema and col.table_name = tab.table_name
                    left join information_schema.key_column_usage kcu on col.table_schema = kcu.table_schema
                                                                     and col.table_name = kcu.table_name
                                                                     and col.column_name = kcu.column_name
                                                                     and kcu.referenced_table_schema is not null
                    where col.table_schema not in('information_schema','sys', 'mysql', 'performance_schema')
                                              and tab.table_type = 'BASE TABLE'
                    order by col.table_schema, col.table_name, col.ordinal_position;"""
        results = self.query(query)
        if nested == False:
            return results

        table_info = {}
        for row in results:
            table_info[row['table']] = {} if table_info.get(row['table']) is None else table_info[row['table']]
            table_info[row['table']][row['column_name']] = {} if table_info.get(row['table']).get(
                row['column_name']) is None else table_info[row['table']][row['column_name']]
            table_info[row['table']][row['column_name']]['column_comment'] = row['column_comment']
            table_info[row['table']][row['column_name']]['fk_column_name'] = row['fk_column_name']
            table_info[row['table']][row['column_name']]['fk_table_name'] = row['fk_table_name']
            table_info[row['table']][row['column_name']]['is_key'] = row['is_key']
            table_info[row['table']][row['column_name']]['table'] = row['table']
        return table_info

    def createTables(self, purge=False, data_path='flask_app/database/'):
        # Create the tables
        order: list = ['feedback', 'institutions', 'positions', 'experiences', 'skills']

        # Drop the tables if purge is true
        if purge:
            for table in order[::-1]:
                self.query(f"DROP TABLE IF EXISTS {table}")

        # Create the tables
        for table in order:
            with open(f'{data_path}create_tables/{table}.sql') as f:
                query = f.read()
                self.query(query)

        # Insert data into the tables from csv except for feedback
        for table in order[1:]:
            with open(f'{data_path}initial_data/{table}.csv') as f:
                reader = csv.reader(f)
                columns = next(reader)
                rows = list(reader)
                self.insertRows(table, columns, rows)

    def insertRows(self, table='table', columns=['x', 'y'], parameters=[['v11', 'v12'], ['v21', 'v22']]):
        # Insert a row into the database
        query = f"INSERT INTO {table} ({','.join(columns)}) VALUES "

        # For each row, add the values to the query
        for paramList in parameters:
            query += "("

            # For each value in the row, add it to the query
            for param in paramList:
                if param == 'NULL':
                    query += f"{param},"
                else:
                    query += f"'{param}',"
            query = query[:-1] + "),"

        query = query[:-1] + ";"
        self.query(query)

    def getResumeData(self):

        institutions = self.query("SELECT * FROM institutions")

        resume_data = {}

        # Loop through each institution
        for i in range(len(institutions)):
            positions = self.query(
                f"SELECT position_id, title, responsibilities, start_date, end_date FROM positions WHERE inst_id = {institutions[i]['inst_id']}")
            # Create an empty dictionary for the positions
            institutions[i]['positions'] = {}

            # Loop through each position
            for j in range(len(positions)):
                experiences = self.query(
                    f"SELECT experience_id, name, description, hyperlink, start_date, end_date FROM experiences WHERE position_id = {positions[j]['position_id']}")
                # Create an empty dictionary for the experiences
                positions[j]['experiences'] = {}

                # Loop through each experience
                for k in range(len(experiences)):
                    skills = self.query(
                        f"SELECT name, skill_level FROM skills WHERE experience_id = {experiences[k]['experience_id']}")
                    # Create an empty dictionary for the skills
                    experiences[k]['skills'] = {}

                    # Loop through each skill
                    for l in range(len(skills)):
                        # Add the skill to the dictionary with an in-order index
                        experiences[k]['skills'][l + 1] = skills[l]

                    # Add the experience to the dictionary with an in-order index
                    positions[j]['experiences'][k + 1] = experiences[k]

                    # Pop the experience_id from the dictionary
                    experiences[k].pop('experience_id')

                # Add the position to the dictionary with an in-order index
                institutions[i]['positions'][j + 1] = positions[j]

                # Pop the position_id from the dictionary
                positions[j].pop('position_id')

            # Add the institution to the dictionary with an in-order index
            resume_data[i + 1] = institutions[i]

            # Pop the inst_id from the dictionary
            institutions[i].pop('inst_id')

        return resume_data
