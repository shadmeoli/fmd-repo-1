
from select import select
import sqlalchemy as s
from connect import engine
from connect import connection
from connect import metadata

import algos

import tables_project.project_category as project_category 
import tables_project.project_source as project_source
import tables_project.project_status as project_status
import tables_project.scope as scope
import tables_project.project as project
import tables_project.project_scope as project_scope
import tables_project.project_fund as project_fund
import tables_project.project_bees as project_bees
import tables_project.pay as pay
import tables_project.bees as bees


import tables_transaction.co_account as co_account
import tables_transaction.co_company as co_company
import tables_transaction.co_fund as co_fund
import tables_transaction.co_loans as co_loans
import tables_transaction.co_loans_type as co_loans_type
import tables_transaction.co_loans
import tables_transaction.co_operations as co_operations
import tables_transaction.co_salaries as co_salaries
import tables_transaction.co_transaction as co_transaction
import tables_transaction.co_transtatus as co_transtatus_id
import tables_transaction.co_operations_type as co_operations_type


st = s.Table("project", metadata, autoload=True, autoload_with=engine) #selected table
ps = s.Table("project_scope", metadata, autoload=True, autoload_with=engine) #project_scope


def insert_project_data():

    #ensure the ids are intandem with the database for it to work
    # PROJECT STATUS ID
    ACTIVE_ID = 1
    COMPLETE_ID = 2
    CANCELLED_ID = 3

    CLIENT_NAME = algos.client_name()
    DATE_COMMENCMENT = algos.date_setup("date of commencment")

    #extract the category name in order to create the project name
    return_value = project_category.display_table("project_category")
    PROJECT_CATEGORY_ID = return_value[0]
    PROJECT_CATEGORY = str.lower(return_value[1])

    PROJECT_NAME = algos.project_name(DATE_COMMENCMENT,CLIENT_NAME,PROJECT_CATEGORY)
    PROJECT_SOURCE_ID = project_source.display_table("project_source")
    PROJECT_STATUS_ID = project_status.display_table("project_status")

     # ADD PROJECT FUND
    PROJECT_FUND_ID =project_fund.insert_table(PROJECT_SOURCE_ID)


    if PROJECT_STATUS_ID == ACTIVE_ID:
        # ADD PROJECT TABLE
        project.insert_table(CLIENT_NAME,DATE_COMMENCMENT,PROJECT_CATEGORY_ID,PROJECT_NAME,PROJECT_SOURCE_ID,PROJECT_STATUS_ID,PROJECT_FUND_ID,date_completion=False)
        
        # retirieve project id
        PROJECT_ID = project.retrieve_project_id()

        # ADD PROJECT SCOPE
        project_scope.insert_table(PROJECT_ID)

    
    elif PROJECT_STATUS_ID == COMPLETE_ID:

        # ADD PROJECT TABLE + DATE COMPLETION
        project.insert_table(CLIENT_NAME,DATE_COMMENCMENT,PROJECT_CATEGORY_ID,PROJECT_NAME,PROJECT_SOURCE_ID,PROJECT_STATUS_ID,PROJECT_FUND_ID,date_completion=True)

        # retirieve project id
        PROJECT_ID = project.retrieve_project_id()

        # ADD PROJECT SCOPE
        project_scope.insert_table(PROJECT_ID)

        # ADD FUND BEES ( BEES WHO DID THE WORK)
        project_bees.insert_table(PROJECT_ID)

        # show them salaries to be distributed.
        pj_fund, company, salaries = project_fund.retrieve_project_company_salaries_fund(PROJECT_ID)

        print(f"SALARY TO BE DISTRIBUTED : {salaries}")

        # pay the active bees
        pay.insert_table(PROJECT_ID,salaries)
    
def insert_transaction_data():
    #account_id
    co_account_id = co_account.display_table("account_id")

    # co_fund
    co_fund_id = co_fund.display_table("co_fund")
    #company_fund or salaries_fund
    if co_fund_id == 1: 
        co_company_id = co_company.display_table("co_company")
        print("complete")
        #operations or loan_allocation
        if co_company_id == 1:#operations
            #project_fund or running_cost
            co_operations_type_id = co_operations_type.display_table("operation_type")
            if co_operations_type_id == 1: #project_fund
                co_transtatus_id = 1
                co_operation_id = co_operations.display_table("co_operations",co_operations_type_id,co_company_id)

                if co_operation_id == 2: #if a virtual project, store er and  project_income at the same time.
                    date_of_transaction = algos.date_setup("date of transaction")
                    project_income, er_income = algos.dollars_to_ksh()
                    # project_income
                    co_transaction_id =co_transaction.insert_table_operations_money_in(co_account_id,co_operation_id,co_transtatus_id,project_income,date_of_transaction)

                    #er_income
                    co_operation_id = 3
                    co_transaction_id =co_transaction.insert_table_operations_money_in(co_account_id,co_operation_id,co_transtatus_id,er_income,date_of_transaction)

                else:
                    money_in = algos.money_setup("Money in")
                    date_of_transaction = algos.date_setup("date of transaction")
                    co_transaction_id =co_transaction.insert_table_operations_money_in(co_account_id,co_operation_id,co_transtatus_id,money_in,date_of_transaction)
                

            elif co_operations_type_id == 2: #running_cost
                co_transtatus_id = 2
                co_operation_id = co_operations.display_table("co_operations",co_operations_type_id,co_company_id)
                money_out = algos.money_setup("Money out")
                date_of_transaction = algos.date_setup("date of transaction")
                co_transaction_id =co_transaction.insert_table_operations_money_out(co_account_id,co_operation_id,co_transtatus_id,money_out,date_of_transaction)

            else:
                print("I need an update")

        elif co_company_id == 2:#loans
            #loan_issued or loans_repayed
        
            co_loan_type_id = co_loans_type.display_table("co_loan_type")

            if co_loan_type_id == 1:
                co_transtatus_id = 2
                bee_no = bees.display_table("bees")
                co_loans.insert_table(co_company_id,bee_no,co_loan_type_id)
                co_loans_id = co_loans.retrieve_co_loans_id()
                money_out = algos.money_setup("Money out")
                date_of_transaction = algos.date_setup("date of transaction")

                co_transaction_id =co_transaction.insert_table_loans_money_out(co_account_id,co_loans_id,co_transtatus_id,money_out,date_of_transaction)

            elif co_loan_type_id == 2:
                co_transtatus_id = 1
                bee_no = bees.display_table("bees")
                co_loans.insert_table(co_company_id,bee_no,co_loan_type_id)
                co_loans_id = co_loans.retrieve_co_loans_id()
                money_in = algos.money_setup("Money in")
                date_of_transaction = algos.date_setup("date of transaction")
                co_transaction_id =co_transaction.insert_table_loans_money_in(co_account_id,co_loans_id,co_transtatus_id,money_in,date_of_transaction)

        else:
            print("I need an update")

    elif co_fund_id == 2:
        co_transtatus_id = 2
        bee_no = bees.display_table("bees")
        co_salaries.insert_table(co_fund_id,bee_no)
        co_salaries_id = co_salaries.retrieve_salaries_id()
        money_out = algos.money_setup("Money out")
        date_of_transaction = algos.date_setup("date of transaction")
        co_transaction.insert_table_salaries_money_out(co_account_id,co_salaries_id,co_transtatus_id,money_out,date_of_transaction)
    else:
        print("error")
        
def bee_status():
    print("\n***************BEE FINANCIAL STATS*****************")

    bee_no = bees.display_table("bees")

    print("***********************SALARIES***********************")
    # Establish all the projects done
    salaries_total = pay.salaries_total(bee_no)
    # Establish all the projects payed
    salaries_payed = co_transaction.salaries_payed(bee_no)
    salaries_remainder = salaries_total - salaries_payed
    print("******************************************************")
    print(f"Unpayed Salaries: {salaries_remainder}")
    print()


    print("***********************LOANS***********************")
    # Establish all the projects done
    loans_issued = co_transaction.loans_issued(bee_no)
    # Establish all the projects payed
    loans_repayed = co_transaction.loans_repayed(bee_no)
    loans_remainder = loans_issued - loans_repayed
    print("***************************************************")
    print(f"Unpayed Salaries: {loans_remainder}")

    print()
    print("***********************NET INCOME***********************")
    net_income = salaries_remainder - loans_remainder
    print(f"{net_income}")

def project_calculator():

    print()
    print(f"project calculator")
    print("***************************************************")
    project_source_id = project_source.display_table("project_source")
    project_fund = algos.project_fund("project fund",project_source_id)
    
    algos.display_fee_distribution(project_source_id,project_fund,timeline=False)

    print("***************************************************")

def mark_active_projects():

    print("************ACTIVE PROJECTS**********")
    print("1. View project Quote\n2. Mark project Complete")
    print("************************************")
    user_input = int(input("insert option: "))

    project_id = project.active_projects()
    project_source_id = project_source.retrieve_project_source_id(project_id)
    fund_project, fund_company, fund_salary = project_fund.retrieve_project_company_salaries_fund(project_id)

    if user_input == 1:
        algos.display_fee_distribution(project_source_id,fund_project,timeline=True)
     
    
    elif user_input == 2:
        if project_id == 0:
            return None
        else:
            # project completion date
            project_status_id = 2 #from active to complete
            date_of_completion = algos.date_setup("date of completion")
            
            # refresh project fund
            project_fund_id = project_fund.update_table(project_source_id,project_id)
        
            # retreive new salary
            fund_project_new, fund_company_new, fund_salary_new = project_fund.retrieve_project_company_salaries_fund(project_id)

            # ADD FUND BEES ( BEES WHO DID THE WORK)
            project_bees.insert_table(project_id)


            # display salary
            print(f"SALARY TO BE DISTRIBUTED : {fund_salary_new}")

             # pay the active bees
            pay.insert_table(project_id,fund_salary_new)

            #close project
            project.update_status(project_id,project_status_id,date_of_completion)

def net_company_fund():
    print("COMPANY REVENUE INCOME")
    # establish all the company fund recieved
    print("***************************************************")
    total_company_fund = project_fund.company_fund_total()

    total_er_income = co_transaction.select_total_er_income()

    print("***************************************************")
    
    print("\nCOMPANY REVENUE EXPENDITURE")
    # establish all the running cost
    total_running_cost = co_transaction.select_total_running_cost()

    print("***************************************************")
    returns = (total_company_fund + total_er_income) - (total_running_cost)

    print(f"NET INCOME: {returns}")


 
if __name__ == "__main__":
    pass
    #bee_status(2)
    #insert_transaction_data()
    net_company_fund()


