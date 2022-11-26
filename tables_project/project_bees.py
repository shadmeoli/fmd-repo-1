#connection

import sqlalchemy as s
from connect import engine
from connect import connection
from connect import metadata

import tables_project.project as project
import tables_project.bees as bees
import tables_project.project_fund as project_fund



# table objects
#________________________________________________________________________________________________________________________

st = s.Table("project_bees", metadata, autoload=True, autoload_with=engine) #project_source
b = s.Table("bees", metadata, autoload=True, autoload_with=engine) #project_source


# crud table options
#________________________________________________________________________________________________________________________
def select_table():
    # the query object
    query = s.select([st.columns.project_bees_id, st.columns.project_id,st.columns.bee_no])
    # execute query
    select_result_proxy = connection.execute(query)
    return select_result_proxy

def update_table():
    fund_bees_id = int(input("Select fund_bees id: "))
    project_fund_id = input("Insert project fund_id: ")
    bee_no = input("Insert bee no: ")

    update = s.update(st).values(project_fund_id= project_fund_id,bee_no=bee_no).where(st.columns.fund_bees_id == fund_bees_id)
    proxy = connection.execute(update)
    ans = "selected id updated"
    return ans

def delete_table():
    fund_bees_id = int(input("Select fund_bees_id: "))
    query = s.delete(st).where(st.columns.fund_bees_id == fund_bees_id)
    proxy = connection.execute(query)
    ans = "selected id deleted"
    return ans

def insert_table(project_id):
    while True:
        bee_no = bees.display_table("bees")
        # check if project_id and bee_no already recorded to avoid repetition
        available = check_project_bee_availability(project_id,bee_no)
        if not available:
            insert_fund_bees = s.insert(st).values(
                project_id=project_id,
                bee_no=bee_no)
            proxy = connection.execute(insert_fund_bees)
        else:
            print(f"Bee no {bee_no} already recorded.")

        user_input = str.lower(input("another bee? (y/n)?:"))

        if user_input == "y":
            pass
        elif user_input == "n":
            break
        else:
            print("wrong input")

 
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
        output_dict = {}
        for result in select:
            #convert tuple output to one item
            column_a = result[0]
            column_b= result[1]

            # table_id (primary key) recorded as the key, followed by identifier name

            output_dict[column_a]=str.upper(column_b)

        # insert option to update if input is missing
        changes = {"u":"update","d":"delete","i":"insert" }


        # DISPLAY ENTRIES IN DATABASE
        #_______________________________________________________________________________________
        print()
        print(F"{table_name}")
        print("***************************************************")
        for key, value in output_dict.items():
            print(f"{key}:{value}")
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
            if user_selection in output_dict.keys():
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


        
    for key,value in salary.items():
        print(f"{key}:{value}")
    return salary


# select functions
#________________________________________________________________________________________________________________________


def check_project_bee_availability(project_id : int,bee_no: int) -> bool:
    """scan through the database for entries with similar project_id and scan_id

    Args:
        project_id (int): project_id
        bee_no (int): be_no

    Returns:
        bool: returns true if it finds one
    """

    query = s.select([st.columns.project_id,st.columns.bee_no]).where(st.columns.project_id==project_id and st.columns.bee_no==bee_no )
    select_result_proxy = connection.execute(query)
    items = [result for result in select_result_proxy]

    composite_key = [int(str(item[0])+str(item[1])) for item in items]
    composite_check = int(str(project_id) + str(bee_no))
    
    if composite_check in composite_key:
        availability = True
    else:
        availability = False

    return availability
    


if __name__ == "__main__":
    ava = check_project_bee_availability(36,9)
    print(ava)
    
