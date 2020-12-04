from bs4 import BeautifulSoup
import pandas as pm25_df


def get_pm25_df(html_path):
    with open(html_path,encoding="utf-8") as html_file:
        soup = BeautifulSoup(html_file,"html.parser")
    pm25_df = pd.DataFrame(columns=["hour","pm25_value_max","pm25_value_min"])
    container_tag = soup.find_all("div",{"class":"whitebody"})[0]
    parent_tag = container_tag.center.div.find("div",{"class":"forecast-body"}).find("div",{"class":"forecast-body-table"}).table
    list_of_pm25 = parent_tag.find("tr",{"class":"wf-row-pm25"}).find_all("td")[1:]
    hour = 0
    for each_point in list_of_pm25:
        try:
            this_hour = hour
            max_pm25 = int(each_point.div.find("div",{"class":"wf-cell-aqi-val-max"}).text)
            min_pm25 = int(each_point.div.find("div",{"class":"wf-cell-aqi-val-min"}).text)
            pm25_df = pm25_df.append({"hour":this_hour,"pm25_value_max":max_pm25,"pm25_value_min":min_pm25}, ignore_index=True)
            hour += 3
            hour = hour % 24
        except:
            print("this one dose not contain info")
    return pm25_df


def get_windspeed_df(html_path):
    with open(html_path,encoding="utf-8") as html_file:
        soup = BeautifulSoup(html_file,"html.parser")
    wind_speed_df = pd.DataFrame(columns=["hour","wind_speed"])
    container_tag = soup.find_all("div",{"class":"whitebody"})[0]
    parent_tag = container_tag.center.div.find("div",{"class":"forecast-body"}).find("div",{"class":"forecast-body-table"}).table
    list_of_windspeed = parent_tag.find("tr",{"class":"wf-row-wind"}).find_all("td")[1:]
    hour = 0
    for each_point in list_of_windspeed:
        try:
            this_hour = hour
            wind_speed = int(each_point.svg.find("text").text)
            wind_speed_df = wind_speed_df.append({"hour":this_hour,"wind_speed":wind_speed}, ignore_index=True)
            hour += 3
            hour = hour % 24
        except:
            print("this one dose not contain info")
    return wind_speed_df


def get_winddir_df(html_path):
    with open(html_path,encoding="utf-8") as html_file:
        soup = BeautifulSoup(html_file,"html.parser")
    wind_dir_df = pd.DataFrame(columns=["hour","wind_direction"])
    container_tag = soup.find_all("div",{"class":"whitebody"})[0]
    parent_tag = container_tag.center.div.find("div",{"class":"forecast-body"}).find("div",{"class":"forecast-body-table"}).table
    list_of_winddir = parent_tag.find("tr",{"class":"wf-row-winddir"}).find_all("td")[1:]
    hour = 0
    for each_point in list_of_winddir:
        try:
            this_hour = hour
            wind_dir_text = each_point.svg.line["transform"][7:12]
            wind_dir_ret = re.search(r"\d+\.\d",wind_dir_text)[0]
            wind_dir_df = wind_dir_df.append({"hour":this_hour,"wind_direction":wind_dir_ret}, ignore_index=True)
            hour += 3
            hour = hour % 24
        except:
            print("this one dose not contain info")
    return wind_dir_df
