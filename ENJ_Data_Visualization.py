
def Convert_to_JSON(list_of_salary_data):
    import csv
    import json
    salary_json={}; work_json={}

    # 1. Save the salary data in json
    for file_name in list_of_salary_data:
        salary_json[file_name]={}

        # Open CSV file
        excel_name = "".join([file_name, ".csv"])
        with open(excel_name, encoding='utf-8-sig') as csv_file:
            csv_reader  = csv.reader(csv_file, delimiter=',')
            inputs = [row for row in csv.reader(csv_file)]
            
        # Read the data
        for i in range(1,len(inputs)):
            if inputs[i][1] != '':
                salary_json[file_name][inputs[i][1].strip()]={}
                
                for j in range(6,len(inputs[i])):
                    try:
                        salary_json[file_name][inputs[i][1].strip()][inputs[0][j].strip()] = float(inputs[i][j])     
                    except:
                        salary_json[file_name][inputs[i][1].strip()][inputs[0][j].strip()] = 0     
            else:
                break
            
    # 2. Generate JSON intance
    with open('salary_data.json', 'w', encoding='utf-8') as f:
        json.dump(salary_json, f, ensure_ascii=False, indent=4)


class ENJ_Data_Visualization:
    """
        The company has a lot of employees, and its employee's data is saved in Excel files.
        However, the problem was that it was challenging to know whether the salary was paid correctly
        considering the work hours and whether the salary was paid fairly between the employees.
        Thus, this code was developed to visualize employees' salary in given months.
        Once the starting/ending year, month, and name are input, the code visualizes aggregated salaries in a bar graph and work hour table.

        Parameters:
        self.Year_Start: integer
                    Starting Year (e.g., 2020).
                    
        Month_Start: str,
                     Starting Month (e.g., Feb).
                     
        Year_End:    integer,
                     Ending Year (e.g., 2021).
                   
        Month_End:   integer,
                     Ending Month (e.g., Sep)

        Name:        str,
                     Employee name(s).
         
    """

    def __init__(self, Year_Start, Month_Start, Year_End, Month_End, *Name):
              
        self.Year_Start  = Year_Start
        self.Month_Start = Month_Start
        self.Year_End    = Year_End
        self.Month_End   = Month_End
        self.Name        = Name

        self.list_of_month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        
        # 1. Examine arguments
        if isinstance(self.Year_Start, int) == False or isinstance(self.Year_End, int) == False:
            raise Exception("Year_Start and Year_End must be an integer type.")

        if self.Year_Start < 2019 or self.Year_End > 2021:
            raise Exception("Year_Start or Year_End isn't included in the min/max boundary.")
        
        if self.Year_Start + self.list_of_month.index(self.Month_Start)/12 > self.Year_End + self.list_of_month.index(self.Month_End)/12:
            raise Exception("Year_End and Month_End must be later than Year_Start and self.Month_Start.")
        
        if self.Month_Start not in self.list_of_month or self.Month_End not in self.list_of_month:
            raise Exception("Month_Start or Month_End is not in the correct format.")



    def Read_Data(self):
        import pandas as pd
        import json
         
        data = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0] for i in range(len(self.Name))]
        self.instance_salary_data = pd.DataFrame(data, columns = ["시급", "식비", "자녀보육", "기본급", "미만근자", "상여", "기타수당", "성과급", "징계(감봉)", "비과세포함", "비과세제외", "국민연금",\
                                                             "건강보험", "장기요양", "고용보험", "산재보험", "퇴직금", "4대보험외", "아웃소싱비", "기숙사", "학자금", "총계"],
                                                   index = [i for i in self.Name])

        loop={}
        tempo_year = self.Year_End - self.Year_Start
        if tempo_year == 0:

            loop[self.Year_End] = [self.list_of_month[i]+1 for i in range(self.list_of_month.index(self.Month_Start), self.list_of_month.index(self.Month_End)+1)]
            
        elif tempo_year == 1:
            loop[self.Year_Start] = []
            loop[self.Year_End]   = []

            for i in range(self.list_of_month.index(self.Month_Start), 12):
                loop[self.Year_Start].append(i+1)
            for i in range(self.list_of_month.index(self.Month_End)):
                loop[self.Year_End].append(i+1)


        # Fetch the necessary data
        with open("salary_data.json") as f:
            self.salary_data = json.load(f)

        for year in loop.keys():
            for month in loop[year]:
                if month < 10:
                        month = "".join(['0', str(month)])
                        
                for name in self.Name:                   
                    tempo = "".join(["급여정산_", str(year), str(month)])
                    
                    self.instance_salary_data.loc[name, "시급"] += self.salary_data[tempo][name]["시급"]
                    self.instance_salary_data.loc[name, "식비"] += self.salary_data[tempo][name]["식비"]
                    self.instance_salary_data.loc[name, "자녀보육"] += self.salary_data[tempo][name]["자녀보육"]
                    self.instance_salary_data.loc[name, "기본급"] += self.salary_data[tempo][name]["기본급"]
                    self.instance_salary_data.loc[name, "미만근자"] += self.salary_data[tempo][name]["미만근자"]
                    try:
                        self.instance_salary_data.loc[name, "상여"] += self.salary_data[tempo][name]["상여"]
                    except:
                        self.instance_salary_data.loc[name, "상여"] += self.salary_data[tempo][name]["상여수당"]
                    self.instance_salary_data.loc[name, "기타수당"] += self.salary_data[tempo][name]["기타수당"]
                    self.instance_salary_data.loc[name, "성과급"] += self.salary_data[tempo][name]["성과급"]
                    self.instance_salary_data.loc[name, "징계(감봉)"] += self.salary_data[tempo][name]["징계(감봉)"]
                    self.instance_salary_data.loc[name, "비과세포함"] += self.salary_data[tempo][name]["비과세포함"]
                    self.instance_salary_data.loc[name, "비과세제외"] += self.salary_data[tempo][name]["비과세제외"]
                    self.instance_salary_data.loc[name, "국민연금"] += self.salary_data[tempo][name]["국민연금"]
                    self.instance_salary_data.loc[name, "건강보험"] += self.salary_data[tempo][name]["건강보험"]
                    self.instance_salary_data.loc[name, "장기요양"] += self.salary_data[tempo][name]["장기요양"]
                    self.instance_salary_data.loc[name, "고용보험"] += self.salary_data[tempo][name]["고용보험"]
                    self.instance_salary_data.loc[name, "산재보험"] += self.salary_data[tempo][name]["산재보험"]
                    self.instance_salary_data.loc[name, "퇴직금"] += self.salary_data[tempo][name]["퇴직금"]
                    self.instance_salary_data.loc[name, "4대보험외"] += self.salary_data[tempo][name]["4대보험외"]
                    self.instance_salary_data.loc[name, "아웃소싱비"] += self.salary_data[tempo][name]["아웃소싱비"]
                    self.instance_salary_data.loc[name, "기숙사"] += self.salary_data[tempo][name]["기숙사"]
                    self.instance_salary_data.loc[name, "학자금"] += self.salary_data[tempo][name]["학자금"]
                    self.instance_salary_data.loc[name, "총계"] += self.salary_data[tempo][name]["총계"]
              

    def Visualize_Empolyees_Data(self):
        import matplotlib.pyplot as plt
        from  matplotlib import ticker
        import pandas as pd
        import numpy as np

        # 3. Visualize the data
        x_axis_name = ["hourly_wage", "food expenses", "child care", "base pay", "part-time wage", "bonus", "other allowances", "merit pay", "pay cut", "taxfree included", "taxfree excluded",
                       "401k", "health insurance", "longterm care", "employment insurance", "compensation insurance", "severance pay", "4 major insurance fee", "outsourcing fee", "dormitory fee", "student funds", "total"]

        tempo_Name = ("James", "Lucas", "Noah")       
        tempo_data={}; df={}
        i=0
        for name in self.Name:
            tempo_data[tempo_Name[i]]={}
            tempo_data[tempo_Name[i]]=self.instance_salary_data.loc[name].to_numpy()
            i+=1
        
        df = pd.DataFrame(tempo_data, index=x_axis_name)
        
        ax = df.plot.bar(rot=0, figsize=(35,30))
        plt.xticks(rotation=50)
        plt.ticklabel_format(axis='y', style='plain')
        ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
        plt.ylabel('South Korean Won [KRW]')
        plt.title(f"Salary from {self.Year_Start} {self.Month_Start} to {self.Year_End} {self.Month_End}")
        plt.legend(loc='upper left')
        plt.show()
        


if __name__ == '__main__':

    salary = ["급여정산_202001","급여정산_202002","급여정산_202003","급여정산_202004","급여정산_202005","급여정산_202006","급여정산_202007","급여정산_202008","급여정산_202009",\
              "급여정산_202010","급여정산_202011","급여정산_202012","급여정산_202101","급여정산_202102","급여정산_202103","급여정산_202104","급여정산_202105","급여정산_202106",\
              "급여정산_202107","급여정산_202108","급여정산_202109"]
    Convert_to_JSON(salary)
    instance = ENJ_Data_Visualization(2020, "Dec", 2021, "Aug", "전순효", "황해든", "김준형")
    instance.Read_Data()
    instance.Visualize_Empolyees_Data()
