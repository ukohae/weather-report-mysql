import requests
import json
import mysql.connector
from mysql.connector import errorcode


def write_data_to_db(username, password, host, file_name, db):
    try:
        mydb = mysql.connector.connect(
            user=username,
            password=password,
            host=host
        )
        mycursor = mydb.cursor()
        mycursor.execute("CREATE DATABASE {}".format(db))
        mycursor.execute("USE {}".format(db))
        mycursor.execute(
            "CREATE TABLE locations (name VARCHAR(255), temp VARCHAR(255), country VARCHAR(255), weather_desc VARCHAR(255))")

        print("Writing data to database...")

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
            val = (info['name'], info['main']['temp'], info['sys']
                   ['country'], info['weather'][0]['description'])
            mycursor.execute(insert, val)

        mydb.commit()
        print("Successfully saved all data to the {} database \n".format(db))
    except mysql.connector.Error as err:
        print("Failed creating database: The name {} is invalid".format(db))
        database = input("Re-enter a Database: ")
        write_data_to_db(username, password, host, file_name, database)
    except KeyError:
        print("Failed getting data from api")
        exit(1)


def show_data_from_db(username, password, host_ip):
    while True:
        try:
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
        except mysql.connector.ProgrammingError as err:
            if err.errno == errorcode.ER_SYNTAX_ERROR:
                print("Check your syntax!")
            else:
                print("Error: {}".format(err))
            continue
        else:
            break


def fetch_weather_report(file_name):
    def validate_location(location, pos):

        complete_url = base_url + "appid=" + api_key + "&q=" + location
        response = requests.get(complete_url)
        data = response.json()
        if (data['cod'] != '404'):
            locations.append(data)
        else:
            print(data['message'])
            city_name = input("Re-enter {} Location: ".format(pos))
            validate_location(city_name, pos)

    api_key = "3cb067f899a8c989f711fbb5e9444c3c"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    locations = []
    positions = ['First', 'Second', 'Third']

    for position in positions:
        city_name = input(
            "Enter {} Location: ".format(position))
        validate_location(city_name, position)

    with open(file_name, "w") as file:
        file.write(json.dumps(locations))
    print()


def main():
    file = 'configuration.json'
    user = 'root'
    password = '123a'
    host = '127.0.0.1'
    fetch_weather_report(file)

    database = input("Enter a Database you want data written to: ")
    write_data_to_db(user, password, host, file, database)
    read_db = (
        input('Do you wish to read data from the database[Y / N]: ')).lower()
    if(read_db == 'yes' or read_db == 'y'):
        show_data_from_db(user, password, host)


main()
