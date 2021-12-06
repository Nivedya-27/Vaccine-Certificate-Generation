#https://realpython.com/python-mysql/
from getpass import getpass
from mysql.connector import connect,Error
import csv

try:
	with connect(host="localhost", user=input("Enter username: "), password=getpass("Enter password: "),database="vaccine_certificates") as connection:
		insert_vaclist="""
		INSERT INTO vaccine_list
		(name,optional_brand)
		VALUES(%s,%s)
		"""
		values=[]
		with connection.cursor() as cursor:
			with open("template.csv","r") as file:
				csvreader=csv.reader(file)
				for row in csvreader:
					name=row[0]
					brandname=row[1]
					values.append((name,brandname))
			cursor.executemany(insert_vaclist,values)
			connection.commit()
except Error as e:
	print(e)