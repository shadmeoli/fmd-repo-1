
import sub_programs as sp

def main():
    """ engine of the programme"""


    correct = True
    while correct:
        print("""
          o__ __o__/_                                                                o               
 <|    v                                                                    <|>              
 < >                                                                        < \              
  |              o__ __o    \o__ __o   \o__ __o__ __o     o__ __o      o__ __o/    o__  __o  
  o__/_         /v     v\    |     |>   |     |     |>   /v     v\    /v     |    /v      |> 
  |            />       <\  / \   < >  / \   / \   / \  />       <\  />     / \  />      //  
 <o>           \         /  \o/        \o/   \o/   \o/  \         /  \      \o/  \o    o/    
  |             o       o    |          |     |     |    o       o    o      |    v\  /v __o 
 / \            <\__ __/>   / \        / \   / \   / \   <\__ __/>    <\__  / \    <\/> __/> 
                                                                                               
        """)
        print("*******FORMODE REPOSITORY**************")
        print("1) Add project data\n"
              "2) Bee Financial stats\n"
              "3) Completed projects\n"
              "4) Active projects\n"
              "5) Add transaction data\n"
              "6) Net fund\n"
              "7) Project calculator\n"
              "0) Quit")
        print("**************************************")
        user_selection = int(input("insert option: "))

        if user_selection == 1:
            sp.insert_project_data()
        # check earnings
        elif user_selection == 2:
           sp.bee_status()
        # view complete projects
        elif user_selection == 3:
            print("In progress")
        # view active projects
        elif user_selection == 4:
            sp.mark_active_projects()
        # formode fund
        elif user_selection == 5:
            sp.insert_transaction_data()
        # settings
        elif user_selection == 6:
            sp.net_company_fund()

        elif user_selection == 7:
            sp.project_calculator()
            
        # Quit
        elif user_selection == 0:
            correct = False
            print("""Unless the Lord builds the house,those who build it labor in vain.\nThank you!""")
        else:
            print("Wrong input, try again")



if __name__ == "__main__":
    main()

