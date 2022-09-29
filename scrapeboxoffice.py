import requests
import datetime
from csv import writer
from requests_html import HTML
import pandas as pd


now = datetime.datetime.now()
year = now.year

def url_to_txt(url,filename = "world.html",save = False):
    r = requests.get(url)
    if r.status_code == 200:
        html_txt = r.text
        if save:
            with open(f"world_{year}.html",'w') as f:
                f.write(html_txt)
        return html_txt
    return ""

movie_years = [x for x in range(1977,year+1)]
# print(r.status_code)
url = f"https://www.boxofficemojo.com/year/world/{movie_years[-1]}/"
html_txt = url_to_txt(url)

r_html = HTML(html= html_txt)
table_class = ".imdb-scroll-table-inner"
r_table = r_html.find(table_class)


table_list = []
if len(r_table) == 1:
    # print(r_table[0].text)
    parsed_table = r_table[0]
    rows = parsed_table.find('tr')
    header_row = rows[0]
    header_col = header_row.find("th")
    header_name = [x.text for x in header_col]
    for row in rows[1:]:
        cols = row.find("td")
        row_list = []

        for col in cols:
            row_list.append(col.text)

        table_list.append(row_list)

def create_csv(headrow,tablerow,filename = f'projectfile{movie_years[-1]}.csv'):
    with open(filename,'w',encoding='utf8',newline="") as f:
        thewriter = writer(f)
        thewriter.writerow(headrow)
        for rw in tablerow:
            thewriter.writerow(rw)

def create_csv_pd(headrow,tablerow,filename = 'Boxoffice_projectfile.csv'):
    df = pd.DataFrame(tablerow,columns=headrow)
    df.to_csv(filename,index=False)

def create_excel_pd(headrow,tablerow,filename = 'Boxoffice_projectfile.xlsx'):
    df = pd.DataFrame(tablerow,columns=headrow)
    datatoexcel = pd.ExcelWriter(filename)
    df.to_excel(datatoexcel)
    datatoexcel.save()
# create_csv(headrow=header_name,tablerow=table_list,filename='BoxOffice22_US.csv')
# create_excel_pd(headrow=header_name,tablerow=table_list)
print(header_name) #debug
print(table_list) #for debug