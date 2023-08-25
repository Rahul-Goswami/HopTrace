import csv

def readcsvfile(filepath):
    """
    Method to read CSV file
    :param filepath [str]: Please pass full valid path to the function parameter
    :return: Header and Data [list]
    """
    # Open the CSV file
    csvfile = open(filepath)
    reader = csv.reader(csvfile)

    # Capture the headers of the CSV file
    header = next(reader)
    # print(f"Header = {header}")

    # Iterate through the CSV content to get every row as a list
    data = list ()
    for rows in reader:
        data.append(rows)
    # print(f"\nData = {type(data[0][0])}")
    # return header and data
    return header, data
