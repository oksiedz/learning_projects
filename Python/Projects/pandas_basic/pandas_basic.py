import csv
import pandas

READ_MODE = "r"
WEATHER_DATA_FILE_PATH = "weather_data.csv"
HEADER_FOR_TEMPERATURE = "temp"
SQUIRREL_CSV = "Squirels/2018_Central_Park_Squirrel_Census_-_Squirrel_Data_20240328.csv"
FUR_COLOUR = "Primary Fur Color"



# opening file and reading it with simple approach
with open(file=WEATHER_DATA_FILE_PATH, mode=READ_MODE) as weather_data_file:
    weather_data = weather_data_file.readlines()
    print(weather_data)

# opening file and reading it with csv package
with open(WEATHER_DATA_FILE_PATH) as data_file:
    data = csv.reader(data_file)  # creation of CSV data object
    temperatures = []
    for row in data:
        if row[1] != HEADER_FOR_TEMPERATURE:  # there is also header
            temperatures.append(int(row[1]))
    print(temperatures)

# opening file with pandas
pandas_data = pandas.read_csv(filepath_or_buffer=WEATHER_DATA_FILE_PATH)
print(pandas_data)
# printing only selected columns
print(pandas_data[HEADER_FOR_TEMPERATURE])
print(type(pandas_data))
print(type(pandas_data[HEADER_FOR_TEMPERATURE]))

pandas_data_dictionary = pandas_data.to_dict()
print(pandas_data_dictionary)

temperature_list = pandas_data[HEADER_FOR_TEMPERATURE].to_list()
print(temperature_list)
average_temperature = sum(temperature_list) / len(temperature_list)
print(f"Average temperature equals: {average_temperature}")
average_temperature2 = pandas_data[HEADER_FOR_TEMPERATURE].mean()
maximum_temperature = pandas_data[HEADER_FOR_TEMPERATURE].max()  # could be called also as pandas_data.temp
print(f"Average temperature equals: {average_temperature2}, maximum temperature equals: {maximum_temperature}")

# getting row of data
print(pandas_data[pandas_data.day == "Monday"])  # returning number of row where day is Monday

row_of_week_with_maximum_temp = pandas_data[pandas_data.temp == maximum_temperature]
print(row_of_week_with_maximum_temp)
day_of_week_with_maximum_temp = row_of_week_with_maximum_temp["day"]
print(f"Maximum temperature of {maximum_temperature} was noted on {day_of_week_with_maximum_temp}")

# how to create data frame
data_dict = {
    "students": ["Amy", "James", "Bob"],
    "scores": [73, 35, 69]
}
pandas_data_from_dictionary = pandas.DataFrame(data_dict)
print(pandas_data_from_dictionary)
pandas_data_from_dictionary.to_csv("new_data.csv")

# ######################################################### #
# ######################################################### #
# Squirrel analysis
# ######################################################### #
# ######################################################### #


squirrel_data_set = pandas.read_csv(filepath_or_buffer=SQUIRREL_CSV)
# print(squirrel_data_set.keys())  # printing the headers
print(squirrel_data_set[FUR_COLOUR].value_counts())
