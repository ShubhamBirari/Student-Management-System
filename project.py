from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
from tabulate import tabulate
from connectDB import *
import pygame.mixer
import time
import re
import time
import socket
import requests


def display_temp():

	try :
		socket.create_connection(('www.google.com',80))
		res = requests.get("https://ipinfo.io/")
		data=res.json()
		city = data['city']
		api_address = "http://api.openweathermap.org/data/2.5/weather?units=metric&q="+city+"&appid=10c91e2ac136e2a770ec750eefafd161"
		res1 = requests.get(api_address)
		wdata = requests.get(api_address).json()
		temp = wdata['main']['temp']
		temp2 = wdata['name']
		msg="You are in "+str(temp2)+"\n Temperature is "+str(temp)+" degree Celcius"
	except OSError:
		msg="Check your internet connection"

	return msg

# Root user interface
root = Tk()
root.geometry("400x350+450+200")
root.title("Student Managament System")
root.withdraw()

temp_window = Toplevel(root)
temp_window.geometry("400x350+450+200")
temp_window.title("Student Managament System")

msg="Getting info"

lbl_welcome = Label(temp_window,text="Welcome", font=("ariel", 24, 'bold'))
lbl_temp = Label(temp_window,text=msg, height=2,font=("ariel",15))
lbl_welcome.pack(pady=20)
lbl_temp.pack(pady=20)


def a1():
	lbl_temp.configure(text=msg+".",font=("ariel", 15))
	return

def a2():
	lbl_temp.configure(text=msg+"..",font=("ariel", 15))
	return

def a3():
	lbl_temp.configure(text=msg+"...",font=("ariel", 15))
	return

def sound():
	pygame.mixer.init()
	pygame.mixer.music.load("system-fault.mp3")
	time.sleep(1)
	pygame.mixer.music.play(1)
	time.sleep(1)
	pygame.mixer.music.stop()

def function():
	c = display_temp()
	lbl_temp.configure(text=c, font=("ariel", 15))
	if c=="Check your internet connection" :
		sound()

temp_window.after(1000,a1)
temp_window.after(2000,a2)
temp_window.after(3000,a3)
temp_window.after(3001,function)

temp_window.after(6500, lambda: temp_window.destroy())
root.after(6500,lambda:root.deiconify())

def f1():
	add_st.deiconify()
	root.withdraw()

btn_add = Button(root, text="Add Student", height=2,width=20, command=f1)

#	Navigate to another window when button is clicked
def f2():	
	connect_db()
	view_st.deiconify()
	root.withdraw()
	sql = "select * from student order by rno"
	cursor.execute(sql)
	data = cursor.fetchall()
	info =""
	list_of_lists = [list(elem) for elem in data]
	view_stdata.insert(INSERT,tabulate(data, headers=['Roll No.', 'Name'], tablefmt='orgtbl'))
btn_view = Button(root, text="View Student Details", height=2, width=20, command=f2)

def f3():
	update_st.deiconify()
	root.withdraw()
btn_update = Button(root, text="Update Student", height=2, width=20, command=f3)

def f4():
	delete_st.deiconify()
	root.withdraw()
btn_delete = Button(root, text="Delete Student", height=2, width=20, command=f4)

btn_add.pack(pady=20)
btn_view.pack(pady=20)
btn_update.pack(pady=20)
btn_delete.pack(pady=20)




# Add Student Interface

add_st = Toplevel(root)
add_st.geometry("400x300+450+200")
add_st.title("Add Student")
add_st.withdraw()

lbl_addrno = Label(add_st, text="Enter Roll Number")
ent_addrno = Entry(add_st, bd=2)
lbl_addname = Label(add_st, text="Enter Name")
ent_addname = Entry(add_st, bd=2)

def f5():
	connect_db()
	# Validate roll number
	try :
		num = ent_addrno.get()
		if len(num)==0:
			messagebox.showerror("Error","Enter roll number")
			ent_addrno.delete(0,END)
			ent_addrno.focus()
			return
		rno = int(num)

		if rno<=0:
			messagebox.showerror("Error","Enter positive roll number only!")
			ent_addrno.delete(0,END)
			ent_addrno.focus()
			return
	except ValueError as e:
		messagebox.showerror("Error","Invalid roll number")
		ent_addrno.delete(0,END)
		ent_addrno.focus()
		return

	name = ent_addname.get()

	# Validate Name
	if len(name)==0:
		messagebox.showerror("Error","Enter name")
		ent_addname.delete(0,END)
		ent_addname.focus()
		return
	
	if all(x.isalpha() or x.isspace() for x in name):
		pass
	else:
		messagebox.showerror("Error","Invalid name")
		ent_addname.delete(0,END)
		ent_addname.focus()
		return
	sql = "insert into student values(%d,'%s')"
	args = (rno, name)
	cursor.execute(sql%args)
	con.commit()
	print(cursor.rowcount,"rows inserted\n")
	messagebox.showinfo("Result",str(cursor.rowcount)+" rows inserted")

	ent_addrno.delete(0,END)
	ent_addname.delete(0,END)
	ent_addrno.focus()

btn_addSave = Button(add_st, text="Save", width=10, command=f5)

def f6():
	root.deiconify()
	add_st.withdraw()

btn_addBack = Button(add_st, text="Back", width=10, command=f6)

lbl_addrno.pack(pady=10)
ent_addrno.pack(pady=10)
lbl_addname.pack(pady=10)
ent_addname.pack(pady=10)
btn_addSave.pack(pady=10)
btn_addBack.pack(pady=10)

add_st.protocol("WM_DELETE_WINDOW", f6)




# View Student Details Interface

view_st = Toplevel(root)
view_st.geometry("400x300+450+200")
view_st.title("View Student Details")
view_st.withdraw()

view_stdata = scrolledtext.ScrolledText(view_st, width=35, height=10)

def f7():
	root.deiconify()
	view_st.withdraw()
	view_stdata.delete('1.0', END)
btn_viewBack = Button(view_st, text="Back", width=10, command=f7)

view_stdata.pack(pady=10)
btn_viewBack.pack(pady=10)

view_st.protocol("WM_DELETE_WINDOW",f7)





# Update Student Interface

update_st = Toplevel(root)
update_st.geometry("400x300+450+200")
update_st.title("Update Student")
update_st.withdraw()

lbl_updaterno = Label(update_st, text="Enter roll number to be updated")
ent_updaterno = Entry(update_st, bd=2)
lbl_updatename = Label(update_st, text="Enter new name")
ent_updatename = Entry(update_st, bd=2)

def f8():
	connect_db()
	# Validate roll number
	try :
		num = ent_updaterno.get()
		if len(num)==0:
			messagebox.showerror("Error","Enter roll number")
			ent_updaterno.delete(0,END)
			ent_updaterno.focus()
			return

		rno = int(num)

		if rno<=0:
			messagebox.showerror("Error","Enter positive roll number only!")
			ent_updaterno.delete(0,END)
			ent_updaterno.focus()
			return
	except ValueError as e:
		messagebox.showerror("Error","Invalid roll number")
		ent_updaterno.delete(0,END)
		ent_updaterno.focus()
		return

	name = ent_updatename.get()
	# Validate Name
	if len(name)==0:
		messagebox.showerror("Error","Enter name")
		ent_updatename.delete(0,END)
		ent_updatename.focus()
		return
	if (all(x.isalpha() or x.isspace() for x in name) and len(name)>0):
		pass
	else:
		messagebox.showerror("Error","Invalid name")
		ent_updatename.delete(0,END)
		ent_updatename.focus()
		return
	
	sql="update student set name='%s' where rno=%d"
	args = (name, rno)
	cursor.execute(sql%args)
	con.commit()
	print("Update successful")
	ent_updaterno.delete(0,END)
	ent_updatename.delete(0,END)
	ent_updaterno.focus()
	messagebox.showinfo("Result",str(cursor.rowcount)+" rows updated")

btn_updateSave = Button(update_st, text="Update", width=10, command=f8)

def f9():
	root.deiconify()
	update_st.withdraw()
btn_updateBack = Button(update_st, text="Back", width=10, command=f9)

lbl_updaterno.pack(pady=10)
ent_updaterno.pack(pady=10)
lbl_updatename.pack(pady=10)
ent_updatename.pack(pady=10)
btn_updateSave.pack(pady=10)
btn_updateBack.pack(pady=10)

update_st.protocol("WM_DELETE_WINDOW",f9)





# Delete Student Interface

delete_st = Toplevel(root)
delete_st.geometry("400x300+450+200")
delete_st.title("Delete Student")
delete_st.withdraw()

lbl_deleterno = Label(delete_st, text="Enter the roll number to be deleted")
ent_deleterno = Entry(delete_st, bd=2)

def f10():
	connect_db()
	ans = messagebox.askyesno("Exit","Sure you want to delete?")
	if ans:
		try :
			num = ent_deleterno.get()
			if len(num)==0:
				messagebox.showerror("Error","Enter roll number")
				ent_deleterno.delete(0,END)
				ent_deleterno.focus()
				return

			rno = int(num)

			if rno<=0:
				messagebox.showerror("Error","Enter positive roll number only!")
				ent_deleterno.delete(0,END)
				ent_deleterno.focus()
				return
		except ValueError as e:
			messagebox.showerror("Error","Invalid roll number")
			ent_deleterno.delete(0,END)
			ent_deleterno.focus()
			return
		
		sql = "delete from student where rno=%d"
		agrs = (rno)
		cursor.execute(sql%agrs)
		con.commit()
		print("Delete successful")
		ent_deleterno.delete(0, END)
		ent_deleterno.focus()
		messagebox.showinfo("Result", str(cursor.rowcount)+" row deleted")

btn_deleteSave = Button(delete_st, text="Delete", width=10, command=f10)

def f11():
	root.deiconify()
	delete_st.withdraw()
btn_deleteBack = Button(delete_st, text="Back", width=10, command=f11)

lbl_deleterno.pack(pady=10)
ent_deleterno.pack(pady=10)
btn_deleteSave.pack(pady=10)
btn_deleteBack.pack(pady=10)

delete_st.protocol("WM_DELETE_WINDOW", f11)
 
def f12():
	ans = messagebox.askyesno("Exit","Do you really want to exit?")
	if ans:
		disconn_db()
		import sys
		sys.exit()

root.protocol("WM_DELETE_WINDOW",f12)
root.mainloop()