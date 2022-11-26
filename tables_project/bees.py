#connection
import re
import sqlalchemy as s
from connect import engine
from connect import connection
from connect import metadata

import tables_project.project as project
import tables_project.scope as scope

import algos


# create table object, called selected table, st
st = s.Table("bees", metadata, autoload=True, autoload_with=engine) #bees


# the functions that are imported into the display table and view table, adapt/change this when updating a table.
#________________________________________________________________________________________________________________________
def select_table():
    # the query object
    query = s.select([st.columns.bee_no,st.columns.first_name ,st.columns.last_name])
    # execute query
    select_result_proxy = connection.execute(query)
    return select_result_proxy

def update_table():
    bee_no = int(input("select scope id: "))
    first_name = input("Insert first name: ")
    last_name = input("Insert last name: ")
    email = input("Insert email: ")
    phone_no = input("Insert phone_no: ")
    gender = algos.gender_type()
    hire_date = algos.date_setup("hire date")
    birth_date = algos.date_setup("birth date")

    update = s.update(st).values(first_name= first_name,last_name=last_name,email=email,phone_no=phone_no,gender=gender,hire_date=hire_date,birth_date=birth_date).where(st.columns.bee_no == bee_no)
    proxy = connection.execute(update)
    ans = "selected id updated"
    return ans

def delete_table():
    bee_no = int(input("Select scope id: "))
    query = s.delete(st).where(st.columns.bee_no == bee_no)
    proxy = connection.execute(query)
    ans = "selected id deleted"
    return ans

def insert_table():
    first_name = input("Insert first name: ")
    last_name = input("Insert last name: ")
    email = input("Insert email: ")
    phone_no = input("Insert phone_no: ")
    gender = algos.gender_type()
    hire_date = algos.date_setup("hire date")
    birth_date = algos.date_setup("birth date")

    insert = s.insert(st).values(first_name= first_name,last_name=last_name,email=email,phone_no=phone_no,gender=gender,hire_date=hire_date,birth_date=birth_date)
    proxy = connection.execute(insert)
    ans = "selected id updated"
   

# display functions
#________________________________________________________________________________________________________________________

def display_table(table_name):
    """View , select, update and insert the table:
    To adopt this function to suit other table; Change all occurencies for 
    1) selected_table.columns.[column_a]
    2) selected_table.columns.[column_b]

    with the new column names

    To allow the user to insert into more columns (more than one),modify the insert section.


    Args:
        table_name (str): the name of the table

    Returns:
        _type_: the id of the entry selected

    """
    try_again = True
    while try_again:

        select = select_table()

        # STORING RESULTS PROXY IN A DICT
        #_______________________________________________________________________________________
       
        # record the output in a dict ( key and value); id and the name
        items = [result for result in select]
        items_dict = {item[0]:(item[1] + " " + item[2]) for item in items}
    

        # insert option to update if input is missing
        changes = {"u":"update","d":"delete","i":"insert" }


        # DISPLAY ENTRIES IN DATABASE
        #_______________________________________________________________________________________
        print()
        print(F"{table_name}")
        print("***************************************************")
        for key, value in items_dict.items():
            print(f"{key}:{str.upper(value)}")
        print("___________________________________________________")

        # DISPLAY CREATE, DELETE AND INSERT OPTIONS
        #_______________________________________________________________________________________
        for key, value in changes.items():
            print(f"<> ({key}):{value} <> ", end="")
    
        print()
        print("***************************************************")

        user_selection = input("select: ")
    
        # SELECT ENTRY IN DATABASE LOGIC
        #_______________________________________________________________________________________
        if user_selection.isdigit():
            user_selection = int(user_selection)
            if user_selection in items_dict.keys():
                try_again = False
            else:
                print("Integer selected out of range")
                try_again = True

        # UPDATE , DELETE AND INSERT LOGIC
        #_______________________________________________________________________________________
        else:
            if user_selection in changes.keys():
                #UPDATE
                if user_selection == str.lower("u"):
                    print()
                    print("_____________________________")
                    print("Updating a database entry")
                    print("_____________________________")
                    update_table()
                    print("_____________________________")
                    print()
                    try_again = True

            
                #DELETE

                elif user_selection == "d":
                    # delete the entries
                    print()
                    print("_____________________________")
                    print("Deleting a database entry")
                    print("_____________________________")
                    delete_table()
                    print("_____________________________")
                    print()
                    try_again = True
                

                # INSERT
                elif user_selection == "i":
                    # insert new entries
                    print()
                    print("_____________________________")
                    insert_table()
                    print("_____________________________")
                    try_again = True

                else:
                    print("Input selected is out of range")

    # RETURN ID(PRIMARY KEY) OF SELECTED OPTION
    #_______________________________________________________________________________________   
    return user_selection 

def show_table(table_name):
    try_again = True
    while try_again:

        select = select_table()
 
        # STORING RESULTS PROXY IN A DICT
        #_______________________________________________________________________________________
       
        # record the output in a dict ( key and value); id and the name
        output_dict = {}
        for result in select:
            #convert tuple output to one item
            column_a = result[0]
            column_b= result[1]

            # table_id (primary key) recorded as the key, followed by identifier name

            output_dict[column_a]=str.upper(column_b)

        # DISPLAY ENTRIES IN DATABASE
        #_______________________________________________________________________________________
        print()
        print(F"{table_name}")
        print("***************************************************")
        for key, value in output_dict.items():
            print(f"{key}:{value}")
        print("___________________________________________________")

        # SELECT ENTRY IN DATABASE LOGIC
        #_______________________________________________________________________________________
        user_selection = input("select: ")
        if user_selection.isdigit():
            user_selection = int(user_selection)
            if user_selection in output_dict.keys():
                try_again = False
            else:
                print("Integer selected out of range")
                try_again = True
        else:
            print("Wrong input")

    return user_selection



# select functions
#________________________________________________________________________________________________________________________

def show_bee_name(bee_no):
    # the query object
    query = s.select([st.columns.first_name, st.columns.last_name]).where(st.columns.bee_no==bee_no)
    # execute query
    select_result_proxy = connection.execute(query)
    full_name = [result for result in select_result_proxy]
    bee_name = str(full_name[0][0]) + " " +  str(full_name[0][1])
    return bee_name



if __name__ == "__main__":
    display_table("bees")
    #bee_no = 14
    #show_bee_name(bee_no)

