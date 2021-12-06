#https://realpython.com/python-mysql/
from getpass import getpass
from mysql.connector import connect,Error

try:
	with connect(host="localhost", user=input("Enter username: "), password=getpass("Enter password: "),database="vaccine_certificates") as connection:
		create_patients="""
		CREATE TABLE patients(
		patient_id INT AUTO_INCREMENT PRIMARY KEY,
		first_name VARCHAR(100),
		last_name VARCHAR(100),
		dob DATE
		)
		"""
		create_vaclist="""
		CREATE TABLE vaccine_list(
		vaccine_id INT AUTO_INCREMENT PRIMARY KEY,
		name VARCHAR(100),
		optional_brand VARCHAR(100) DEFAULT NULL
		)
		"""
		create_vac_record="""
		CREATE TABLE vaccine_record(
		vac_num INT AUTO_INCREMENT PRIMARY KEY,
		patient_id INT,
		vaccine_id INT,
		FOREIGN KEY(patient_id) REFERENCES patients(patient_id),
		FOREIGN KEY(vaccine_id) REFERENCES vaccine_list(vaccine_id),
		date_of_administration DATE
		)
		"""
		with connection.cursor() as cursor:
			cursor.execute("DROP TABLE IF EXISTS patients, vaccine_list, vaccine_record")
			cursor.execute(create_patients)
			cursor.execute(create_vaclist)
			cursor.execute(create_vac_record)
			connection.commit()
except Error as e:
	print(e)