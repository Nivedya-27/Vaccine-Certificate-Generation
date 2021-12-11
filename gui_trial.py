import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import simpledialog
from mysql.connector import connect,Error
from tkcalendar import DateEntry
from datetime import date,datetime
import pandas as pd
import pdfkit

def login():
	global connection
	global username
	global password
	username=username.get()
	password=password.get()
	try:
		connection=connect(host="localhost", user=username, password=password,database="vaccine_certificates")

	except Error as e:
		print(e)

def view_table(table_name):
	global connection
	global root
	view_patients="""SELECT * FROM patients"""
	view_vaclist="""SELECT * FROM vaccine_list"""
	view_vacrecord="""SELECT * FROM vaccine_record"""
	cols_patients=('patient id','first name','last name','date of birth')
	cols_vacs=('vaccine id','name','optional brand')
	cols_rec=('vaccine number','patient id','vaccine id','date of administration')
	with connection.cursor() as cursor:
		if table_name=='patients':
			cols=cols_patients
			cursor.execute(view_patients)
		elif table_name=='vaccines':
			cols=cols_vacs
			cursor.execute(view_vaclist)
		else:
			cols=cols_rec
			cursor.execute(view_vacrecord)
		result=cursor.fetchall()
		connection.commit()
	new_window=tk.Toplevel(root)
	new_window.title(table_name)
	new_window.geometry("300x300")
	listBox=Treeview(new_window,columns=cols,show='headings')
	scrollbar = Scrollbar(new_window,orient ="vertical",command = listBox.yview)
	scrollbar.grid(column=1, row=0, sticky='NS')
	listBox.configure(xscrollcommand = scrollbar.set)
	for col in cols:
		listBox.heading(col, text=col)
		listBox.grid(row=1, column=0, columnspan=2)
	for i, tuple_val in enumerate(result, start=1):
		if table_name=='patients':
			listBox.insert("","end",values=(tuple_val[0],tuple_val[1],tuple_val[2],(tuple_val[3]).strftime("%d/%m/%Y")))
		elif table_name=='vaccines':
			listBox.insert("","end",values=tuple_val)
		else:
			listBox.insert("", "end", values=(tuple_val[0], tuple_val[1], tuple_val[2], (tuple_val[3].strftime("%d/%m/%Y"))))

def enter_patient():
	global root
	global firstname
	global lastname
	global dob
	new_window=tk.Toplevel(root)
	new_window.title("Enter new patient")
	new_window.geometry("300x300")
	l_firstname=tk.Label(new_window,text="First Name")
	l_firstname.grid(row=1,column=0,padx=5)
	firstname=tk.StringVar()
	firstname.set('')
	e_firstname=tk.Entry(new_window,textvariable=firstname,width=10)
	e_firstname.grid(row=1,column=1)
	l_lastname=tk.Label(new_window,text="Last Name")
	l_lastname.grid(row=2,column=0,padx=5)
	lastname=tk.StringVar()
	lastname.set('')
	e_lastname=tk.Entry(new_window,textvariable=lastname,width=10)
	e_lastname.grid(row=2,column=1)
	l_dob=tk.Label(new_window,text="Date of Birth")
	l_dob.grid(row=3,column=0)
	sel=tk.StringVar()
	cal=DateEntry(new_window,select_mode='day',textvariable=sel)
	cal.grid(row=4,column=1,padx=20)
	dob=datetime.strptime(sel.get(),'%m/%d/%y')
	dob=dob.strftime("%Y-%m-%d")
	b_enter=tk.Button(new_window,text="Submit",width=10,command=lambda:submit_patient_details())
	b_enter.grid(row=5,column=1)

def submit_patient_details():
	global firstname
	global lastname
	global dob
	global connection
	insert_patient="""INSERT INTO patients (first_name,last_name,dob) VALUES(%s,%s,%s)"""
	with connection.cursor() as cursor:
		cursor.executemany(insert_patient,[(firstname.get(),lastname.get(),dob)])
		connection.commit()

def enter_record():
	global vaccine_id
	global patient_id
	global date_of_administration
	global root
	new_window=tk.Toplevel(root)
	new_window.title("Enter new vaccine record")
	new_window.geometry("300x300")
	l_vid=tk.Label(new_window,text="Vaccine ID")
	l_vid.grid(row=1,column=0)
	vaccine_id=tk.StringVar()
	vaccine_id.set('')
	e_vid=tk.Entry(new_window,textvariable=vaccine_id,width=10)
	e_vid.grid(row=1,column=1)
	l_pid=tk.Label(new_window,text="Patient ID")
	l_pid.grid(row=2,column=0)
	patient_id=tk.StringVar()
	patient_id.set('')
	e_pid=tk.Entry(new_window,textvariable=patient_id,width=10)
	e_pid.grid(row=2,column=1)
	l_doa=tk.Label(new_window,text="Date of Administration")
	l_doa.grid(row=3,column=0)
	sel=tk.StringVar()
	cal=DateEntry(new_window,select_mode='day',textvariable=sel)
	cal.grid(row=4,column=1,padx=20)
	date_of_administration=datetime.strptime(sel.get(),'%m/%d/%y')
	date_of_administration=date_of_administration.strftime("%Y-%m-%d")
	b_enter=tk.Button(new_window,text="Submit",width=10,command=lambda:submit_vaccine_record())
	b_enter.grid(row=5,column=1)

def submit_vaccine_record():
	global vaccine_id
	global patient_id
	global date_of_administration
	global connection
	if(not (len(vaccine_id.get()))):
		tk.messagebox.showwarning("Empty vaccine ID","Enter vaccine ID")
	if(not (len(patient_id.get()))):
		tk.messagebox.showwarning("Empty Patient ID","Enter patient ID")
	insert_record="""INSERT INTO vaccine_record (patient_id,vaccine_id,date_of_administration) VALUES(%s,%s,%s)"""
	with connection.cursor() as cursor:
		cursor.executemany(insert_record,[(int(patient_id.get()),int(vaccine_id.get()),date_of_administration)])
		connection.commit()

def generate_certif():
	global root
	global pid
	new_window=tk.Toplevel(root)
	new_window.title("Generate vaccine certificate")
	new_window.geometry("200x200")
	l_pid=tk.Label(new_window,text="Enter patient ID")
	l_pid.grid(row=1,column=0)
	pid=tk.StringVar()
	pid.set('')
	e_pid=tk.Entry(new_window,textvariable=pid,width=10)
	e_pid.grid(row=1,column=1)
	b_make_certif=tk.Button(new_window,text="Generate",width=10,command=lambda:make_certif())
	b_make_certif.grid(row=2,column=0)

def make_certif():
	global connection
	global pid
	if(not len(pid.get())):
		tk.messagebox.showwarning("Empty Patient ID","Enter Patient ID")
	patient_id=int(pid.get())
	select_records="""
	SELECT vaccine_list.name,vaccine_list.optional_brand,date_of_administration 
	FROM vaccine_record join vaccine_list 
	ON vaccine_record.vaccine_id=vaccine_list.vaccine_id WHERE patient_id={patient_id} ORDER BY date_of_administration ASC
	""".format(patient_id=patient_id)
	select_details="""
	SELECT first_name,last_name,dob FROM patients WHERE patient_id={patient_id}""".format(patient_id=patient_id)
	with connection.cursor() as cursor:
		cursor.execute(select_records)
		result1=cursor.fetchall()
		df=pd.read_sql(select_records,connection)
		df.rename(columns={'name': 'Vaccine', 'optional_brand': 'Brand if applicable', 'date_of_administration': 'date of administration'},
			inplace=True)
		cursor.execute(select_details)
		result2=cursor.fetchall()
		first_name=(result2[0])[0]
		last_name=(result2[0])[1]
		dob=(result2[0])[2].strftime("%d/%m/%Y")
		HTML_TEMPLATE1 = """\
		<html>
		<head>
		<style>
		h2 {{
		text-align: center;
		font-family: Arial, Helvetica, sans-serif;
		}}
		p{{
		text-align:center;
		}}
		#left {{text-align: left}}
		#right {{text-align: right}}
		table {{
		margin-left: auto;
		margin-right: auto;
		}}
		table, th, td {{
		border: 1px solid black;
		border-collapse: collapse;
		}}
		th, td {{
		padding: 5px;
		text-align: center;
		font-family: Helvetica, Arial, sans-serif;
		font-size: 90%;
		}}
		table tbody tr:hover {{
		background-color: #dddddd;
		}}
		.wide {{
		width: 90%; 
		}}
		</style>
		<h2>
		IMMUNIZATION CERTIFICATE
		</h2>
		</head>
		<body>
		<p>
		This is to certify that {first_name} {last_name}, date of birth {dob}, hospital id {hospital_id}
		has received the following vaccinations as mentioned below.
		</p>
		""".format(first_name=first_name,last_name=last_name,dob=dob,hospital_id=patient_id)
		HTML_TEMPLATE2 = '''
		<p id="left">Date: </p>
		<pre id="right">Dr:              </pre>
		</body>
		</html>
		'''
		html_name=str(patient_id)+'.html'
		pdf_name=str(patient_id)+'.pdf'
		a=df.to_html()
		with open(html_name, 'w') as f:
			f.write(HTML_TEMPLATE1 + a + HTML_TEMPLATE2)
		path_wkhtmltopdf=r'D:\wkhtml\wkhtmltopdf\bin\wkhtmltopdf.exe'
		config=pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
		pdfkit.from_file(html_name,pdf_name,configuration=config)
		connection.commit()

root=tk.Tk()
root.geometry("600x420")
root.title("Vaccine Records Database")

l1=tk.Label(root,text="User")
l1.grid(row=1, column=1,padx=5)
username=tk.StringVar()
username.set('')
e1=tk.Entry(root,textvariable=username,width=10)
e1.grid(row=1,column=2)

l2=tk.Label(root,text="Password")
l2.grid(row=1,column=3,padx=5)
password=tk.StringVar()
password.set('')
e2=tk.Entry(root,textvariable=password,show='*',width=10)
e2.grid(row=1,column=4)

b1=tk.Button(root,text="Connect",width=10,command=lambda:login())
b1.grid(row=1,column=5)

b_view_patients=tk.Button(root,text="View patients",width=10,command=lambda:view_table('patients'))
b_view_patients.grid(row=2,column=1)

b_view_vaccines=tk.Button(root,text="View vaccines",width=10,command=lambda:view_table('vaccines'))
b_view_vaccines.grid(row=2,column=2)

b_view_records=tk.Button(root,text="View records",width=10,command=lambda:view_table('records'))
b_view_records.grid(row=2,column=4)

b_enter_patient=tk.Button(root,text="Enter new patient",width=15,command=lambda:enter_patient())
b_enter_patient.grid(row=3,column=1)

b_enter_record=tk.Button(root,text="Enter vaccine record",width=15,command=lambda:enter_record())
b_enter_record.grid(row=3,column=3)

b_gen_certif=tk.Button(root,text="Generate vaccine certificate",width=25,command=lambda:generate_certif())
b_gen_certif.grid(row=4,column=1)

closeButton = tk.Button(root, text="Close", width=15, command=exit).grid(row=5, column=1)
root.mainloop()
