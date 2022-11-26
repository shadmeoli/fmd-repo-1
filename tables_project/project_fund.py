#connection
import sqlalchemy as s
from connect import engine
from connect import connection
from connect import metadata


import algos


# table objects
#________________________________________________________________________________________________________________________
st = s.Table("project_fund", metadata, autoload=True, autoload_with=engine) #project_fund
p = s.Table("project", metadata, autoload=True, autoload_with=engine) #project_fund


# crud table options
#________________________________________________________________________________________________________________________
def select_table():
    # the query object
    query = s.select([st.columns.project_fund_id, st.columns.project_fund,st.columns.company_fund,st.columns.consultancies_fund,st.columns.salaries,st.columns.tax])
    # execute query
    select_result_proxy = connection.execute(query)
    return select_result_proxy

def update_table(project_source_id,project_fund_id):
    project_fund = algos.project_fund("project_fund",project_source_id)
    company_fund,salaries,tax = algos.project_funds_distribution_V3(project_source_id,project_fund,optical_illusion=False)
    update = s.update(st).values(project_fund=project_fund,company_fund=company_fund,salaries_fund=salaries,tax=tax).where(st.columns.project_fund_id == project_fund_id)
    proxy = connection.execute(update)
    ans = "selected id updated"
    return ans

def delete_table():
    project_fund_id = int(input("Select project source id: "))
    query = s.delete(st).where(st.columns.project_fund_id == project_fund_id)
    proxy = connection.execute(query)
    ans = "selected id deleted"
    return ans

def insert_table(project_source_id):
    project_fund = algos.project_fund("project_fund",project_source_id)
    company_fund,salaries,tax = algos.project_funds_distribution_V3(project_source_id,project_fund) #distribute funds according to the source.
    insert = s.insert(st).values(project_fund=project_fund,company_fund=company_fund,salaries_fund=salaries,tax=tax)
    proxy = connection.execute(insert)
    ans = f"{project_fund} inserted"

    #retrieve project_fund id of the above transaction so that It can be saved in the project table,

    query = s.select([st.columns.project_fund_id]).order_by(s.desc(st.columns.project_fund_id)).limit(1)
    select_result_proxy = connection.execute(query)

    for result in select_result_proxy:
        project_fund_id = result[0]

    return project_fund_id


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


# select options
#________________________________________________________________________________________________________________________

def retrieve_project_fund_id():
    # retrieve the id of the project just inserted
     # the query object
    query = s.select([st.columns.project_fund_id]).order_by(s.desc(st.columns.project_fund_id)).limit(1)
    # execute query
    select_result_proxy = connection.execute(query)

    for result in select_result_proxy:
        project_fund_id = result[0]

    print(project_fund_id)

    return project_fund_id


def retrieve_project_company_salaries_fund(project_id)-> tuple:
    # retrieve the id of the project just inserted
    # the query object
    join_statement = st.join(p,p.columns.project_fund_id == st.columns.project_fund_id)
    query = s.select([st.columns.project_fund,st.columns.company_fund,st.columns.salaries_fund]).select_from(join_statement).where(p.columns.project_id == project_id)
    # execute query
    select_result_proxy = connection.execute(query)

    for result in select_result_proxy:
        project_fund = result[0] #project_fund
        company = result[1] #company
        salaries = result[2] #salaries
        result = [project_fund, company, salaries]

    return project_fund, company, salaries


def company_fund_total():
    # the query object
    join_statement = st.join(p,p.columns.project_fund_id == st.columns.project_fund_id)
    query = s.select([p.columns.project_id,p.columns.project_name,st.columns.company_fund,p.columns.date_completion]).select_from(join_statement).where(p.columns.project_status_id== 2).order_by(s.asc(p.columns.project_id))
    # execute query
    select_result_proxy = connection.execute(query)
    selected_items = [result for result in select_result_proxy] #convert to 2d list

    sum = 0
    print()
    print(f"Total projects completed by Formode Architecture: ")
    print("*************************************************")
    #item[0]- project_id
    #item[1]- project_name
    #item[2]- company_fund
    #item[3]- date completion
    
    for items in selected_items:
        if items is not None:
            sum += items[2] * 110
        print(f"id: {items[0]} ~~~ project_name : {items[1]} ~~~  company_fund: {items[2] * 110} ~~~  date_completion: {items[3]}")

    print("*************************************************")

    print(f"Total sum: {sum}")

    return sum


if __name__ == "__main__":
    company_fund_total()



