import sys
from db import Database
from PyQt5.QtWidgets import *

db = Database('visma.db')

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visma")
        self.setGeometry(50, 50, 600, 600)
        self.client_info = ["FirmaID", "Firmanavn", "Adresse", "Postadresse", "Telefon", "Fax"]
        self.ref_info = ["PersonID", "FirmaID", "Etternavn", "Fornavn", "Tittel", "Telefon", "epost"]
        self.load_db()
        self.UI()
    

    def load_db(self):
        data = db.fetch_all_clients()
        self.all_clients = []
        for row in range(len(data)):
            self.all_clients.append((data[row][0], data[row][1]))


    def UI(self):
        # Header
        self.header = QLabel("Visma Kundebank", self)
        self.header.move(10, 10)

        # Search
        self.search_prompt = QLineEdit(self)
        self.search_prompt.setPlaceholderText("Sok på kunde")
        self.search_prompt.move(10, 50)
        self.search_btn = QPushButton("Sok", self)
        self.search_btn.move(150, 50)
        self.search_btn.clicked.connect(self.search)

        # View all button
        self.view_all_btn = QPushButton("Se alle", self)
        self.view_all_btn.move(250, 50)
        self.view_all_btn.clicked.connect(self.view_all_clients)

        # Legg til-button
        self.add_client_btn = QPushButton("Legg til kunde", self)
        self.add_client_btn.move(350, 50)
        self.add_client_btn.clicked.connect(self.add_client)

        # Slett-button
        self.add_client_btn = QPushButton("Slett kunde", self)
        self.add_client_btn.move(480, 50)
        self.add_client_btn.clicked.connect(self.delete_client)

        # Search result list
        self.result_h = QLabel("Resultater", self)
        self.result_h.move(10, 80)
        self.search_results = QListWidget(self)
        self.search_results.move(10, 100)
        # When item on the list is clicked
        self.search_results.itemClicked.connect(self.on_client_clicked)

        # Client info list
        self.client_info_h = QLabel("Info", self)
        self.client_info_h.move(300, 80)
        self.info_list = QListWidget(self)
        self.info_list.move(300, 100)

        # Reference people list and reference infolist
        self.ref_h = QLabel("Referansepersoner", self)
        self.ref_h.move(10, 300)
        self.ref_list = QListWidget(self)
        self.ref_list.move(10, 320)
        # When name on ref list is clicked
        self.ref_list.itemClicked.connect(self.on_ref_clicked)
        self.ref_info_h = QLabel("Info", self)
        self.ref_info_h.move(300, 300)
        self.ref_info_list = QListWidget(self)
        self.ref_info_list.move(300, 320)

        # Add and delete reference person buttons
        self.add_ref_btn = QPushButton("Legg til referanse", self)
        self.del_ref_btn = QPushButton("Slett referanse", self)
        self.add_ref_btn.move(10, 520)
        self.del_ref_btn.move(120, 520)
        self.add_ref_btn.clicked.connect(self.add_reference)
        self.del_ref_btn.clicked.connect(self.delete_reference)

        self.show()
    
    
    def on_client_clicked(self):
        self.ref_info_list.clear()
        client = self.search_results.currentItem().text()
        id = int(client.split("-")[0])
        self.get_client_info(id)
        self.get_ref_persons(id)
    

    def on_ref_clicked(self):
        # Get ref id
        ref = self.ref_list.currentItem().text()
        id = int(ref.split("-")[0])
        # Collect info on ref
        self.get_ref_info(id)
    

    def get_client_info(self, id):
        data = db.fetch_client_info(id)
        self.populate_info_list(data)
    

    def get_ref_persons(self, id):
        data = db.fetch_contacts(id)
        names = []
        # Just take out names
        for person in range(len(data)):
            # Make string of PersonID, first name and last name
            line = str(data[person][0]) + '-' + data[person][3] + ' ' + data[person][2]
            names.append(line)
        self.populate_ref_list(names)

    
    def get_ref_info(self, id):
        data = db.fetch_contact_info(id)
        self.populate_ref_info_list(data)


    def search(self):
        firma = self.search_prompt.text()
        self.search_prompt.clear()
        data = db.search_by_name(firma)
        if data != []:
            self.populate_results(data)
        elif firma == "":
            QMessageBox.information(self, "Advarsel", "Du må legge inn et kundenavn, eller kundetype")
        else:
            QMessageBox.information(self, "Advarsel", "Kunne ikke finne {}\n Appen er 'case'-sensitiv for øybelikket".format(firma))
    

    def view_all_clients(self):
        self.search_results.clear()
        self.populate_results(self.all_clients)
    

    def populate_results(self, data):
        self.search_results.clear()
        for item in data:
            client = str(item[0]) + '-' + item[1]
            self.search_results.addItem(client)
    

    def populate_info_list(self, data):
        self.info_list.clear()
        data = data[0]
        for item in range(len(data)):
            row = self.client_info[item] + ": " + str(data[item])
            self.info_list.addItem(row)
    

    def populate_ref_info_list(self, data):
        self.ref_info_list.clear()
        data = data[0]
        for item in range(len(data)):
            row = self.ref_info[item] + ": " + str(data[item])
            self.ref_info_list.addItem(row)
    

    def populate_ref_list(self, names):
        self.ref_list.clear()
        for name in names:
            self.ref_list.addItem(name)


    def add_client(self):
        self.new_client = AddClient(self, self.client_info)
        #self.close()


    def add_reference(self):
        if self.search_results.currentItem() == None:
            QMessageBox.information(self, "Advarsel", "Du må velge en kunde")
            return
        else:
            client = self.search_results.currentItem().text().split('-')
            clientID = int(client[0])
            client_name = client[1]
            self.new_ref = AddReference(self, self.ref_info, clientID)


    def delete_reference(self):
        if self.ref_list.currentItem() == None:
            QMessageBox.information(self, "Advarsel", "Du må velge en referanseperson")
        else:
            ref = self.ref_list.currentItem().text().split('-')
            refID = int(ref[0])
            ref_name = ref[1]
            clientID = db.fetch_contact_info(refID)[0][1]
            reply = QMessageBox.question(self, "Advarsel", "Er du sikkert på at du vil slette {}?".format(ref_name))
            if reply == QMessageBox.Yes:
                try:
                    db.delete_reference(refID)
                    QMessageBox.information(self, "Vellykket", "{} ble slettet".format(ref_name))
                    self.refresh_db()
                    self.get_ref_persons(clientID)
                except Exception as e:
                    QMessageBox.information(self, "Advarsel", "No gikk galt. Kunne ikke slette {} \n Exception error: {}".format(ref_name, e))
    

    def delete_client(self):
        if self.search_results.currentItem() == None:
            QMessageBox.information(self, "Advarsel", "Du må velge en kunde")
            return
        else:
            client = self.search_results.currentItem().text().split('-')
            clientID = int(client[0])
            client_name = client[1]
            reply = QMessageBox.question(self, "Advarsel", "Er du sikkert på at du vil slette {}?".format(client_name))
            if reply == QMessageBox.Yes:
                try:
                    db.delete_client(clientID)
                    QMessageBox.information(self, "Vellykket", "{} ble slettet fra kundebanken".format(client_name))
                    self.refresh_db()
                except:
                    QMessageBox.informtaion(self, "Advarsel", "No gikk galt. Kunne ikke slette {} fra kundebanken".format(client_name))
            else:
                return
    
    
    def refresh_db(self):
        self.load_db()
        self.view_all_clients()


class AddClient(QWidget):
    def __init__(self, window, info):
        super().__init__()
        self.setWindowTitle("Legg til kunde")
        self.setGeometry(450, 150, 260, 200)
        self.client_info = info
        self.UI()
        self.show()
        self.window = window
        
    
    def UI(self):
        self.labels = []
        self.inputs = []
        x = 10
        y = 10
        xinput = 80
        increment = 25
        for i in range((len(self.client_info)) - 1):
            self.labels.append(QLabel((self.client_info[i+1] + ': '), self))
            self.labels[i].move(x, y)
            self.inputs.append(QLineEdit(self))
            self.inputs[i].move(xinput, y)
            y += increment

        self.add_btn = QPushButton("Legg til", self)
        self.abort_btn = QPushButton("Avbryt", self)
        self.add_btn.move(10, 170)
        self.abort_btn.move(160, 170)
        self.add_btn.clicked.connect(self.add_client)
        self.abort_btn.clicked.connect(self.close)
    
    #def closeEvent(self, event): #Innebygd funksjon
        #self.window.refresh_db()
        #self.main = Window()
    
    def add_client(self):
        self.input_data = []
        for i in range((len(self.client_info)) - 1):
            self.input_data.append(self.inputs[i].text())

        if (self.input_data[0] != "" and self.input_data[3] != ""):
            try:        
                db.add_client(self.input_data)
                QMessageBox.information(self, "Utfort!", "Kunde lagt til")
                self.window.refresh_db()
                self.close()
                #self.window = Window()
            except:
                QMessageBox.information(self, "Advarsel", "Noe gikk galt")
                pass
        else:
            QMessageBox.information(self, "Advarsel", "Du må legge til navn og telefon")

class AddReference(QWidget):
    def __init__(self, window, info, clientID):
        super().__init__()
        self.setWindowTitle("Legg til Referanseperson")
        self.setGeometry(450, 150, 260, 240)
        self.window = window
        self.clientID = clientID
        self.ref_info = info
        self.UI()
        self.show()
        
    
    def UI(self):
        self.labels = []
        self.inputs = []
        x = 10
        y = 10
        xinput = 80
        increment = 25
        for i in range((len(self.ref_info)) - 2):
            self.labels.append(QLabel((self.ref_info[i+2] + ': '), self))
            self.labels[i].move(x, y)
            self.inputs.append(QLineEdit(self))
            self.inputs[i].move(xinput, y)
            y += increment

        self.add_btn = QPushButton("Legg til", self)
        self.abort_btn = QPushButton("Avbryt", self)
        self.add_btn.move(10, 170)
        self.abort_btn.move(160, 170)
        self.add_btn.clicked.connect(self.add_ref)
        self.abort_btn.clicked.connect(self.close)
    
    #def closeEvent(self, event): #Innebygd funksjon
        #self.main = Window()
    
    def add_ref(self):
        self.input_data = []
        for i in range((len(self.ref_info)) - 2):
            self.input_data.append(self.inputs[i].text())
        
        print(self.input_data)

        if (self.input_data[0] == "" or self.input_data[1] == "" or self.input_data[3] == ""):
            QMessageBox.information(self, "Advarsel", "Du må legge til et fullt navn og telefonnummer")
        else:
            try:
                db.add_reference(self.clientID, self.input_data)
                QMessageBox.information(self, "Utfort!", "Referanseperson lagt til")
                # Refresh
                self.window.refresh_db()
                self.window.get_ref_persons(self.clientID)
                self.close()
            except:
                QMessageBox.information(self, "Advarsel", "Noe gikk galt")


def main():
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec_()) 

main()