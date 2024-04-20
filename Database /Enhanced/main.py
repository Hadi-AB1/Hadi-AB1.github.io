###################
#     IMPORTS     #
###################

# Library for keyboard manipulation
import keyboard
# Libraries for the GUI
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import customtkinter
# Database Library
import sqlite3
# Library used for importing new databases
import os

######################
#   DISPLAY WINDOW   #
######################

# Set up color themes for the program using customtkinter
customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

# Set up program window name and size and tkinter
root = customtkinter.CTk()
root.title('Data Tree Lite')
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
print("Screen width:", screen_width)
print("Screen height:", screen_height)
root.geometry('600x450+550+200')

root.maxsize(650, 500)
#root.geometry('600x450')

# Make it so the window can't be resized
root.resizable(False, False)


###################
#    FUNCTIONS    #
###################


# This function obtains the ID number of a selected item in the treeview
# This makes it so that we can delete and update certain items
def obtainID():
    # NOTE: Using globals within a function is not ideal. Considering switching
    # to an Object-Oriented approach with classes
    global selected_item
    global id_number
    global create_list

    # Every time the user presses the mouse button and releases, the obtainID function will be run
    tree.bind('<ButtonRelease-1>', obtainID)

    # Pulls id number for selected item on the treeview
    selected_item = tree.selection()[0]
    current_item = tree.focus()
    # Creates a dictionary with values of the data
    create_dict = tree.item(current_item)
    # Converts the dict to a list
    create_list = create_dict.get('values')
    # Finds the ID number from the list
    id_number = create_list[6]


# Create delete button function
def delete():
    # Call function to obtain the ID number of the treeview item
    obtainID()

    # Connect to the database
    conn = sqlite3.connect(dbname_combo.get())
    connect = conn.cursor()

    # Confirmation message to make sure the user really wants to delete the selected item
    answer = messagebox.askquestion(title="Are you sure?",
                                    message=f"Are you sure you'd like to delete the data for {create_list[0]}?")
    # If the user answers yes to the messagebox, then delete the specified item
    if answer == 'yes':
        # Delete the specified item from the treeview
        tree.delete(selected_item)
        # Delete the selected item from the database
        connect.execute("DELETE FROM data WHERE oid = " + str(id_number))

    # Commit changes and close connection
    conn.commit()
    conn.close()

    # Call query function to update the treeview and database
    query()


# Add record button function, which commits changes to the database
def submit():
    # Connect to the database
    conn = sqlite3.connect(dbname_combo.get())
    connect = conn.cursor()

    connect.execute("INSERT INTO data VALUES (:f_name, :l_name, :address, :city, :state, :zipcode)",
                    {
                        'f_name': f_name.get(),
                        'l_name': l_name.get(),
                        'address': address.get(),
                        'city': city.get(),
                        'state': state.get(),
                        'zipcode': zipcode.get()
                    })

    # Clear text boxes after the 'Add record' button is pressed
    f_name.delete(0, END)
    l_name.delete(0, END)
    address.delete(0, END)
    city.delete(0, END)
    state.delete(0, END)
    zipcode.delete(0, END)

    # Commit changes and close connection
    conn.commit()
    conn.close()

    # Call the query function to update the database and treeview
    query()


# The query function lets us view data that is currently in the database and add that data into the treeview
def query():
    # Connect to the database
    conn = sqlite3.connect(dbname_combo.get())
    connect = conn.cursor()

    # Query the database
    connect.execute("SELECT *, oid FROM data")
    records = connect.fetchall()
    print(records)

    # Clear the tree every time the update button is pressed
    for item in tree.get_children():
        tree.delete(item)

    # Add the DB records into the treeview
    for record in records:
        tree.insert("", 'end', text='', values=record)
        print(record)

    # Close the connection to the database to push changes
    conn.commit()
    conn.close()


# Update function allows us to update things in the database
def update():
    # Connect to the database
    conn = sqlite3.connect(dbname_combo.get())
    connect = conn.cursor()

    # Obtain the ID so that we know which piece of data we're changing
    obtainID()

    # Some SQL code to update the data table
    connect.execute("""UPDATE data SET
                   first_name = :first,
                   last_name = :last,
                   address = :address,
                   city = :city,
                   state = :state,
                   zipcode = :zipcode
                   WHERE oid = """ + str(id_number),
                    {
                        'first': f_name.get(),
                        'last': l_name.get(),
                        'address': address.get(),
                        'city': city.get(),
                        'state': state.get(),
                        'zipcode': zipcode.get(),
                    })

    # Close the connection to the database to push changes
    conn.commit()
    conn.close()

    # Call the query function to pull the most recent data from the database and update the treeview data
    query()


# This allows for the text boxes to autofill when an option in treeview is selected
def fill_text(event):
    # Call the obtainID function first so that we know which piece of data we're changing
    obtainID()

    # Set up new variables from the data lists we created in the obtainID function
    # which is from the selected treeview data
    new_f_name = create_list[0]
    new_l_name = create_list[1]
    new_address = create_list[2]
    new_city = create_list[3]
    new_state = create_list[4]
    new_zip = create_list[5]

    # This clears the data inside the text boxes
    # I think I could make a `for` loop for this instead to adhere to coding best practices
    f_name.delete(0, END)
    l_name.delete(0, END)
    address.delete(0, END)
    city.delete(0, END)
    state.delete(0, END)
    zipcode.delete(0, END)

    # Then this enters the new data in those text boxes
    f_name.insert(0, new_f_name)
    l_name.insert(0, new_l_name)
    address.insert(0, new_address)
    city.insert(0, new_city)
    state.insert(0, new_state)
    zipcode.insert(0, new_zip)


# This updates the database combobox list
def update_dblist():
    # Stores the available databases in a list
    databases = []
    # Goes through the databases available in the database folder
    for root_val, dirs, files in os.walk(r"databases"):
        # Finds each file that ends in a .db
        print(files)
        for file in files:

            if file.endswith(".db"):
                # Adds each database to the databases list
                databases.append(os.path.join(file))
    # Returns the databases list to be used in the combobox
    return databases


# This function is called whenever the combobox is clicked on
# This will allow the user to switch back and forth between databases
def selected_combo(event):
    print(f"{dbname_combo.get()} has been selected in the combobox!")
    connection = sqlite3.connect(dbname_combo.get())
    cursor = connection.execute('select * from data')
    names = list(map(lambda x: x[0], cursor.description))
    print(names)


####################
#    TEXT BOXES    #
####################

# Create Text Boxes for the user to enter data
f_name = customtkinter.CTkEntry(root, width=150)
f_name.grid(row=1, column=1, padx=20, sticky="we")
l_name = customtkinter.CTkEntry(root, width=150)
l_name.grid(row=2, column=1, padx=20, sticky="we")
address = customtkinter.CTkEntry(root, width=150)
address.grid(row=3, column=1, padx=20, sticky="we")
city = customtkinter.CTkEntry(root, width=150)
city.grid(row=4, column=1, padx=20, sticky="we")
state = customtkinter.CTkEntry(root, width=150)
state.grid(row=5, column=1, padx=20, sticky="we")
zipcode = customtkinter.CTkEntry(root, width=150)
zipcode.grid(row=6, column=1, padx=20, sticky="we")

####################
#      LABELS      #
####################

# Labels to show which database the user is in
db_label = customtkinter.CTkLabel(root, text="Database:")
db_label.grid(row=0, column=0)

# Combobox for databases
dbname_combo = customtkinter.CTkComboBox(root, values=update_dblist(), command=selected_combo)
dbname_combo.grid(row=0, column=1, padx=20)
#dbname_combo.bind('<<ComboboxSelected>>', lambda _: selected_combo())


# Create labels for the text boxes where the user inputs new data
f_name_label = customtkinter.CTkLabel(root, text="First Name")
f_name_label.grid(row=1, column=0)
l_name_label = customtkinter.CTkLabel(root, text="Last Name")
l_name_label.grid(row=2, column=0)
address_label = customtkinter.CTkLabel(root, text="Address")
address_label.grid(row=3, column=0)
city_label = customtkinter.CTkLabel(root, text="City")
city_label.grid(row=4, column=0)
state_label = customtkinter.CTkLabel(root, text="State")
state_label.grid(row=5, column=0)
zipcode_label = customtkinter.CTkLabel(root, text="Zipcode")
zipcode_label.grid(row=6, column=0)

####################
#     TREEVIEW     #
####################

# This is for styling the treeview
style = ttk.Style(root)
# set ttk theme to "clam" which support the field background option
style.theme_use("clam")
# This is for the background & where data is
style.configure("Treeview", background="#A49393",
                fieldbackground="#A49393", foreground="#28282B")
# This is for the heading
style.configure("Treeview.Heading", background="#EED6D3", foreground="#67595E")

# Create the treeview to hold the data
tree = ttk.Treeview(root, selectmode='browse')
tree.grid(row=7, column=0, columnspan=5, padx=15, pady=15, sticky='nsew')

# Set up the columns of the treeview data
tree['columns'] = ('first_name', 'last_name', 'address', 'city', 'state', 'zip')
tree.column('#0', width=0)
tree.column('first_name', width=100)
tree.column('first_name', width=100)
tree.column('last_name', width=100)
tree.column('address', width=200)
tree.column('city', width=100)
tree.column('state', width=100)
tree.column('zip', width=100)
#tree.column('id', width=50)

# Headings for the treeview data
tree.heading('first_name', text='First Name')
tree.heading('last_name', text='Last Name')
tree.heading('address', text='Address')
tree.heading('city', text='City')
tree.heading('state', text='State')
tree.heading('zip', text='Zip Code')
#tree.heading('id', text='ID')

###################
#     BUTTONS     #
###################

# Create a submit button
submit_btn = customtkinter.CTkButton(root, text="Add Record", command=submit)
submit_btn.grid(row=1, column=2, columnspan=1, rowspan=2, pady=10, padx=0, ipadx=10, ipady=10)

# Create a delete button
delete_btn = customtkinter.CTkButton(root, text="Delete Record", command=delete)  # delete
delete_btn.grid(row=3, column=2, columnspan=1, rowspan=2, pady=10, padx=0, ipadx=10, ipady=10)

# Whenever the user clicks on a treeview option a second time, the data will auto-populate in the text boxes
tree.bind("<Button>", fill_text)

# Create an update button
update_btn = customtkinter.CTkButton(root, text="Update Record", command=update)
update_btn.grid(row=5, column=2, columnspan=1, rowspan=2, pady=10, padx=0, ipadx=10, ipady=10)

###################
#      OTHER      #
###################

# This opens the database automatically when the user opens the program
query()

# Count the enter key as a mouse click
keyboard.on_press_key("enter", lambda _: query())

# This detects delete keypress and connects it to delete() function
keyboard.on_press_key("del", lambda _: delete())

root.mainloop()




