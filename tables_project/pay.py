#connection
import sqlalchemy as s
from connect import engine
from connect import connection
from connect import metadata

import tables_project.project as project
import tables_project.bees as bees
import tables_project.project_fund as project_fund

import algos

# table objects
#________________________________________________________________________________________________________________________

st = s.Table("pay", metadata, autoload=True, autoload_with=engine) #project_source
pb = s.Table("project_bees", metadata, autoload=True, autoload_with=engine) #project_bees
pf = s.Table("project_fund", metadata, autoload=True, autoload_with=engine) #project fund
p = s.Table("project", metadata, autoload=True, autoload_with=engine) #project
b = s.Table("bees", metadata, autoload=True, autoload_with=engine) #project


# crud table options
#________________________________________________________________________________________________________________________
def select_table():
    join_statement = st.join(pb,pb.columns.fund_bees_id==st.columns.fund_bees_id).join(pf,pf.columns.project_fund_id==pb.columns.project_fund_id).join(p,p.columns.project_id==pf.columns.project_id)
    # select project_id,project_name and the salary fund
    query = s.select([p.columns.project_id, p.columns.project_name,pf.columns.salaries]).select_from(join_statement)
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

def insert_table(project_id,salary):
    salary = float(salary)
    list_details =[]
    #select bees who did this particular project
    query = s.select([pb.columns.project_bees_id,pb.columns.bee_no]).where(pb.columns.project_id == project_id)#.select_from(join_statement)#
    select_result_proxy = connection.execute(query)

    list_details = [ [result[0], result[1]] for result in select_result_proxy]


    for list_item in list_details:
        bee_name = bees.show_bee_name(list_item[1])
        amount_earned = float(input(f"{str.upper(bee_name)} SHARE : "))

        insert_fund_bees = s.insert(st).values(project_bees_id=list_item[0],pay_amount=amount_earned)
        proxy = connection.execute(insert_fund_bees)
        rem = salary - amount_earned
        salary = rem
        print(f"REMAINING SALARY : {rem}")

    if salary != 0:
        print(f"The was an error in recording the input, the unassigned remaining salary is {salary} ")

        error = True
    else:
        error = False
    return error


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

def salaries_total(bee_no):
    # the query object
    join_statement = st.join(pb,pb.columns.project_bees_id == st.columns.project_bees_id).join(p,p.columns.project_id == pb.columns.project_id)
    query = s.select([p.columns.project_id,p.columns.project_name,st.columns.pay_amount,p.columns.date_completion]).select_from(join_statement).where(pb.columns.bee_no == bee_no).order_by(s.asc(p.columns.date_completion))
    # execute query
    select_result_proxy = connection.execute(query)
    selected_items = [result for result in select_result_proxy] #convert to 2d list

    bee_name = bees.show_bee_name(bee_no)
   
    sum = 0
    print()
    print(f"total project completed by bee: {bee_name}")
    print("*************************************************")
    #item[0]- project_id
    #item[1]- project_name
    #item[2]- pay_amount
    #item[3]- date completion
    
    for items in selected_items:
        if items is not None:
            sum += items[2] * 110
        print(f"id: {items[0]} ~~~ project_name : {items[1]} ~~~  pay_amount: {items[2] * 110} ~~~  date_completion: {items[3]}")

    print("*************************************************")

    print(f"Total sum: {sum}")

    return sum
    

if __name__ == "__main__":
    salaries_total(3)

