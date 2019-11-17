import sqlite3

class Database:
    def __init__(self, database):
        self.conn = sqlite3.connect(database)
        self.c = self.conn.cursor()

    def fetch_all_clients(self):
        self.c.execute("SELECT * FROM Kunde")
        data = self.c.fetchall()
        return data
    
    def fetch_client_info(self, id):
        self.c.execute("SELECT * FROM Kunde WHERE FirmaID = ?", (id,))
        data = self.c.fetchall()
        return data
    
    def fetch_contacts(self, id):
        self.c.execute("SELECT * FROM Referanseperson WHERE FirmaID = ?", (id,))
        data = self.c.fetchall()
        return data
    
    def fetch_contact_info(self, id):
        self.c.execute("SELECT * FROM Referanseperson WHERE PersonID = ?", (id,))
        data = self.c.fetchall()
        return data

    def add_client(self, data):
        query = "INSERT INTO Kunde (Firmanavn, Adresse, Postadresse, Telefon, Fax) \
            VALUES (?, ?, ?, ?, ?)"
        self.c.execute(query, (data[0], data[1], data[2], data[3], data[4]))
        self.conn.commit()
    
    def __del__(self):
        self.conn.close()
