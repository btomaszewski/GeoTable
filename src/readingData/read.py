#Note: Antivirus applications, such as Avast, seem to consider the 
# camlot library as a potential threat. Make sure to label python.exe 
# as an exluded file.
import camelot

from requests import Session

class reading():
    def getTable(file):
        #Ask what page to read
        print("What page do you want to read?")
        numOfPages = input()

        tables = camelot.read_pdf(file, pages = str(numOfPages))

        #Print statements
        print("Total Tables Extracted:", tables.n)

        return tables

    #loop through all of the tables and check if the following 
    # ("County", "Country", "Territory", "Region", "Area", etc.)

    def findAreaType(location):
        if location == "Country":
            return True
        elif location == "County":
            return True
        elif location == "Territory":
            return True
        elif location == "Region":
            return True
        elif location == "Area":
            return True
        else:
            return False

    def findValues(string, startIndex, lenOfValue):
        endIndex = string.find(",", startIndex)
        value = str(string[startIndex+lenOfValue+1:endIndex])
        value = value.split('"')
        return value[1]

    def getGeoNamesData(tables, foundTable, foundColumn, state):
        #Have the code login into the http://api.geonames.org/ website 
        # as "agentp" so they can use the service 

        dictionary = {"Name":[], "Latitude":[], "Longitude":[], "Cases":[], "Percent":[]}
        with Session() as s:
            login_data = {"username":"agentp","password":"GeoguesserF3620#^@)"}
            s.post("http://api.geonames.org/",login_data)
            
            for t in range(len(foundTable)):
                for c in range(len(tables[foundTable[t]].df)):
                    if c > 0:
                        county = tables[foundTable[t]].df[foundColumn[t]][c]
                        home_page = s.get("http://api.geonames.org/geocodeJSON?q={}+{}&username=agentp".format(county, state))
                        latIndex = str(home_page.content).find("lat")
                        longIndex = str(home_page.content).find("lng")
                        adminNameIndex = str(home_page.content).find("adminName2")
                        lat = reading.findValues(str(home_page.content), latIndex, len("lat"))
                        long = reading.findValues(str(home_page.content), longIndex, len("long"))
                        name = reading.findValues(str(home_page.content), adminNameIndex, len("adminName2"))
                        cases = tables[foundTable[t]].df[foundColumn[t]+1][c]
                        percent = tables[foundTable[t]].df[foundColumn[t]+2][c]


                        dictionary["Name"].append(name)
                        dictionary["Latitude"].append(lat)
                        dictionary["Longitude"].append(long)
                        dictionary["Cases"].append(cases)
                        dictionary["Percent"].append(percent)
        return dictionary

    def getDictionary():
        #PDF file
        file = "src\\readingData\\PDFs\\COVID_Data_2.pdf"

        #get the table data
        tableData = reading.getTable(file)

        foundTable = []  #a list of tables that contain the above cases (represented by index)
        foundColumn = []  #a list of columns that contain the above cases (represented by index)
        for x in range(tableData.n):
            split = tableData[x].df[0][0].split("\n")  #split the first cell by "\n"
            for y in range(len(split)):
                if reading.findAreaType(split[y]):  #if a case matches the table and column are recorded (represented as index)
                    foundTable.append(x)
                    foundColumn.append(y)

        #tables[x].df[y][z] where 'x' represents which table to look at (if 
        # multiple tables were found), 'y' represents the column of the table
        # in question, and 'z' represents the row of the table.
        
        #Note: The headers of the table are commonly at index 0. Also the 
        # header can sometimes be all in one cell making index 0 of another 
        # column be empty.
        
        #Note: len() of the tables[x].df gets the number of rows in a table

        #Convert the table to a csv file
        tableData[0].to_csv("test.csv")

        print("Enter the State")
        state = input()

        return reading.getGeoNamesData(tableData, foundTable, foundColumn, state)

    def main():
        reading.getDictionary()

    if __name__ == "__main__":
        main()