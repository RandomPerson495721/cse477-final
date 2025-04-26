from datetime import datetime, timedelta, time

import mysql.connector
import csv
from io import StringIO
import itertools
from hashlib import scrypt
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
        self.tables         = ['events', 'users', 'event_user_slots']
        
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
        return self.query(query)

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

    def getEvent(self, event_id):
        events = self.query(f"SELECT * FROM events WHERE event_id = '{event_id}'")
        if len(events) == 0:
            return []

        # Turn the event into a dictionary
        event = events[0]
        event['invitee_emails'] = event['invitee_emails'].split(',')
        event['invitee_emails'] = [e.strip() for e in event['invitee_emails']]
        start_time: timedelta = event['start_time']
        end_time: timedelta = event['end_time']
        event['slots'] = int((end_time - start_time) / timedelta(minutes=30))

        start_date: datetime = event['start_date']
        end_date: datetime = event['end_date']
        event['days'] = (end_date - start_date).days + 1
        # Return the first event
        return event

    def createEvent(self, user, name, start_date, end_date, start_time, end_time, invitee_emails):
        # Event Name: a short descriptive title for the event (e.g., “Team Meeting Scheduler”).
        # Start Date and End Date: these define the date range over which availability will be collected. Both dates must be inclusive.
        # Daily Time Range: the hours of the day in which availability will be collected (e.g., 8:00 AM to 8:00 PM).
        # List of Invitee Emails: a comma-separated list of email addresses belonging to registered users who should be allowed to view and participate in the event.
        event_id = self.insertRows('events', ['owner_id', 'name', 'start_date', 'end_date', 'start_time', 'end_time', 'invitee_emails'], [[user, name, start_date, end_date, start_time, end_time, invitee_emails]])
        return {'success': 1, 'event_id': event_id[0]['LAST_INSERT_ID()']}

    def getUserAvailability(self, user, event_id):
        # Get the event
        query = f"SELECT e_column, e_row, status FROM event_user_slots WHERE event_id = {event_id} AND user_id = {user} ORDER BY e_column, e_row"
        slots = self.query(query)
        if len(slots) == 0:
            return []

        res: dict = {}
        # turn it into a dictionary
        for i in range(len(slots)):
            res[(slots[i]['e_row'], slots[i]['e_column'])] = slots[i]['status']

        return res

    def updateUserAvailability(self, event_id, user, slots):
        # Update the user's availability
        for slot in slots:
            self.query(f"DELETE from event_user_slots WHERE event_id = {event_id} AND user_id = {user} AND e_column = {slot['column']} AND e_row = {slot['row']}")
            self.insertRows('event_user_slots', ['event_id', 'user_id', 'e_column', 'e_row', 'status'], [[event_id, user, slot['column'], slot['row'], slot['status']]])

        pass

    def getUserEvents(self, user):
        # Get all events
        events = self.query(f"SELECT event_id, name, start_date, end_date, users.email as owner_email FROM events INNER JOIN users on events.owner_id = users.user_id WHERE owner_id = {user['user_id']} OR FIND_IN_SET('{user['email']}', invitee_emails) > 0")
        return events

    def getHeatmapData(self, event_id):
        query = f"SELECT e_column, e_row, status, COUNT(*) as count FROM event_user_slots WHERE event_id = {event_id} GROUP BY e_column, e_row, status"
        slots = self.query(query)
        if len(slots) == 0:
            return {}
        res: dict = {}

        # turn it into a dictionary
        for i in range(len(slots)):
            key = f"{slots[i]['e_row']}_{slots[i]['e_column']}"

            if (key == "00"):
                print("key")

            if key not in res:
                res[key] = {}

            if slots[i]['status'] not in res[key]:
                res[key][slots[i]['status']] = 0

            res[key][slots[i]['status']] += slots[i]['count']

        return res
