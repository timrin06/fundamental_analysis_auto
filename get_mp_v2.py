import requests
import json
from data.sectors import sectors
from data.request_params import cookies, headers, params
from get_list import get_list
import numpy as np
import pandas as pd

symbol_list = get_list({"size":25,"offset":0,"sortField":"intradaymarketcap","sortType":"DESC","quoteType":"EQUITY","topOperator":"AND","query":{"operator":"AND","operands":[{"operator":"or","operands":[{"operator":"EQ","operands":["sector","Industrials"]}]},{"operator":"or","operands":[{"operator":"EQ","operands":["industry","Specialty Industrial Machinery"]}]},{"operator":"or","operands":[{"operator":"EQ","operands":["exchange","NYQ"]},{"operator":"EQ","operands":["exchange","NAS"]}]},{"operator":"or","operands":[{"operator":"EQ","operands":["region","us"]}]},{"operator":"gt","operands":["avgdailyvol3m",100000]},{"operator":"or","operands":[{"operator":"LT","operands":["intradaymarketcap",2000000000]},{"operator":"BTWN","operands":["intradaymarketcap",2000000000,10000000000]},{"operator":"BTWN","operands":["intradaymarketcap",10000000000,100000000000]},{"operator":"GT","operands":["intradaymarketcap",100000000000]}]},{"operator":"gt","operands":["altmanzscoreusingtheaveragestockinformationforaperiod.lasttwelvemonths",0]}]},"userId":"","userIdType":"guid"}, 100)
print(symbol_list)
cap_list = {}
q1 = 0.25
q3 = 0.75
q = ""
errors = []


#prices
for i in symbol_list:
    price = requests.get("https://query1.finance.yahoo.com/v10/finance/quoteSummary/"+ i +"?modules=price", cookies=cookies, headers=headers)
    cap = json.loads(price.text)["quoteSummary"]["result"][0]["price"]["marketCap"]["raw"]
    cap_list[i] = cap
def p_gp():
    print("gp")
    multiplicators = {}
    multi_list = {}
    data = []
    avg = []
    for i in symbol_list:
        cap = cap_list[i]
        incomeStatementHistoryQuarterly = requests.get("https://query1.finance.yahoo.com/v10/finance/quoteSummary/"+ i +"?modules=incomeStatementHistory"+q, cookies=cookies, headers=headers)
        #print(i)
        gp = json.loads(incomeStatementHistoryQuarterly.text)["quoteSummary"]["result"][0]["incomeStatementHistory"+q]["incomeStatementHistory"][0]["grossProfit"]["raw"]
        #if gp == 0:
            #print(i)
            #symbol_list.remove(i)
            #continue
        # print(gp, cap, i)
        p_gp = cap / gp
        data.append(p_gp)
        multiplicators[i] = p_gp
    print(multiplicators)
    #(pd.DataFrame(data=multi_list, index=[0]).T).to_excel('1-gp.xlsx')
    #print(avg_a, avg_std)
    for i in multiplicators:
        if multiplicators[i] > np.quantile(data, q1) and multiplicators[i] < np.quantile(data, q3):
            avg.append(multiplicators[i])
    mean = np.mean(avg)
    print(np.median(avg))
    print(mean)
    for i in multiplicators:
        multi_list[i] = mean / multiplicators[i]
    #(pd.DataFrame(data=multi_list, index=[0]).T).to_excel('1.xlsx')
    return [multi_list, multiplicators]
def p_s():
    print("ps")
    multiplicators = {}
    multi_list = {}
    data = []
    avg = []
    for i in symbol_list:
        cap = cap_list[i]
        incomeStatementHistoryQuarterly = requests.get("https://query1.finance.yahoo.com/v10/finance/quoteSummary/"+ i +"?modules=incomeStatementHistory"+q, cookies=cookies, headers=headers)
        #print(i)
        s = json.loads(incomeStatementHistoryQuarterly.text)["quoteSummary"]["result"][0]["incomeStatementHistory"+q]["incomeStatementHistory"][0]["totalRevenue"]["raw"]
        p_s = cap / s
        data.append(p_s)
        multiplicators[i] = p_s
    print(multiplicators)
    #print(avg_a, avg_std)
    for i in multiplicators:
        if multiplicators[i] > np.quantile(data, q1) and multiplicators[i] < np.quantile(data, q3):
            avg.append(multiplicators[i])
    mean = np.mean(avg)
    print(np.median(avg))
    print(mean)
    for i in multiplicators:
        multi_list[i] = mean / multiplicators[i]
    #(pd.DataFrame(data=multi_list, index=[0]).T).to_excel('2.xlsx')
    return [multi_list, multiplicators]
def p_b():
    print("pb")
    multiplicators = {}
    multi_list = {}
    data = []
    avg = []
    for i in symbol_list:
        cap = cap_list[i]
        balanceSheetHistoryQuarterly = requests.get("https://query1.finance.yahoo.com/v10/finance/quoteSummary/"+ i +"?modules=balanceSheetHistory"+q, cookies=cookies, headers=headers)
        #print(i)
        b = json.loads(balanceSheetHistoryQuarterly.text)["quoteSummary"]["result"][0]["balanceSheetHistory"+q]["balanceSheetStatements"][0]["totalAssets"]["raw"]
        p_b = cap / b
        data.append(p_b)
        multiplicators[i] = p_b
    print(multiplicators)
    #(pd.DataFrame(data=multi_list, index=[0]).T).to_excel('3-b.xlsx')
    #print(avg_a, avg_std)
    for i in multiplicators:
        if multiplicators[i] > np.quantile(data, q1) and multiplicators[i] < np.quantile(data, q3):
            avg.append(multiplicators[i])
    mean = np.mean(avg)
    print(np.median(avg))
    print(mean)
    for i in multiplicators:
        multi_list[i] = mean / multiplicators[i]
    #(pd.DataFrame(data=multi_list, index=[0]).T).to_excel('3.xlsx')
    return [multi_list, multiplicators]
def p_e():
    print("pe")
    multi_list = {}
    multiplicators = {}
    data_p = []
    data_m = []
    avg_p = []
    avg_m = []
    for i in symbol_list:
        cap = cap_list[i]
        incomeStatementHistoryQuarterly = requests.get("https://query1.finance.yahoo.com/v10/finance/quoteSummary/"+ i +"?modules=incomeStatementHistory"+q, cookies=cookies, headers=headers)
        #print(i)
        e = json.loads(incomeStatementHistoryQuarterly.text)["quoteSummary"]["result"][0]["incomeStatementHistory"+q]["incomeStatementHistory"][0]["netIncome"]["raw"]
        p_e = cap / e
        #print(gp, cap, i)
        if p_e < 0:
            data_m.append(p_e)
        else:
            data_p.append(p_e)
        multiplicators[i] = p_e
    print(multiplicators)
    #(pd.DataFrame(data=multi_list, index=[0]).T).to_excel('4-gp.xlsx')
    #print(avg_a, avg_std)
    for i in multiplicators:
        if multiplicators[i] < 0:
            if multiplicators[i] > np.quantile(data_m, q1) and multiplicators[i] < np.quantile(data_m, q3):
                avg_m.append(multiplicators[i])
            elif len(data_m) < 4:
                avg_m = data_m
        else:
            if multiplicators[i] > np.quantile(data_p, q1) and multiplicators[i] < np.quantile(data_p, q3):
                avg_p.append(multiplicators[i])
            elif len(data_p) < 4:
                avg_p = data_p
    mean_p = np.mean(avg_p)
    mean_m = np.mean(avg_m)
    print(np.median(avg_p), np.median(avg_m))
    print(mean_p, mean_m)
    for i in multiplicators:
        if multiplicators[i] < 0:
            multi_list[i] = mean_m / multiplicators[i] * (-1)
        else:
            multi_list[i] = mean_p / multiplicators[i]
    #(pd.DataFrame(data=multi_list, index=[0]).T).to_excel('4.xlsx')
    return [multi_list, multiplicators]
def p_e1():
    print("pe")
    multi_list = {}
    multiplicators = {}
    data_p = []
    data_m = []
    for i in symbol_list:
        cap = cap_list[i]
        incomeStatementHistoryQuarterly = requests.get("https://query1.finance.yahoo.com/v10/finance/quoteSummary/"+ i +"?modules=incomeStatementHistory"+q, cookies=cookies, headers=headers)
        #print(i)
        e = json.loads(incomeStatementHistoryQuarterly.text)["quoteSummary"]["result"][0]["incomeStatementHistory"+q]["incomeStatementHistory"][0]["netIncome"]["raw"]
        p_e = cap / e
        #print(gp, cap, i)
        if p_e < 0:
            data_m.append(p_e)
        else:
            data_p.append(p_e)
        multiplicators[i] = p_e
    print(multiplicators)
    mean_p = np.median(data_p)
    mean_m = np.median(data_m)
    print(mean_p, mean_m)
    for i in multiplicators:
        if multiplicators[i] < 0:
            multi_list[i] = mean_m / multiplicators[i] * (-1)
        else:
            multi_list[i] = mean_p / multiplicators[i]
    #(pd.DataFrame(data=multi_list, index=[0]).T).to_excel('4.xlsx')
    return [multi_list, multiplicators]
def fwd_p_e():
    print("fwd")
    multi_list = {}
    multiplicators = {}
    data_p = []
    data_m = []
    avg_p = []
    avg_m = []
    for i in symbol_list:
        cap = cap_list[i]
        earningsTrend = requests.get("https://query1.finance.yahoo.com/v10/finance/quoteSummary/"+ i +"?modules=earningsTrend", cookies=cookies, headers=headers)
        defaultKeyStatistics = requests.get("https://query1.finance.yahoo.com/v10/finance/quoteSummary/"+ i +"?modules=defaultKeyStatistics", cookies=cookies, headers=headers)
        e = json.loads(earningsTrend.text)["quoteSummary"]["result"][0]["earningsTrend"]["trend"][0]["earningsEstimate"]["growth"]
        if e == {} or e["raw"] == 0:
            errors.append(i)
            print("F  " + i)
            continue
        else:
            e = e["raw"]
        #print(gp, cap, i)
        if e < 0:
            data_m.append(e)
        else:
            data_p.append(e)
        multiplicators[i] = e
    print(multiplicators)
    #(pd.DataFrame(data=multi_list, index=[0]).T).to_excel('4-gp.xlsx')
    #print(avg_a, avg_std)
    for i in multiplicators:
        if multiplicators[i] < 0:
            if multiplicators[i] > np.quantile(data_m, q1) and multiplicators[i] < np.quantile(data_m, q3):
                avg_m.append(multiplicators[i])
            elif len(data_m) < 4:
                avg_m = data_m
        else:
            if multiplicators[i] > np.quantile(data_p, q1) and multiplicators[i] < np.quantile(data_p, q3):
                avg_p.append(multiplicators[i])
            elif len(data_p) < 4:
                avg_p = data_p
    mean_p = np.mean(avg_p)
    mean_m = np.mean(avg_m)
    print(np.median(avg_p), np.median(avg_m))
    print(mean_p, mean_m)
    for i in multiplicators:
        if multiplicators[i] < 0:
            multi_list[i] = multiplicators[i] * (-1) / mean_m
        else:
            multi_list[i] = multiplicators[i] / mean_p
    for i in errors:
        multiplicators[i] = 0
        multi_list[i] = 0
    #(pd.DataFrame(data=multi_list, index=[0]).T).to_excel('4.xlsx')
    return [multi_list, multiplicators]
def peg():
    print("peg")
    multi_list = {}
    multiplicators = {}
    data_p = []
    data_m = []
    avg_p = []
    avg_m = []
    for i in symbol_list:
        cap = cap_list[i]
        incomeStatementHistoryQuarterly = requests.get("https://query1.finance.yahoo.com/v10/finance/quoteSummary/"+ i +"?modules=incomeStatementHistory"+q, cookies=cookies, headers=headers)
        financialData = requests.get("https://query1.finance.yahoo.com/v10/finance/quoteSummary/" + i + "?modules=financialData", cookies=cookies, headers=headers)
        #print(i)
        e = json.loads(incomeStatementHistoryQuarterly.text)["quoteSummary"]["result"][0]["incomeStatementHistory"+q]["incomeStatementHistory"][0]["netIncome"]["raw"]
        gr = json.loads(incomeStatementHistoryQuarterly.text)["quoteSummary"]["result"][0]["incomeStatementHistory"+q]["incomeStatementHistory"][0]["netIncome"]["raw"] / json.loads(incomeStatementHistoryQuarterly.text)["quoteSummary"]["result"][0]["incomeStatementHistory"+q]["incomeStatementHistory"][1]["netIncome"]["raw"]
        peg = cap / e / gr / 100
        #print(gp, cap, i)
        if peg < 0:
            data_m.append(peg)
        else:
            data_p.append(peg)
        multiplicators[i] = peg
    print(multiplicators)
    #(pd.DataFrame(data=multi_list, index=[0]).T).to_excel('4-gp.xlsx')
    #print(avg_a, avg_std)
    for i in multiplicators:
        if multiplicators[i] < 0:
            if multiplicators[i] > np.quantile(data_m, q1) and multiplicators[i] < np.quantile(data_m, q3):
                avg_m.append(multiplicators[i])
            elif len(data_m) < 4:
                avg_m = data_m
        else:
            if multiplicators[i] > np.quantile(data_p, q1) and multiplicators[i] < np.quantile(data_p, q3):
                avg_p.append(multiplicators[i])
            elif len(data_p) < 4:
                avg_p = data_p
    mean_p = np.mean(avg_p)
    mean_m = np.mean(avg_m)
    print(np.median(avg_p), np.median(avg_m))
    print(mean_p, mean_m)
    for i in multiplicators:
        if multiplicators[i] < 0:
            multi_list[i] = mean_m / multiplicators[i] * (-1)
        else:
            multi_list[i] = mean_p / multiplicators[i]
    #(pd.DataFrame(data=multi_list, index=[0]).T).to_excel('4.xlsx')
    return [multi_list, multiplicators]

def p_fcf():
    print("fcf     now")
    multi_list = {}
    multiplicators = {}
    data_p = []
    data_m = []
    avg_p = []
    avg_m = []
    for i in symbol_list:
        cap = cap_list[i]
        financialData = requests.get("https://query1.finance.yahoo.com/v10/finance/quoteSummary/"+ i +"?modules=financialData", cookies=cookies, headers=headers)
        #print(i)
        fcf = json.loads(financialData.text)["quoteSummary"]["result"][0]["financialData"]["freeCashflow"]["raw"]
        p_fcf = cap / fcf
        #print(gp, cap, i)
        if p_fcf < 0:
            data_m.append(p_fcf)
        else:
            data_p.append(p_fcf)
        multiplicators[i] = p_fcf
    print(multiplicators)
    #(pd.DataFrame(data=multi_list, index=[0]).T).to_excel('4-gp.xlsx')
    #print(avg_a, avg_std)
    for i in multiplicators:
        if multiplicators[i] < 0:
            if multiplicators[i] > np.quantile(data_m, q1) and multiplicators[i] < np.quantile(data_m, q3):
                avg_m.append(multiplicators[i])
            elif len(data_m) < 2:
                avg_m = data_m[0]
        else:
            if multiplicators[i] > np.quantile(data_p, q1) and multiplicators[i] < np.quantile(data_p, q3):
                avg_p.append(multiplicators[i])
            elif len(data_p) < 2:
                avg_p = data_p[0]
    mean_p = np.mean(avg_p)
    mean_m = np.mean(avg_m)
    print(np.median(avg_p), np.median(avg_m))
    print(mean_p, mean_m)
    for i in multiplicators:
        if multiplicators[i] < 0:
            multi_list[i] = mean_m / multiplicators[i] * (-1)
        else:
            multi_list[i] = mean_p / multiplicators[i]
    #(pd.DataFrame(data=multi_list, index=[0]).T).to_excel('4.xlsx')
    return [multi_list, multiplicators]


#marginal
def roa():
    print("roa")
    multi_list = {}
    multiplicators = {}
    data_p = []
    data_m = []
    avg_p = []
    avg_m = []
    for i in symbol_list:
        incomeStatementHistoryQuarterly = requests.get("https://query1.finance.yahoo.com/v10/finance/quoteSummary/" + i + "?modules=incomeStatementHistory"+q, cookies=cookies, headers=headers)
        e = json.loads(incomeStatementHistoryQuarterly.text)["quoteSummary"]["result"][0]["incomeStatementHistory"+q]["incomeStatementHistory"][0]["netIncome"]["raw"]
        # print(i)
        balanceSheetHistoryQuarterly = requests.get("https://query1.finance.yahoo.com/v10/finance/quoteSummary/"+ i +"?modules=balanceSheetHistory"+q, cookies=cookies, headers=headers)
        a = json.loads(balanceSheetHistoryQuarterly.text)["quoteSummary"]["result"][0]["balanceSheetHistory"+q]["balanceSheetStatements"][0]["totalAssets"]["raw"]
        roa = e / a
        # print(gp, cap, i)
        if roa < 0:
            data_m.append(roa)
        else:
            data_p.append(roa)
        multiplicators[i] = roa
    print(multiplicators)
    # (pd.DataFrame(data=multi_list, index=[0]).T).to_excel('4-gp.xlsx')
    # print(avg_a, avg_std)
    for i in multiplicators:
        if multiplicators[i] < 0:
            if multiplicators[i] > np.quantile(data_m, q1) and multiplicators[i] < np.quantile(data_m, q3):
                avg_m.append(multiplicators[i])
            elif len(data_m) < 2:
                avg_m = data_m[0]
        else:
            if multiplicators[i] > np.quantile(data_p, q1) and multiplicators[i] < np.quantile(data_p, q3):
                avg_p.append(multiplicators[i])
            elif len(data_p) < 2:
                avg_p = data_p[0]
    mean_p = np.mean(avg_p)
    mean_m = np.mean(avg_m)
    print(np.median(avg_p), np.median(avg_m))
    print(mean_p, mean_m)
    for i in multiplicators:
        if multiplicators[i] < 0:
            multi_list[i] = multiplicators[i] / mean_m * (-1)
        else:
            multi_list[i] = multiplicators[i] / mean_p
    # (pd.DataFrame(data=multi_list, index=[0]).T).to_excel('4.xlsx')
    return [multi_list, multiplicators]
def roe():
    print("roe")
    multi_list = {}
    multiplicators = {}
    data_p = []
    data_m = []
    avg_p = []
    avg_m = []
    for i in symbol_list:
        incomeStatementHistoryQuarterly = requests.get("https://query1.finance.yahoo.com/v10/finance/quoteSummary/" + i + "?modules=incomeStatementHistory"+q, cookies=cookies, headers=headers)
        e = json.loads(incomeStatementHistoryQuarterly.text)["quoteSummary"]["result"][0]["incomeStatementHistory"+q]["incomeStatementHistory"][0]["netIncome"]["raw"]
        # print(i)
        balanceSheetHistoryQuarterly = requests.get("https://query1.finance.yahoo.com/v10/finance/quoteSummary/"+ i +"?modules=balanceSheetHistory"+q, cookies=cookies, headers=headers)
        eq = json.loads(balanceSheetHistoryQuarterly.text)["quoteSummary"]["result"][0]["balanceSheetHistory"+q]["balanceSheetStatements"][0]["totalAssets"]["raw"] - json.loads(balanceSheetHistoryQuarterly.text)["quoteSummary"]["result"][0]["balanceSheetHistory"+q]["balanceSheetStatements"][0]["totalLiab"]["raw"]
        roa = e / eq
        # print(gp, cap, i)
        if roa < 0:
            data_m.append(roa)
        else:
            data_p.append(roa)
        multiplicators[i] = roa
    print(multiplicators)
    # (pd.DataFrame(data=multi_list, index=[0]).T).to_excel('4-gp.xlsx')
    # print(avg_a, avg_std)
    for i in multiplicators:
        if multiplicators[i] < 0:
            if multiplicators[i] > np.quantile(data_m, q1) and multiplicators[i] < np.quantile(data_m, q3):
                avg_m.append(multiplicators[i])
            elif len(data_m) < 2:
                avg_m = data_m[0]
        else:
            if multiplicators[i] > np.quantile(data_p, q1) and multiplicators[i] < np.quantile(data_p, q3):
                avg_p.append(multiplicators[i])
            elif len(data_p) < 2:
                avg_p = data_p[0]
    mean_p = np.mean(avg_p)
    mean_m = np.mean(avg_m)
    print(np.median(avg_p), np.median(avg_m))
    print(mean_p, mean_m)
    for i in multiplicators:
        if multiplicators[i] < 0:
            multi_list[i] = multiplicators[i] / mean_m * (-1)
        else:
            multi_list[i] = multiplicators[i] / mean_p
    # (pd.DataFrame(data=multi_list, index=[0]).T).to_excel('4.xlsx')
    return [multi_list, multiplicators]
def oper_marg():
    print("oper_marg")
    multiplicators = {}
    multi_list = {}
    data = []
    avg = []
    for i in symbol_list:
        financialData = requests.get("https://query1.finance.yahoo.com/v10/finance/quoteSummary/" + i + "?modules=financialData", cookies=cookies, headers=headers)
        # print(i)
        oper_marg = json.loads(financialData.text)["quoteSummary"]["result"][0]["financialData"]["operatingMargins"]["raw"]
        data.append(oper_marg)
        multiplicators[i] = oper_marg
    print(multiplicators)
    #(pd.DataFrame(data=multi_list, index=[0]).T).to_excel('1-gp.xlsx')
    #print(avg_a, avg_std)
    for i in multiplicators:
        if multiplicators[i] > np.quantile(data, q1) and multiplicators[i] < np.quantile(data, q3):
            avg.append(multiplicators[i])
    mean = np.mean(avg)
    print(np.median(avg))
    print(mean)
    for i in multiplicators:
        multi_list[i] = multiplicators[i] / mean
    #(pd.DataFrame(data=multi_list, index=[0]).T).to_excel('1.xlsx')
    return [multi_list, multiplicators]
def gross_marg():
    print("oper_marg")
    multiplicators = {}
    multi_list = {}
    data = []
    avg = []
    for i in symbol_list:
        financialData = requests.get("https://query1.finance.yahoo.com/v10/finance/quoteSummary/" + i + "?modules=financialData", cookies=cookies, headers=headers)
        # print(i)
        gross_marg = json.loads(financialData.text)["quoteSummary"]["result"][0]["financialData"]["grossMargins"]["raw"]
        data.append(gross_marg)
        multiplicators[i] = gross_marg
    print(multiplicators)
    #(pd.DataFrame(data=multi_list, index=[0]).T).to_excel('1-gp.xlsx')
    #print(avg_a, avg_std)
    for i in multiplicators:
        if multiplicators[i] > np.quantile(data, q1) and multiplicators[i] < np.quantile(data, q3):
            avg.append(multiplicators[i])
    mean = np.mean(avg)
    print(np.median(avg))
    print(mean)
    for i in multiplicators:
        multi_list[i] = multiplicators[i] / mean
    #(pd.DataFrame(data=multi_list, index=[0]).T).to_excel('1.xlsx')
    return [multi_list, multiplicators]
def prof_marg():
    print("prof_marg")
    multiplicators = {}
    multi_list = {}
    data = []
    avg = []
    for i in symbol_list:
        financialData = requests.get("https://query1.finance.yahoo.com/v10/finance/quoteSummary/" + i + "?modules=financialData", cookies=cookies, headers=headers)
        # print(i)
        prof_marg = json.loads(financialData.text)["quoteSummary"]["result"][0]["financialData"]["profitMargins"]["raw"]
        data.append(prof_marg)
        multiplicators[i] = prof_marg
    print(multiplicators)
    #(pd.DataFrame(data=multi_list, index=[0]).T).to_excel('1-gp.xlsx')
    #print(avg_a, avg_std)
    for i in multiplicators:
        if multiplicators[i] > np.quantile(data, q1) and multiplicators[i] < np.quantile(data, q3):
            avg.append(multiplicators[i])
    mean = np.mean(avg)
    print(np.median(avg))
    print(mean)
    for i in multiplicators:
        multi_list[i] = multiplicators[i] / mean
    #(pd.DataFrame(data=multi_list, index=[0]).T).to_excel('1.xlsx')
    return [multi_list, multiplicators]
def roi():
    print("roi")
    multi_list = {}
    multiplicators = {}
    data_p = []
    data_m = []
    avg_p = []
    avg_m = []
    for i in symbol_list:
        incomeStatementHistoryQuarterly = requests.get("https://query1.finance.yahoo.com/v10/finance/quoteSummary/" + i + "?modules=incomeStatementHistory"+q, cookies=cookies, headers=headers)
        e = json.loads(incomeStatementHistoryQuarterly.text)["quoteSummary"]["result"][0]["incomeStatementHistory"+q]["incomeStatementHistory"][0]["netIncome"]["raw"]
        # print(i)
        balanceSheetHistoryQuarterly = requests.get("https://query1.finance.yahoo.com/v10/finance/quoteSummary/"+ i +"?modules=cashflowStatementHistory"+q, cookies=cookies, headers=headers)
        capex = json.loads(balanceSheetHistoryQuarterly.text)["quoteSummary"]["result"][0]["cashflowStatementHistory"+q]["cashflowStatements"][0]["totalCashflowsFromInvestingActivities"]["raw"] * (-1)
        roi = e / capex
        # print(gp, cap, i)
        if roi < 0:
            data_m.append(roi)
        else:
            data_p.append(roi)
        multiplicators[i] = roi
    print(multiplicators)
    # (pd.DataFrame(data=multi_list, index=[0]).T).to_excel('4-gp.xlsx')
    # print(avg_a, avg_std)
    for i in multiplicators:
        if multiplicators[i] < 0:
            if multiplicators[i] > np.quantile(data_m, q1) and multiplicators[i] < np.quantile(data_m, q3):
                avg_m.append(multiplicators[i])
            elif len(data_m) < 2:
                avg_m = data_m[0]
        else:
            if multiplicators[i] > np.quantile(data_p, q1) and multiplicators[i] < np.quantile(data_p, q3):
                avg_p.append(multiplicators[i])
            elif len(data_p) < 2:
                avg_p = data_p[0]
    mean_p = np.mean(avg_p)
    mean_m = np.mean(avg_m)
    print(np.median(avg_p), np.median(avg_m))
    print(mean_p, mean_m)
    for i in multiplicators:
        if multiplicators[i] < 0:
            multi_list[i] = multiplicators[i] / mean_m * (-1)
        else:
            multi_list[i] = multiplicators[i] / mean_p
    # (pd.DataFrame(data=multi_list, index=[0]).T).to_excel('4.xlsx')
    return [multi_list, multiplicators]

def sum_rang(l, name):
    super_list = {}
    print(symbol_list)
    multi_list = {}
    multiplicators = {}
    for i in symbol_list:
        sum_symbol = 0
        all_symbols = []
        for n in l:
            #print(i, n)
            sum_symbol += n[0][i]
            #print(n[1][i])
            all_symbols.append(n[1][i])
            all_symbols.append(n[0][i])
            #print(all_symbols)
        all_symbols.append(sum_symbol)
        #print(all_symbols)
        super_list[i] = all_symbols
        #multi_list[i] = sum_symbol
    #print('ok')
    #return (pd.DataFrame(data=super_list, columns=["p_gp", "score", "p_gp", "score", "p_gp", "score", "p_gp", "score", "p_gp", "score", "p_gp", "score", "p_gp", "score", "p_gp", "score", "p_gp", "score", "p_gp", "score", "p_gp", "score", "p_gp", "score"]).T).to_excel(name + '.xlsx')
    print(pd.DataFrame(data=super_list))
    return (pd.DataFrame(data=super_list).T).to_excel(name + '.xlsx')
def ev_s():
    print("ev_s")
    multi_list = {}
    multiplicators = {}
    data_p = []
    data_m = []
    avg_p = []
    avg_m = []
    for i in symbol_list:
        incomeStatementHistoryQuarterly = requests.get("https://query1.finance.yahoo.com/v10/finance/quoteSummary/" + i + "?modules=incomeStatementHistory"+q, cookies=cookies, headers=headers)
        s = json.loads(incomeStatementHistoryQuarterly.text)["quoteSummary"]["result"][0]["incomeStatementHistory"+q]["incomeStatementHistory"][0]["totalRevenue"]["raw"]
        # print(i)
        defaultKeyStatistics = requests.get("https://query1.finance.yahoo.com/v10/finance/quoteSummary/"+ i +"?modules=defaultKeyStatistics", cookies=cookies, headers=headers)
        ev = json.loads(defaultKeyStatistics.text)["quoteSummary"]["result"][0]["defaultKeyStatistics"]["enterpriseValue"]["raw"]
        ev_s = ev / s
        # print(gp, cap, i)
        if ev_s < 0:
            data_m.append(ev_s)
        else:
            data_p.append(ev_s)
        multiplicators[i] = ev_s
    print(multiplicators)
    # (pd.DataFrame(data=multi_list, index=[0]).T).to_excel('4-gp.xlsx')
    # print(avg_a, avg_std)
    for i in multiplicators:
        if multiplicators[i] < 0:
            if multiplicators[i] > np.quantile(data_m, q1) and multiplicators[i] < np.quantile(data_m, q3):
                avg_m.append(multiplicators[i])
            elif len(data_m) < 2:
                avg_m = data_m[0]
        else:
            if multiplicators[i] > np.quantile(data_p, q1) and multiplicators[i] < np.quantile(data_p, q3):
                avg_p.append(multiplicators[i])
            elif len(data_p) < 2:
                avg_p = data_p[0]
    mean_p = np.mean(avg_p)
    mean_m = np.mean(avg_m)
    print(np.median(avg_p), np.median(avg_m))
    print(mean_p, mean_m)
    for i in multiplicators:
        if multiplicators[i] < 0:
            multi_list[i] = mean_m / multiplicators[i] * (-1)
        else:
            multi_list[i] = mean_p / multiplicators[i]
    # (pd.DataFrame(data=multi_list, index=[0]).T).to_excel('4.xlsx')
    return [multi_list, multiplicators]
def deb_ass():
    print("deb_ass")
    multiplicators = {}
    multi_list = {}
    data = []
    avg = []
    for i in symbol_list:
        balanceSheetHistoryQuarterly = requests.get("https://query1.finance.yahoo.com/v10/finance/quoteSummary/" + i + "?modules=balanceSheetHistory" + q,cookies=cookies, headers=headers)
        # print(i)

        ass = json.loads(balanceSheetHistoryQuarterly.text)["quoteSummary"]["result"][0]["balanceSheetHistory" + q]["balanceSheetStatements"][0]["totalAssets"]["raw"]
        deb = json.loads(balanceSheetHistoryQuarterly.text)["quoteSummary"]["result"][0]["balanceSheetHistory" + q]["balanceSheetStatements"][0]["totalLiab"]["raw"]
        deb_ass = deb / ass
        data.append(deb_ass)
        multiplicators[i] = deb_ass
        print(deb_ass)
    print(multiplicators)
    #(pd.DataFrame(data=multi_list, index=[0]).T).to_excel('1-gp.xlsx')
    #print(avg_a, avg_std)
    for i in multiplicators:
        if multiplicators[i] > np.quantile(data, q1) and multiplicators[i] < np.quantile(data, q3):
            avg.append(multiplicators[i])
    mean = np.mean(avg)
    print(np.median(avg))
    print(mean)
    for i in multiplicators:
        multi_list[i] = mean / multiplicators[i]
    #(pd.DataFrame(data=multi_list, index=[0]).T).to_excel('1.xlsx')
    return [multi_list, multiplicators]
def quickRatio():
    print("quickRatio")
    multiplicators = {}
    multi_list = {}
    data = []
    avg = []
    for i in symbol_list:
        financialData = requests.get("https://query1.finance.yahoo.com/v10/finance/quoteSummary/" + i + "?modules=financialData", cookies=cookies, headers=headers)
        # print(i)

        qr = json.loads(financialData.text)["quoteSummary"]["result"][0]["financialData"]["quickRatio"]["raw"]
        data.append(qr)
        multiplicators[i] = qr
    print(multiplicators)
    #(pd.DataFrame(data=multi_list, index=[0]).T).to_excel('1-gp.xlsx')
    #print(avg_a, avg_std)
    for i in multiplicators:
        if multiplicators[i] > np.quantile(data, q1) and multiplicators[i] < np.quantile(data, q3):
            avg.append(multiplicators[i])
    mean = np.mean(avg)
    print(np.median(avg))
    print(mean)
    for i in multiplicators:
        multi_list[i] = mean / multiplicators[i]
    #(pd.DataFrame(data=multi_list, index=[0]).T).to_excel('1.xlsx')
    return [multi_list, multiplicators]
def currentRatio():
    print("currentRatio")
    multiplicators = {}
    multi_list = {}
    data = []
    avg = []
    for i in symbol_list:
        financialData = requests.get("https://query1.finance.yahoo.com/v10/finance/quoteSummary/" + i + "?modules=financialData", cookies=cookies, headers=headers)
        # print(i)

        cr = json.loads(financialData.text)["quoteSummary"]["result"][0]["financialData"]["quickRatio"]["raw"]
        data.append(cr)
        multiplicators[i] = cr
    print(multiplicators)
    #(pd.DataFrame(data=multi_list, index=[0]).T).to_excel('1-gp.xlsx')
    #print(avg_a, avg_std)
    for i in multiplicators:
        if multiplicators[i] > np.quantile(data, q1) and multiplicators[i] < np.quantile(data, q3):
            avg.append(multiplicators[i])
    mean = np.mean(avg)
    print(np.median(avg))
    print(mean)
    for i in multiplicators:
        multi_list[i] = mean / multiplicators[i]
    #(pd.DataFrame(data=multi_list, index=[0]).T).to_excel('1.xlsx')
    return [multi_list, multiplicators]

print(p_e())
print(p_e1())

#print(quickRatio(), currentRatio())
#print(errors)
print(sum_rang([p_gp(), p_s(), p_b(), p_e(), peg(), p_fcf(), prof_marg(), oper_marg(), gross_marg(), roe(), roa(), ev_s(), deb_ass(), quickRatio(), currentRatio()], "prices"))