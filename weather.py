import requests
import json
import mysql.connector

DB_Name = input(str("Enter a Database: "))
api_key = "3cb067f899a8c989f711fbb5e9444c3c"
base_url = "http://api.openweathermap.org/data/2.5/weather?"
locations = []
position = ['First', 'Second', 'Third']

for i in range(3):
    city_name = input("Enter {} city name : ".format(position[i]))

    complete_url = base_url + "appid=" + api_key + "&q=" + city_name

    response = requests.get(complete_url)

    locations.append(response.json())

file = (json.dumps(locations))

def write_data_to_db(username, password, host):
    mydb = mysql.connector.connect(
        user=username, 
        password=password,
        host=host
    )
    mycursor = mydb.cursor()
    try: 
        mycursor.execute("CREATE DATABASE {}".format(DB_Name))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)
    mycursor.execute("USE {}".format(DB_Name))
    mycursor.execute("CREATE TABLE locations (name VARCHAR(255), temp VARCHAR(255), country VARCHAR(255), weather_desc VARCHAR(255))")
    data = json.loads(file)

    for info in data:
        print()
        print("name:", info['name'])
        print('temp:', info['main']['temp'])
        print('country:', info['sys']['country'])
        print('weather_desc:', info['weather'][0]['description'])

        insert = "INSERT INTO locations (name, temp, country, weather_desc) VALUES (%s, %s, %s, %s)"
        val = (info['name'], info['main']['temp'], info['sys']['country'], info['weather'][0]['description'])
        mycursor.execute(insert, val)
    mydb.commit()
    print("Successfully written to database \n")

def show_data_from_db(username, password, host_ip, db):
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

def main():
    user='emmanuel'
    password='101Ginger!'  
    host='127.0.0.1'
    database=DB_Name
    write_data_to_db(user, password, host)
    show_data_from_db(user, password, host, database)

main()