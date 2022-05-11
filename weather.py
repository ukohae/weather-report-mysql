import requests
import json
import mysql.connector

def write_data_to_db(username, password, host, file_name):
    print("Writing data to database...")
    db = input("Enter a Database you want data written to: ")
    mydb = mysql.connector.connect(
        user=username, 
        password=password,
        host=host
    )
    mycursor = mydb.cursor()
    try: 
        mycursor.execute("CREATE DATABASE {}".format(db))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)
    mycursor.execute("USE {}".format(db))
    mycursor.execute("CREATE TABLE locations (name VARCHAR(255), temp VARCHAR(255), country VARCHAR(255), weather_desc VARCHAR(255))")

    with open(file_name, 'r') as file:
        print("Pulling current weather information from {} \n".format(file_name))
        data = json.load(file)

    print("Saving the following data in the database")
    for info in data:
        print("name:", info['name'], end="\t")
        print('temp:', info['main']['temp'], end="\t")
        print('country:', info['sys']['country'], end="\t")
        print('weather_desc:', info['weather'][0]['description'])
        print()

        insert = "INSERT INTO locations (name, temp, country, weather_desc) VALUES (%s, %s, %s, %s)"
        val = (info['name'], info['main']['temp'], info['sys']['country'], info['weather'][0]['description'])
        mycursor.execute(insert, val)

    mydb.commit()
    print("Successfully saved all data to the {} database \n".format(db))

def show_data_from_db(username, password, host_ip):
    db = input("Enter a Database to display all data: ")
    mydb = mysql.connector.connect(
        user=username, 
        password=password,
        host=host_ip,
        database=db
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * from locations")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)
 
def fetch_weather_report(file_name):
    api_key = "3cb067f899a8c989f711fbb5e9444c3c"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    locations = []
    position = ['First', 'Second', 'Third']

    for i in position:
        city_name = input("Enter {} city name to get weather information: ".format(i))

        complete_url = base_url + "appid=" + api_key + "&q=" + city_name

        response = requests.get(complete_url)

        locations.append(response.json())

    with open(file_name, "w") as file:
        file.write(json.dumps(locations))

def main():
    file = 'configuration.json'
    user='emmanuel'
    password='101Ginger!'  
    host='127.0.0.1'

    fetch_weather_report(file)

    write_data_to_db(user, password, host, file)
    
    read_db = (input('Do you wish to read data from the database[Y / N]: ')).lower()
    if(read_db == 'yes' or read_db == 'y'):
        show_data_from_db(user, password, host)

main()