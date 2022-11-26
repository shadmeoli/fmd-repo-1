#connection
from pymysql import NULL
import sqlalchemy as s
from connect import engine
from connect import connection
from connect import metadata

import algos

import tables_project.project_category as project_category 
import tables_project.project_source as project_source
import tables_project.project_status as project_status
import tables_project.scope as scope

# table objects
#________________________________________________________________________________________________________________________
st = s.Table("project", metadata, autoload=True, autoload_with=engine) #project
ps = s.Table("project_status", metadata, autoload=True, autoload_with=engine) #project status
psc = s.Table("project_scope", metadata, autoload=True, autoload_with=engine) #project scope

# crud functions
#________________________________________________________________________________________________________________________
def select_table():
    # the query object
    query = s.select([st.columns.project_id, st.columns.project_name])
    # execute query
    select_result_proxy = connection.execute(query)
    return select_result_proxy

def update_table():
    PROJECT_ID = int(input("Select project id: "))
    CLIENT_NAME = algos.client_name()
    DATE_COMMENCMENT = algos.date_setup("date of commencment")
    PROJECT_CATEGORY_ID = project_category.show_table()
    PROJECT_NAME = algos.project_name()
    PROJECT_SOURCE_ID = project_source.show_table()
    PROJECT_SCOPE_ID = 0
    PROJECT_STATUS_ID = project_status.show_table()
    DATE_COMPLETION = algos.date_setup("date of completion")
   
    update = s.update(st).values(
        client_name=CLIENT_NAME,
        date_commencment=DATE_COMMENCMENT,
        project_name=PROJECT_NAME,
        project_category_id=PROJECT_CATEGORY_ID,
        project_source_id=PROJECT_SOURCE_ID,
        project_scope_id=PROJECT_SCOPE_ID,
        project_status_id=PROJECT_STATUS_ID,
        date_completion=DATE_COMPLETION
        ).where(st.columns.project_id == PROJECT_ID)
    proxy = connection.execute(update)
    ans = "selected id updated"
    return ans

def update_status(PROJECT_ID,PROJECT_STATUS_ID,DATE_OF_COMPLETION):
    update = s.update(st).values(project_status_id=PROJECT_STATUS_ID,date_completion=DATE_OF_COMPLETION ).where(st.columns.project_id == PROJECT_ID)
    proxy = connection.execute(update)
    ans = "selected id updated"
    return ans



    id_selection = int(input("Select project id: "))
    query = s.delete(st).where(st.columns.project_id == id_selection)
    proxy = connection.execute(query)
    ans = "selected id deleted"
    return ans

def insert_table(CLIENT_NAME,DATE_COMMENCMENT,PROJECT_CATEGORY_ID,PROJECT_NAME,PROJECT_SOURCE_ID,PROJECT_STATUS_ID,PROJECT_FUND_ID,date_completion = True):
    if date_completion is True:
        DATE_COMPLETION = algos.date_setup("date of completion")

        insert = s.insert(st).values(
            client_name=CLIENT_NAME,
            date_commencment=DATE_COMMENCMENT,
            project_name=PROJECT_NAME,
            project_category_id=PROJECT_CATEGORY_ID,
            project_source_id=PROJECT_SOURCE_ID,
            project_status_id=PROJECT_STATUS_ID,
            project_fund_id=PROJECT_FUND_ID,
            date_completion=DATE_COMPLETION
            )

        proxy = connection.execute(insert)
        ans = f"{PROJECT_NAME} inserted"
    else:
        insert = s.insert(st).values(
            client_name=CLIENT_NAME,
            date_commencment=DATE_COMMENCMENT,
            project_name=PROJECT_NAME,
            project_category_id=PROJECT_CATEGORY_ID,
            project_source_id=PROJECT_SOURCE_ID,
            project_status_id=PROJECT_STATUS_ID,
            project_fund_id=PROJECT_FUND_ID,
            )

        proxy = connection.execute(insert)
        ans = f"{PROJECT_NAME} inserted"


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



# select functions
#________________________________________________________________________________________________________________________

def active_projects()-> int:
    """select active projects filter with project_status

    Returns:
        int: the id of the selected project
    """
    # the query object
    join_statement = st.join(ps,ps.columns.project_status_id == st.columns.project_status_id)
    query = s.select([st.columns.project_id, st.columns.project_name]).select_from(join_statement).where(ps.columns.project_status_desc == "ACTIVE").order_by(s.asc(st.columns.project_id))
    # execute query
    select_result_proxy = connection.execute(query)
    selected_items = [result for result in select_result_proxy] #convert to 2d list
    items_dict = {item[0]:item[1] for item in selected_items} #convert tuples to dict

    print(F"\nActive projects")
    print("***************************************************")
    for key, value in items_dict.items():
        print(f"{key}:{value}")
    print("\n***************************************************")
    user_selection = int(input("select project: "))
    print(f"{items_dict[user_selection]} selected")

    return user_selection


def retrieve_project_id():
    # retrieve the id of the project just inserted
     # the query object
    query = s.select([st.columns.project_id, st.columns.project_name]).order_by(s.desc(st.columns.project_id)).limit(1)
    # execute query
    select_result_proxy = connection.execute(query)

    for result in select_result_proxy:
        project_id = result[0]

    print(project_id)

    return project_id
    



if __name__ == "__main__":
    display_table("project")
