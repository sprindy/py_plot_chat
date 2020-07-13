import matplotlib.pyplot as plt
import pandas as pd
import re
import time

import sys   
#reload(sys)   
#sys.setdefaultencoding('utf8')   

plt.rcParams['font.sans-serif'] = ['SimHei'] # for Chinese lable
plt.rcParams['axes.unicode_minus'] = False # for Chinese -

filename = 'chat_log.txt'
saints_excel_name = 'saints.xlsx'
data_str = '2020-\d-\d'
data_str2 = '2020-\d-\d\d'
time_str = '\d\d:\d\d'
plan_date_str = '2020\d\d\d\d'
saint_name_list = ['Anna', 'Carol', 'Figo', 'Grace', 'Jerry', 'Leon', 'Linda', 'Mandy', 'Siyuan', 'Sprindy']
saint_alias_list = ['Anna', 'Carol', 'WOW-LOL', 'GraceXu', 'blue sky', 'Leon', 'linda', 'Mandy', '周森森', 'Sprindy']

name_lists_by_time = [ [] for i in range(24)]
header = ['real_date', 'real_time', 'alias', 'plan_date', 'saint']
saint_daily_record = header
study_data = pd.DataFrame(columns=header)

def search_and_save_data_to_excel():
    # flags for logic control
    is_real_date_found = False
    is_real_time_found = False
    is_plan_date_found = False
    is_the_saint_found = False

    with open(filename, 'r', encoding='utf8') as f:
        lines = f.readlines()
        line = f.readline()
        for line in lines:
            #value = [float(s) for s in line.split()]#4
            m = re.search(data_str, line)
            if m is not None:
                is_real_date_found = True
                # real_date
                n = re.search(data_str2, line)
                if n is not None:
                    saint_daily_record[0] = n.group()
                else:
                    saint_daily_record[0] = m.group()

            m = re.search(time_str, line)
            if m is not None:
                is_real_time_found = True
                # alias
                saint_daily_record[1] = m.group()
                # real_time
                for i in range(len(saint_name_list)):
                    m = re.search(saint_alias_list[i], line, re.I)
                    if m is not None:
                        saint_daily_record[2] = m.group()
                        # print(saint_daily_record)

            m = re.search(plan_date_str, line)
            if m is not None:
                is_plan_date_found = True
                # plan_date
                saint_daily_record[3] = m.group()

            if (is_real_time_found and is_plan_date_found):
                for i in range(len(saint_name_list)):
                    m = re.search(saint_name_list[i], line, re.I)
                    if m is not None:
                        if (saint_daily_record[2] == saint_alias_list[i]):
                            # print(m.group())
                            # print(saint_alias_list[i])
                            is_the_saint_found = True
                            saint_daily_record[4] = m.group()

            # all found, clear for the next saint
            if (is_plan_date_found and is_the_saint_found):
                study_data.loc[len(study_data)] = saint_daily_record
                is_plan_date_found = False
                is_real_date_found = False
                is_the_saint_found = False

    print(study_data)
    # save DataFrame to excel file
    study_data.to_excel(saints_excel_name)

# Main Entry
def main(args):
    search_and_save_data_to_excel()

if __name__ == '__main__':
  main(sys.argv)