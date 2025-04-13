import mysql.connector
import glob
import json
import csv
from io import StringIO
import itertools
import hashlib
from hashlib import scrypt
import os
import cryptography
from cryptography.fernet import Fernet
from math import pow

class database:

    def __init__(self, purge = False):

        # Grab information from the configuration file
        self.database       = 'db'
        self.host           = '127.0.0.1'
        self.user           = 'master'
        self.port           = 3306
        self.password       = 'master'
        self.tables         = ['institutions', 'positions', 'experiences', 'skills','feedback', 'users']
        
        # NEW IN HW 3-----------------------------------------------------------------
        self.encryption     =  {   'oneway': {'salt' : b'averysaltysailortookalongwalkoffashortbridge',
                                                 'n' : int(pow(2,5)),
                                                 'r' : 9,
                                                 'p' : 1
                                             },
                                'reversible': { 'key' : '7pK_fnSKIjZKuv_Gwc--sZEMKn2zc8VvD6zS96XcNHE='}
                                }
        #-----------------------------------------------------------------------------

    def query(self, query = "SELECT * FROM users", parameters = None):

        cnx = mysql.connector.connect(host     = self.host,
                                      user     = self.user,
                                      password = self.password,
                                      port     = self.port,
                                      database = self.database,
                                      charset  = 'latin1'
                                     )


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

    def createTables(self, purge=False, data_path = 'flask_app/database/'):
        ''' FILL ME IN WITH CODE THAT CREATES YOUR DATABASE TABLES.'''

        #should be in order or creation - this matters if you are using forign keys.
         
        if purge:
            for table in self.tables[::-1]:
                self.query(f"""DROP TABLE IF EXISTS {table}""")
            
        # Execute all SQL queries in the /database/create_tables directory.
        for table in self.tables:
            
            #Create each table using the .sql file in /database/create_tables directory.
            with open(data_path + f"create_tables/{table}.sql") as read_file:
                create_statement = read_file.read()
            self.query(create_statement)

            # Import the initial data
            try:
                params = []
                with open(data_path + f"initial_data/{table}.csv") as read_file:
                    scsv = read_file.read()            
                for row in csv.reader(StringIO(scsv), delimiter=','):
                    params.append(row)
            
                # Insert the data
                cols = params[0]; params = params[1:] 
                self.insertRows(table = table,  columns = cols, parameters = params)
            except:
                print('no initial data')

    def insertRows(self, table='table', columns=['x','y'], parameters=[['v11','v12'],['v21','v22']]):
        
        # Check if there are multiple rows present in the parameters
        has_multiple_rows = any(isinstance(el, list) for el in parameters)
        keys, values      = ','.join(columns), ','.join(['%s' for x in columns])
        
        # Construct the query we will execute to insert the row(s)
        query = f"""INSERT IGNORE INTO {table} ({keys}) VALUES """
        if has_multiple_rows:
            for p in parameters:
                query += f"""({values}),"""
            query     = query[:-1] 
            parameters = list(itertools.chain(*parameters))
        else:
            query += f"""({values}) """                      
        
        insert_id = self.query(query,parameters)[0]['LAST_INSERT_ID()']         
        return insert_id

#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################
    def createUser(self, email='me@email.com', password='password', role='user'):
        # Encrypt the password
        password = self.onewayEncrypt(password)

        # Check if the user already exists in the database
        user = self.query(f"SELECT * FROM users WHERE email = '{email}'")
        if len(user) > 0:
            return {'success': 0, 'error': 'User already exists'}

        # Insert the user into the database
        self.insertRows('users', ['email', 'password', 'role'], [[email, password, role]])
        return {'success': 1}

    def authenticate(self, email='me@email.com', password='password'):
        # Decrypt the password
        password = self.onewayEncrypt(password)
        # Get the user from the database
        user = self.getUser(email)
        # Check if user exists and password is correct
        if len(user) == 0:
            return {'success': 0, 'error': 'User does not exist'}

        if user['password'] != password:
            return {'success': 0, 'error': 'Incorrect password'}

        return {'success': 1}

    def onewayEncrypt(self, string):
        encrypted_string = scrypt(string.encode('utf-8'),
                                          salt = self.encryption['oneway']['salt'],
                                          n    = self.encryption['oneway']['n'],
                                          r    = self.encryption['oneway']['r'],
                                          p    = self.encryption['oneway']['p']
                                          ).hex()
        return encrypted_string


    def reversibleEncrypt(self, type, message):
        fernet = Fernet(self.encryption['reversible']['key'])
        
        if type == 'encrypt':
            message = fernet.encrypt(message.encode())
        elif type == 'decrypt':
            message = fernet.decrypt(message).decode()

        return message

    def getUser(self, email):
        users = self.query(f"SELECT * FROM users WHERE email = '{email}'")
        if len(users) == 0:
            return []

        # Return the first user
        return users[0]

#######################################################################################
# RESUME RELATED
#######################################################################################
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


