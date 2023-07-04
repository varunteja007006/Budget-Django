from collections import defaultdict

expenses_type_list = ['Dues', 'Loan', 'Food', 'Electronics', 'Subscriptions', 'Entertainment', 'Rent', 'Transportation']

    # # category wise monthly data
    # tot_monthly_exp = []
    # total_dues = 0
    # for obj in obj_expenses.filter(type='Dues'):
    #     total_dues = total_dues + obj.cost
    # tot_monthly_exp.append(total_dues)

    # total_loans = 0
    # for obj in obj_expenses.filter(type='Loan'):
    #     total_loans = total_loans + obj.cost
    # tot_monthly_exp.append(total_loans)

    # total_food = 0
    # for obj in obj_expenses.filter(type='Food'):
    #     total_food = total_food + obj.cost
    # tot_monthly_exp.append(total_food)

    # total_electronics = 0
    # for obj in obj_expenses.filter(type='Electronics'):
    #     total_electronics = total_electronics + obj.cost
    # tot_monthly_exp.append(total_electronics)

    # total_subscriptions = 0
    # for obj in obj_expenses.filter(type='Subscriptions'):
    #     total_subscriptions = total_subscriptions + obj.cost
    # tot_monthly_exp.append(total_subscriptions)

    # total_entertainment = 0
    # for obj in obj_expenses.filter(type='Entertainment'):
    #     total_entertainment = total_entertainment + obj.cost
    # tot_monthly_exp.append(total_entertainment)

    # total_rent = 0
    # for obj in obj_expenses.filter(type='Rent'):
    #     total_rent = total_rent + obj.cost
    # tot_monthly_exp.append(total_rent)

    # total_transportation = 0
    # for obj in obj_expenses.filter(type='Transportation'):
    #     total_transportation = total_transportation + obj.cost
    # tot_monthly_exp.append(total_transportation)

    # if tot_monthly_exp.count(0) == 8:
    #     tot_monthly_exp.clear()
    # tot_monthly_exp = [1, 1, 1, 1, 1, 1, 1, 1]

    # # overall expenses catergory wise
    # overall_exp = []
    # tot = 0
    # for obj in obj_overall_expenses.filter(type='Dues'):
    #     tot = tot + obj.cost
    # overall_exp.append(tot)
    # tot = 0
    # for obj in obj_overall_expenses.filter(type='Loan'):
    #     tot = tot + obj.cost
    # overall_exp.append(tot)
    # tot = 0
    # for obj in obj_overall_expenses.filter(type='Food'):
    #     tot = tot + obj.cost
    # overall_exp.append(tot)
    # tot = 0
    # for obj in obj_overall_expenses.filter(type='Electronics'):
    #     tot = tot + obj.cost
    # overall_exp.append(tot)
    # tot = 0
    # for obj in obj_overall_expenses.filter(type='Subscriptions'):
    #     tot = tot + obj.cost
    # overall_exp.append(tot)
    # tot = 0
    # for obj in obj_overall_expenses.filter(type='Entertainment'):
    #     tot = tot + obj.cost
    # overall_exp.append(tot)
    # tot = 0
    # for obj in obj_overall_expenses.filter(type='Rent'):
    #     tot = tot + obj.cost
    # overall_exp.append(tot)
    # tot = 0
    # for obj in obj_overall_expenses.filter(type='Transportation'):
    #     tot = tot + obj.cost
    # overall_exp.append(tot)
    # if overall_exp.count(0) == 8:
    #     overall_exp.clear()
    #     overall_exp = [1, 1, 1, 1, 1, 1, 1, 1]