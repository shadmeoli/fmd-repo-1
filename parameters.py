# record the commencement and completion date
def project_date():
    """generate the date object at time of the recording"""
    global current_date
    from datetime import date
    print("Insert \n"
          "1) Today's date\n"
          "2) Custom date")

    user_option = int(input("insert: "))

    if user_option == 1:
        current_date = date.today()

    elif user_option == 2:
        custom_date = int(input("date:"))
        custom_month = int(input("month:"))
        custom_year = int(input("year"))

        current_date = date(custom_year, custom_month, custom_date)
    return current_date


# record the client name

def client_name():
    """record the client name for the project"""
    global name
    print("\n****NAME OF CLIENT****")
    correct = True
    while correct:
        name = str.lower(input("insert name:"))

        if " " in name:
            correct = True
            print("first and surname should be joined by hyphen\n"
                  "check instructions")
        elif name is None:
            correct = True
            print("a project must have a client, how do you pay bills, without him?")

        else:
            correct = False

    return name


def project_setup(filename, filetype):
    """establish project source"""
    global purpose
    import csv
    from configurations import project_configuration

    file_type_upper = str.upper(filetype)

    try_again = True
    while try_again:
        category_dict = {}
        print(f"\n****{file_type_upper}*****")
        with open(filename, "r") as f:
            iterable = csv.reader(f)
            list_iterable = list(iterable)
            for x in list_iterable:
                print(f"{x[0]}. {x[1]}")
                category_dict[int(x[0])] = x[1]
            print("0. (modify list)")
        user_selection = int(input("Insert option above: "))

        for x in category_dict:
            if user_selection == x:
                purpose = category_dict[x]
                try_again = False
                return purpose
        if user_selection == 0:
            project_configuration(filename, filetype)


def project_fund():
    """Total amount paid for the project"""
    print("\n****PROJECT FUND*****")
    projectFund = int(input("Amount paid:"))

    return projectFund


def project_funds_distribution(projectSource, doneBy, projectFund):
    """The total amount payable for the particular project"""
    company_fund = 0
    brian_income = 0
    symon_income = 0
    other_income = 0
    tax = 0

    if projectSource == "FIVERR":
        shareable_fund = (projectFund / 100) * 80
        tax = (projectFund / 100) * 20
    else:
        shareable_fund = projectFund

    if doneBy == "BRIAN":
        company_fund = (shareable_fund / 100) * 50
        brian_income = shareable_fund - company_fund
    elif doneBy == "SYMON":
        company_fund = (shareable_fund / 100) * 50
        symon_income = shareable_fund - company_fund

    elif doneBy == "SYMON-BRIAN":
        company_fund = (shareable_fund / 100) * 50
        sharable_income = shareable_fund - company_fund
        print("\n*****SHAREABLE_FORMULA *****\n"
              "Symon(s):Brian(B)\n"
              "1)50%S : 50%B \n"
              "2)15%S : 85B% \n"
              "3)85%S : 15B% \n"
              "4)80%S : 20B% \n"
              "5)20%S : 80%B ")
        shareable_formula = input("insert formula:")

        if shareable_formula == 1:
            symon_income = sharable_income / 2
            brian_income = sharable_income / 2

        elif shareable_formula == 2:
            symon_income = (shareable_fund / 100) * 15
            brian_income = (shareable_fund / 100) * 85

        elif shareable_formula == 3:
            symon_income = (shareable_fund / 100) * 85
            brian_income = (shareable_fund / 100) * 15

        elif shareable_formula == 4:
            symon_income = (shareable_fund / 100) * 80
            brian_income = (shareable_fund / 100) * 20

        elif shareable_formula == 5:
            symon_income = (shareable_fund / 100) * 20
            brian_income = (shareable_fund / 100) * 80

    elif doneBy == "OTHER":
        company_fund = (shareable_fund / 100) * 10
        other_fund = shareable_fund - company_fund

    funds = (company_fund, brian_income, symon_income, other_income, tax)
    return funds


def project_name(date, clientName, category):
    """establish the name of the project, should be used as primary key"""
    prjt_name = str(date) + "_" + str(clientName) + "_" + str(category)
    return prjt_name
