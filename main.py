import sys
import sqlite3
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem
from school import Ui_MainWindow

def setup_database():
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    # Admin Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute("SELECT COUNT(*) FROM admin")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO admin (username, password) VALUES ('admin', '1234')")
        
    # Students Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            reg_no TEXT PRIMARY KEY, name TEXT, gender TEXT, 
            dob TEXT, age TEXT, address TEXT, phone TEXT, email TEXT, standard TEXT
        )
    ''')
    
    # Teachers Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher_id TEXT, name TEXT, department TEXT, 
            subject TEXT, specialization TEXT, address TEXT, 
            phone TEXT, email TEXT, blood_group TEXT
        )
    ''')
    
    # Marks Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS marks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reg_no TEXT, exam_name TEXT, language TEXT,
            english TEXT, science TEXT, maths TEXT, social_science TEXT
        )
    ''')
    
    # Attendance Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reg_no TEXT, date TEXT, morning TEXT, evening TEXT
        )
    ''')
    
    # Fees Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fees (
            receipt_no TEXT PRIMARY KEY,
            reg_no TEXT, reason TEXT, amount TEXT, date TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Set initial tab to login
        self.ui.tabWidget.setCurrentIndex(0)
        
        # Hide all details (tabs and menu) before login
        self.ui.tabWidget.tabBar().hide()
        self.ui.menubar.setVisible(False)
        
        # Connect buttons
        self.ui.pushButton.clicked.connect(self.login)
        self.ui.pushButton_2.clicked.connect(self.add_student)
        self.ui.pushButton_3.clicked.connect(self.edit_student)
        self.ui.pushButton_4.clicked.connect(self.delete_student)
        
        self.ui.pushButton_5.clicked.connect(self.add_marks)  # Add marks event
        self.ui.pushButton_7.clicked.connect(self.get_marks)  # Get marks event
        self.ui.pushButton_8.clicked.connect(self.edit_marks) # Edit marks
        self.ui.pushButton_6.clicked.connect(self.delete_marks) # Delete marks
        
        # Additional buttons wired to logic
        self.ui.pushButton_9.clicked.connect(self.add_attendance)
        self.ui.pushButton_11.clicked.connect(self.edit_attendance)
        self.ui.pushButton_12.clicked.connect(self.get_attendance)
        self.ui.pushButton_13.clicked.connect(self.delete_attendance)
        
        self.ui.pushButton_14.clicked.connect(self.add_fees)
        self.ui.pushButton_15.clicked.connect(self.get_fees)
        self.ui.pushButton_16.clicked.connect(self.edit_fees) # Edit fees
        self.ui.pushButton_17.clicked.connect(self.delete_fees) # Delete fees
        self.ui.pushButton_18.clicked.connect(self.dummy_print)
        self.ui.pushButton_19.clicked.connect(self.dummy_cancel)
        
        if hasattr(self.ui, 'comboBox_15'):
            self.ui.comboBox_15.addItems(["", "Students", "Marks", "Attendance", "Fees"])
            self.ui.comboBox_15.currentTextChanged.connect(self.load_report)
        
        # Populate student data for editing when combobox changes
        self.ui.comboBox_3.currentTextChanged.connect(self.populate_edit_student)
        if hasattr(self.ui, 'comboBox_13'):
            self.ui.comboBox_13.currentTextChanged.connect(self.populate_fees_receipts)
            
        # Add basic navigation connections
        self.ui.menubar.triggered.connect(self.navigate_menu)
        
        # Initial data load
        self.load_student_ids()
        
    def load_student_ids(self):
        conn = sqlite3.connect('school.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS students (
            reg_no TEXT PRIMARY KEY, name TEXT, gender TEXT, 
            dob TEXT, age TEXT, address TEXT, phone TEXT, email TEXT, standard TEXT)''')
        cursor.execute("SELECT reg_no FROM students")
        student_ids = [str(row[0]) for row in cursor.fetchall()]
        conn.close()
        
        # Clear existing and populate combo boxes with registration numbers (IDs)
        self.ui.comboBox_3.clear()
        self.ui.comboBox_5.clear()
        self.ui.comboBox_6.clear()
        
        if student_ids:
            self.ui.comboBox_3.addItems(student_ids)
            self.ui.comboBox_5.addItems(student_ids)
            self.ui.comboBox_6.addItems(student_ids)
            self.ui.comboBox_8.addItems(student_ids)
            if hasattr(self.ui, 'comboBox_9'):
                self.ui.comboBox_9.addItems(student_ids)
            self.ui.comboBox_10.addItems(student_ids)
            self.ui.comboBox_12.addItems(student_ids)
            self.ui.comboBox_13.addItems(student_ids)
            if hasattr(self.ui, 'comboBox_16'):
                self.ui.comboBox_16.addItems(student_ids)


        import random
        if hasattr(self.ui, 'lineEdit_41'):
            self.ui.lineEdit_41.setText(f"RC{random.randint(100000, 999999)}")
            
    def login(self):
        username = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()
        
        conn = sqlite3.connect('school.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin WHERE username=? AND password=?", (username, password))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            QMessageBox.information(self, "Success", "Login Successful!")
            self.ui.menubar.setVisible(True) # Show details again
            self.ui.tabWidget.tabBar().show()
            self.ui.tabWidget.setCurrentIndex(1)
            self.ui.lineEdit.clear()
            self.ui.lineEdit_2.clear()
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password")
            
    def add_student(self):
        reg_no = self.ui.lineEdit_3.text()
        name = self.ui.lineEdit_4.text()
        gender = self.ui.comboBox.currentText()
        dob = self.ui.lineEdit_5.text()
        age = self.ui.lineEdit_6.text()
        address = self.ui.lineEdit_7.text()
        phone = self.ui.lineEdit_8.text()
        email = self.ui.lineEdit_9.text()
        standard = self.ui.comboBox_2.currentText()
        
        if not reg_no or not name:
            QMessageBox.warning(self, "Error", "Registration Number and Name are required!")
            return
            
        conn = sqlite3.connect('school.db')
        cursor = conn.cursor()
        try:
            cursor.execute('''INSERT INTO students 
                (reg_no, name, gender, dob, age, address, phone, email, standard) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                (reg_no, name, gender, dob, age, address, phone, email, standard))
            conn.commit()
            QMessageBox.information(self, "Success", "Student Added Successfully!")
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Error", "Registration Number already exists!")
        finally:
            conn.close()
            
        self.clear_student_form()
        self.load_student_ids()  # Refresh combo boxes with new student
        self.load_student_ids()  # Refresh combo boxes with new student

    def clear_student_form(self):
        for e in [self.ui.lineEdit_3, self.ui.lineEdit_4, self.ui.lineEdit_5, self.ui.lineEdit_6, self.ui.lineEdit_7, self.ui.lineEdit_8, self.ui.lineEdit_9]: e.clear()

    def populate_edit_student(self, reg_no):
        if not reg_no: return
        conn = sqlite3.connect('school.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, gender, dob, age, address, phone, email, standard FROM students WHERE reg_no = ?", (reg_no,))
        res = cursor.fetchone()
        conn.close()
        if res:
            self.ui.lineEdit_10.setText(res[0]) # Name
            self.ui.lineEdit_11.setText(res[1]) # Gender
            self.ui.lineEdit_12.setText(res[2]) # DOB
            self.ui.lineEdit_13.setText(res[3]) # Age
            self.ui.lineEdit_14.setText(res[4]) # Address
            self.ui.lineEdit_15.setText(res[5]) # Phone
            self.ui.lineEdit_16.setText(res[6]) # Email

    def populate_fees_receipts(self, reg_no):
        if not hasattr(self.ui, 'lineEdit_46'): return
        if not reg_no: return
        conn = sqlite3.connect('school.db')
        cursor = conn.cursor()
        cursor.execute("SELECT receipt_no FROM fees WHERE reg_no = ?", (reg_no,))
        receipts = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        # Assign a smart autocomplete dropdown to interact exactly like a combobox
        completer = QtWidgets.QCompleter(receipts)
        completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        self.ui.lineEdit_46.setCompleter(completer)
        self.ui.lineEdit_46.clear()

    def edit_student(self):
        reg_no = self.ui.comboBox_3.currentText()
        name = self.ui.lineEdit_10.text()
        gender = self.ui.lineEdit_11.text()
        dob = self.ui.lineEdit_12.text()
        age = self.ui.lineEdit_13.text()
        address = self.ui.lineEdit_14.text()
        phone = self.ui.lineEdit_15.text()
        email = self.ui.lineEdit_16.text()
        
        if not name:
            QMessageBox.warning(self, "Error", "Name is required!")
            return
            
        conn = sqlite3.connect('school.db')
        cursor = conn.cursor()
        cursor.execute('''UPDATE students 
            SET name=?, gender=?, dob=?, age=?, address=?, phone=?, email=? 
            WHERE reg_no=?''', 
            (name, gender, dob, age, address, phone, email, reg_no))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Success", "Student Updated Successfully!")

    def delete_student(self):
        reg_no = self.ui.comboBox_3.currentText()
        if not reg_no: return
        reply = QMessageBox.question(self, 'Confirm', f"Delete Student {reg_no}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            conn = sqlite3.connect('school.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE reg_no=?", (reg_no,))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Success", "Student Deleted Successfully!")
            self.load_student_ids()
            self.ui.lineEdit_10.clear()
            self.ui.lineEdit_11.clear()
            self.ui.lineEdit_12.clear()
            self.ui.lineEdit_13.clear()
            self.ui.lineEdit_14.clear()
            self.ui.lineEdit_15.clear()
            self.ui.lineEdit_16.clear()
        
    def add_marks(self):
        # We assume the user creates student registration manually or types it out. 
        # Future enhancement: populate combo boxes dynamically with actual student Reg Nos
        reg_no = self.ui.comboBox_5.currentText()
        if not reg_no:
            # If combo isn't populated, pull from standard lineEdit fallback if available, or just error
            QMessageBox.warning(self, "Error", "Please provide a valid Registration Number.")
            return
            
        exam = self.ui.lineEdit_19.text()
        lang = self.ui.lineEdit_20.text()
        eng = self.ui.lineEdit_21.text()
        maths = self.ui.lineEdit_22.text()
        sci = self.ui.lineEdit_24.text()
        soc = self.ui.lineEdit_23.text()
        
        conn = sqlite3.connect('school.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO marks 
            (reg_no, exam_name, language, english, science, maths, social_science) 
            VALUES (?, ?, ?, ?, ?, ?, ?)''', 
            (reg_no, exam, lang, eng, sci, maths, soc))
        conn.commit()
        conn.close()
        
        QMessageBox.information(self, "Success", "Marks Details Added Successfully!")
        
        # Clear fields
        self.ui.lineEdit_19.clear()
        self.ui.lineEdit_20.clear()
        self.ui.lineEdit_21.clear()
        self.ui.lineEdit_22.clear()
        self.ui.lineEdit_24.clear()
        self.ui.lineEdit_23.clear()
        
    def get_marks(self):
        reg_no = self.ui.comboBox_6.currentText()
        if not reg_no:
            QMessageBox.warning(self, "Error", "Please select a Registration Number.")
            return
            
        conn = sqlite3.connect('school.db')
        cursor = conn.cursor()
        cursor.execute("SELECT exam_name, language, english, science, maths, social_science FROM marks WHERE reg_no = ?", (reg_no,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            exam_name, lang, eng, sci, maths, soc = result
            # Populate fields
            self.ui.comboBox_7.clear()
            self.ui.comboBox_7.addItem(exam_name)
            self.ui.lineEdit_27.setText(lang)
            self.ui.lineEdit_28.setText(eng)
            self.ui.lineEdit_29.setText(maths)
            self.ui.lineEdit_31.setText(sci)
            self.ui.lineEdit_30.setText(soc)
        else:
            QMessageBox.warning(self, "Error", "No marks found for this student.")
            self.ui.lineEdit_27.clear()
            self.ui.lineEdit_28.clear()
            self.ui.lineEdit_29.clear()
            self.ui.lineEdit_31.clear()
            self.ui.lineEdit_30.clear()
            
    def edit_marks(self):
        reg_no = self.ui.comboBox_6.currentText()
        exam = self.ui.comboBox_7.currentText()
        lang = self.ui.lineEdit_27.text()
        eng = self.ui.lineEdit_28.text()
        maths = self.ui.lineEdit_29.text()
        sci = self.ui.lineEdit_31.text()
        soc = self.ui.lineEdit_30.text()
        
        if not reg_no: return
        conn = sqlite3.connect('school.db')
        cursor = conn.cursor()
        cursor.execute('''UPDATE marks 
            SET language=?, english=?, science=?, maths=?, social_science=?
            WHERE reg_no=? AND exam_name=?''', 
            (lang, eng, sci, maths, soc, reg_no, exam))
        if cursor.rowcount == 0:
            QMessageBox.warning(self, "Error", "Could not update. Verify exactly which Exam is selected!")
        else:
            QMessageBox.information(self, "Success", "Marks Updated Successfully!")
        conn.commit()
        conn.close()

    def delete_marks(self):
        reg_no = self.ui.comboBox_6.currentText()
        if not reg_no: return
        reply = QMessageBox.question(self, 'Confirm', f"Delete Marks for {reg_no}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            conn = sqlite3.connect('school.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM marks WHERE reg_no=?", (reg_no,))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Success", "Marks Deleted Successfully!")
            self.ui.lineEdit_27.clear()
            self.ui.lineEdit_28.clear()
            self.ui.lineEdit_29.clear()
            self.ui.lineEdit_31.clear()
            self.ui.lineEdit_30.clear()
            
    def add_attendance(self):
        reg_no = self.ui.comboBox_8.currentText()
        date = self.ui.lineEdit_25.text()
        morning = self.ui.lineEdit_26.text()
        evening = self.ui.lineEdit_32.text()
        if not reg_no or not date: return
        conn = sqlite3.connect('school.db')
        c = conn.cursor()
        c.execute("INSERT INTO attendance (reg_no, date, morning, evening) VALUES (?, ?, ?, ?)", (reg_no, date, morning, evening))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Success", "Attendance added successfully!")
        self.ui.lineEdit_25.clear()
        self.ui.lineEdit_26.clear()
        self.ui.lineEdit_32.clear()

    def get_attendance(self):
        reg_no = self.ui.comboBox_10.currentText()
        conn = sqlite3.connect('school.db')
        c = conn.cursor()
        c.execute("SELECT date, morning, evening FROM attendance WHERE reg_no=? ORDER BY id DESC LIMIT 1", (reg_no,))
        res = c.fetchone()
        conn.close()
        if res:
            self.ui.comboBox_11.clear()
            self.ui.comboBox_11.addItem(res[0])
            self.ui.lineEdit_37.setText(res[1])
            self.ui.lineEdit_38.setText(res[2])
        else:
            QMessageBox.warning(self, "Error", "No attendance found!")

    def edit_attendance(self):
        reg_no = self.ui.comboBox_10.currentText()
        date = self.ui.comboBox_11.currentText()
        morn = self.ui.lineEdit_37.text()
        eve = self.ui.lineEdit_38.text()
        conn = sqlite3.connect('school.db')
        c = conn.cursor()
        c.execute("UPDATE attendance SET morning=?, evening=? WHERE reg_no=? AND date=?", (morn, eve, reg_no, date))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Success", "Attendance updated!")

    def delete_attendance(self):
        reg_no = self.ui.comboBox_10.currentText()
        date = self.ui.comboBox_11.currentText()
        conn = sqlite3.connect('school.db')
        c = conn.cursor()
        c.execute("DELETE FROM attendance WHERE reg_no=? AND date=?", (reg_no, date))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Success", "Attendance deleted!")
        self.ui.lineEdit_37.clear()
        self.ui.lineEdit_38.clear()

    def add_fees(self):
        receipt = self.ui.lineEdit_41.text()
        reg_no = self.ui.comboBox_12.currentText()
        reason = self.ui.lineEdit_39.text()
        amount = self.ui.lineEdit_40.text()
        date = self.ui.lineEdit_42.text()
        if not receipt: return
        conn = sqlite3.connect('school.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO fees (receipt_no, reg_no, reason, amount, date) VALUES (?, ?, ?, ?, ?)", (receipt, reg_no, reason, amount, date))
            conn.commit()
            QMessageBox.information(self, "Success", "Fees added!")
            
            # Clear UI elements for efficiency
            self.ui.lineEdit_39.clear()
            self.ui.lineEdit_40.clear()
            self.ui.lineEdit_42.clear()
            import random
            self.ui.lineEdit_41.setText(f"RC{random.randint(100000, 999999)}")
            
            # Re-populate the intelligent autocomplete dropdown dynamically
            if hasattr(self.ui, 'comboBox_13') and self.ui.comboBox_13.currentText() == reg_no:
                self.populate_fees_receipts(reg_no)
        except Exception:
            QMessageBox.warning(self, "Error", "Could not add fees. Ensure receipt number is unique.")
        conn.close()
            
    def get_fees(self):
        receipt = self.ui.lineEdit_46.text()
        if not receipt:
            QMessageBox.warning(self, "Error", "Please enter a Receipt Number.")
            return
            
        conn = sqlite3.connect('school.db')
        c = conn.cursor()
        c.execute("SELECT reason, amount, date FROM fees WHERE receipt_no=?", (receipt,))
        res = c.fetchone()
        conn.close()
        if res:
            self.ui.lineEdit_43.setText(res[0])
            self.ui.lineEdit_45.setText(res[1])
            self.ui.lineEdit_44.setText(res[2])
        else:
            QMessageBox.warning(self, "Error", "No fees record found for this receipt!")
            
    def edit_fees(self):
        receipt = self.ui.lineEdit_46.text()
        reason = self.ui.lineEdit_43.text()
        amount = self.ui.lineEdit_45.text()
        date = self.ui.lineEdit_44.text()
        if not receipt: return
        conn = sqlite3.connect('school.db')
        c = conn.cursor()
        c.execute("UPDATE fees SET reason=?, amount=?, date=? WHERE receipt_no=?", (reason, amount, date, receipt))
        if c.rowcount == 0:
            QMessageBox.warning(self, "Error", "Could not update. Verify exactly which Receipt is entered!")
        else:
            QMessageBox.information(self, "Success", "Fees updated!")
        conn.commit()
        conn.close()

    def delete_fees(self):
        receipt = self.ui.lineEdit_46.text()
        if not receipt: return
        reply = QMessageBox.question(self, 'Confirm', f"Delete Fees for {receipt}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            conn = sqlite3.connect('school.db')
            c = conn.cursor()
            c.execute("DELETE FROM fees WHERE receipt_no=?", (receipt,))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Success", "Fees deleted!")
            self.ui.lineEdit_43.clear()
            self.ui.lineEdit_44.clear()
            self.ui.lineEdit_45.clear()
            self.ui.lineEdit_46.clear()
            
    def dummy_success(self):
        QMessageBox.information(self, "Success", "Record successfully stored/updated in database!")
        
    def dummy_print(self):
        QMessageBox.information(self, "Success", "Printing receipt...")
        
    def dummy_cancel(self):
        self.ui.tabWidget.setCurrentIndex(1)
        
    def load_report(self):
        c_text = self.ui.comboBox_15.currentText().lower()
        if not c_text: return
        conn = sqlite3.connect('school.db')
        c = conn.cursor()
        try:
            c.execute(f"SELECT * FROM {c_text}")
            rows = c.fetchall()
            cols = [desc[0] for desc in c.description]
            self.ui.tableWidget.setRowCount(len(rows))
            self.ui.tableWidget.setColumnCount(len(cols))
            self.ui.tableWidget.setHorizontalHeaderLabels(cols)
            for row_idx, row_data in enumerate(rows):
                for col_idx, col_data in enumerate(row_data):
                    self.ui.tableWidget.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(col_data)))
        except sqlite3.OperationalError:
            pass # Invalid table catch
        conn.close()

    def navigate_menu(self, action):
        aname = action.objectName()
        if aname == 'menu11': self.ui.tabWidget.setCurrentIndex(2)
        elif aname == 'menu12': self.ui.tabWidget.setCurrentIndex(3)
        elif aname == 'menu21': self.ui.tabWidget.setCurrentIndex(4)
        elif aname == 'menu31': self.ui.tabWidget.setCurrentIndex(5)
        elif aname == 'menu41': self.ui.tabWidget.setCurrentIndex(6)
        elif aname in ['menu51', 'menu52', 'menu53', 'menu54']:
            self.ui.tabWidget.setCurrentIndex(7)
            table = {"menu51": "Students", "menu52": "Marks", "menu53": "Attendance", "menu54": "Fees"}.get(aname)
            idx = self.ui.comboBox_15.findText(table)
            if idx != -1: self.ui.comboBox_15.setCurrentIndex(idx)
        elif aname == 'menu61': sys.exit()

if __name__ == "__main__":
    setup_database()
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
