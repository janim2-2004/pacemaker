import sqlite3
from sqlite3 import Error


class Database:
    # Database class using sqlite3 for the purpose of local user data storage on hard drive

    def __init__(self):
        # Attempt connection to local db file if possible, else creates a new db file in the current working directory

        try:
            self.conn = sqlite3.connect("data/userdata.db")
            print("User database opened")
            self.curr = self.conn.cursor()
        except Error:
            print(Error)
    
    def createtable(self):
        # Method that creates a table within the database to store usernames and passwords

        create_datatable =  """CREATE TABLE IF NOT EXISTS data(
            id Integer PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
            );
            """
        self.curr.execute(create_datatable)
        self.conn.commit()
        
        create_paramtable = """CREATE TABLE IF NOT EXISTS params(
            id Integer PRIMARY KEY AUTOINCREMENT,
            mode DEFAULT 0,
            lrl DEFAULT 60,
            url DEFAULT 120,
            a_amp DEFAULT 5.0,
            a_pw DEFAULT 1,
            v_amp DEFAULT 5.0,
            v_pw DEFAULT 1,
            vrp DEFAULT 320,
            arp DEFAULT 250,
            aSens DEFAULT 0.0,
            vSens DEFAULT 0.0,
            rateAdapt DEFAULT 0,
            msr DEFAULT 120,
            actThres DEFAULT 2,
            reactTime DEFAULT 30,
            resFactor DEFAULT 8,
            recTime DEFAULT 5,
            avDelay DEFAULT 150
            );
            """
        self.curr.execute(create_paramtable)
        self.conn.commit()
    
    def insertuser(self, userdata):
        # Method that inserts new userdata into the database
        # There is a max of 10 users, so it will reject adding an 11th user; this limit can be incremented
        # @param userdata - a tuple comprised of (username, password)

        rowQuery = "SELECT Count() FROM data"
        self.curr.execute(rowQuery)
        rows = self.curr.fetchone()[0]
        if (rows < 10): # Condition that checks for max users in the database (current limit is 10)
            insert_data =   """INSERT INTO data(username, password)
                VALUES(?,?);
                """
            self.curr.execute(insert_data, userdata)
            self.conn.commit()
            insert_param = "INSERT INTO params DEFAULT VALUES;"
            self.curr.execute(insert_param)
            self.conn.commit()
            return 1
        return 0
    
    def searchusers(self, user):
        # Method that enables the traversal of database to find corresponding userdata
        # @param user - a tuple comprised of (username, ); password can be ignored for user search

        search_user = "SELECT * FROM data WHERE username = (?);"
        self.curr.execute(search_user, user)

        rows = self.curr.fetchall()
        if rows == []:
            return 1
        return 0
    
    def authenticate(self, user, userinput):
        # Method to check if username and password exist in the database
        # @param user - tuple of (username, ); password does not matter, parameter used for userdata retrieval
        # @param userinput - tuple of (username, password)

        authentication = "SELECT * FROM data WHERE username = (?);"
        self.curr.execute(authentication, user)
        row = self.curr.fetchall()
        if row [0][1] == userinput[0]:
            return row[0][2] == userinput[1]

    def searchparam(self, user):
        search_user = "SELECT * from data WHERE username = (?);"
        self.curr.execute(search_user, user)
        self.rowid = self.curr.fetchall()

        search_params = "SELECT * from params WHERE id = (?);"
        self.curr.execute(search_params, (self.rowid[0][0],))
        params = self.curr.fetchall()
        return params

    def updateParams(self, parameters):
        newTup = parameters + (self.rowid[0][0],)
        updateComm = """UPDATE params
            SET mode = ?,
                lrl = ?,
                url = ?,
                a_amp = ?,
                a_pw = ?,
                v_amp = ?,
                v_pw = ?,
                vrp = ?,
                arp = ?,
                aSens = ?,
                vSens = ?,
                rateAdapt = ?,
                msr = ?,
                actThres = ?,
                reactTime = ?,
                resFactor = ?,
                recTime = ?,
                avDelay = ?
            WHERE id = ?
        ;
        """
        self.curr.execute(updateComm, newTup)
        self.conn.commit()