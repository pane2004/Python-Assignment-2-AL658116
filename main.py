#-----------------------------------------------------------------------------
# Name:        Cliently - Report Generator for Lawyers
# Purpose:     Cliently is a program that helps lawyers compile a clients information and produce a general report for administrative purposes.
#
# Author:      Alex Lu
# Created:     09-June-2021
# Updated:     22-June-2021
#-----------------------------------------------------------------------------

# Program Starts
#Import required libraries
import datetime 
import logging

#Logging Configuration
logging.basicConfig(filename='log.txt', level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

#Functions for calculations
def billCalc(rate, hours):
    '''
    Calculates a total cost for a lawyers consultation session
  
    Receives a rate value in dollars, and also receives an hours value. If the parameters are valid with the correct Type and Values, the function calculates the total cost by multiplying the rate by hours consulted and adding on additional retention fees. 
 
    Parameters
    ----------
    rate : int or float
        Cost of consultation per hour in dollars
    hours : int or float
        Amount of time spent with the client in hours
  
    Returns
    -------
    float
        Total bill cost after calculating the rate and time spent along with flat retention fee
 
    Raises 
    ------
    TypeError
        If the rate or hours value inputed is not an integer or float
    ValueError
        If the rate or hours is less than 0, and if the hours value is more than 1000
    ''' 
    logging.info("billCalc() function beginning with rate of: $" + str(rate) + " and " + str(hours) + " consulted")
    #Calculating the total bill amount
    #Check if the parameters are the right type
    if not isinstance(rate, (int, float)) or not isinstance(hours, (int, float)):
        logging.error("The rate or hours parameter was the wrong type")
        raise TypeError("Rate and hours consulted must be an integer or float")
    #Check if the parameters are the right value
    if rate < 0 or hours < 0:
        logging.error("The rate or hours consulted was negative")
        raise ValueError("Rate and hours consulted must be 0 or more")
    elif hours > 1000:
        logging.error("The hours consulted cannot be more than 1000")
        raise ValueError("The hours consulted was past the realistic threshold of 1000")
    #Otherwise proceed with bill calculation and return the amount
    else:
        bill = round(rate*hours+200,2)
        logging.info("The total bill is: " + str(bill))
        return bill

def suggestion(strength, flexibility, communication):
    '''
    Calculates recommended decision for the client based on their case details
  
    Receives a score of 1-10 for 3 aspects of a client's case: case strength, prosecution flexibility, and client communication. If the parameters are valid with the correct Type and Values, the function calculates a suggested outcome by adding all 3 scores together. 

    Parameters
    ----------
    strength : int 
        A lawyers personal rating based on the strength of the case's defence
    flexibility : int 
        A lawyers personal rating based on the flexibility of the prosecution
    communication : int 
        A lawyers personal rating based on the level of communication from the client
  
    Returns
    -------
    string
        The recommended case decision by the program based on ratings. 
 
    Raises 
    ------
    TypeError
        If the strength, flexibility, or communication value inputed is not an integer
    ValueError
        If the strength, flexibility, or communication value is less than one or more than 10
    ''' 
    logging.info("suggestion() function beginning with the following ratings: " + str(strength) + "-strength " + str(flexibility) + "-flexibility " + str(communication) + "-communication ")
    #Calculating a suggestion for the case
    #Check if the parameters are the right type
    if not isinstance(strength, int) or not isinstance(flexibility, int) or not isinstance(communication, int):
        logging.error("The strength, flexibility, or communication parameter was the wrong type")
        raise TypeError("All three ratings must be an integer")
    #Check if the parameters are the right value
    if strength < 1 or flexibility < 1 or communication < 1:
        logging.error("The strength, flexibility, or communication rating was less than 1")
        raise ValueError("All three ratings must be 1 or more and 10 or less")
    elif strength > 10 or flexibility > 10 or communication > 10:
        logging.error("The strength, flexibility, or communication rating was more than 10")
        raise ValueError("All three ratings must be 1 or more and 10 or less")
    #Otherwise proceed with calculation and return a suggestion depending on total score
    else:
        totalScore = strength + flexibility + communication
        logging.info("The total score is: " + str(totalScore))
        if totalScore >= 1 and totalScore <= 14:
            return "Drop the case"
        elif totalScore > 14 and totalScore <= 20:
            return "Let client decide"
        elif totalScore > 20 and totalScore <= 30:
            return "Pursue the case"

def dateCalc(year, month, day):
    '''
    Calculates the number of days from today to a given date
  
    Receives a year, month, and day value. If the parameters are valid with the correct Values and Type, the function calculates the number of days from the court date by subtracting the future date with today. Leap years also work with the function. 

    Parameters
    ----------
    year : int
        The year of the inputted future date
    month : int
        The month of the inputted future date
    day : int
        The day of the inputted future date
  
    Returns
    -------
    int
        Total amount of days until the court date
 
    Raises 
    ------
    TypeError
        If the year, month, or day is not an integer value
    ValueError
        If days until the court date was before than today or if the day/month/year does not exist or too far from a realistic lifetime
    ''' 
    logging.info("dateCalc() function beginning with the court date: " + str(year) + "/" + str(month) + "/" + str(day))
    #Calculating the days until a date
    #Check if the parameters are the right type
    if not isinstance(year, int) or not isinstance(month, int) or not isinstance(day, int):
        logging.error("The year, month, or day parameter was the wrong type")
        raise TypeError("All three parameters must be an integer")
    #Check if the parameters are the right value and if a date exists within a given month
    if year >= 2100:
        logging.error("Courtdate is more than 2100")
        raise ValueError("Courtdate is too far from today")
    elif month < 1 or month > 12:
        logging.error("Month must be more than 1 and less than 12")
        raise ValueError("The month entered does not exist")
    elif month in [1, 3, 5, 7, 8, 10, 12]:
        if day > 31 or day < 1:
            logging.error("Day must exist within range of the month")
            raise ValueError("The date entered does not exist")
    elif month == 2:
        #Leap Year Calculation, if year divided by 4 has a remainder of 0 it is a leap year
        if year%4 != 0:
            if day > 28 or day < 1:
                logging.error("Day must exist within range of the month")
                raise ValueError("The date entered does not exist")
        else:
            if day > 29 or day < 1:
                logging.error("Day must exist within range of the month")
                logging.warning("Technically, the years 1700, 1800, and 1900 are not leap years even though they pass this function's parameter check for leap years")
                raise ValueError("The date entered does not exist")
    elif month in [4, 6, 9, 11]:
        if day > 30 or day < 1:
            logging.error("Day must exist within range of the month")
            raise ValueError("The date entered does not exist")
    #After the parameters are checked, convert into a datetime object
    courtDate = datetime.date(year, month, day)
    logging.debug("The courtdate is: " + str(courtDate))
    #Find the datetime value for today
    today = datetime.date(2021, 6, 15)
    #today = datetime.date.today()
    logging.debug("The todays date is: " + str(today))
    #Check if the courtDate value is before today 
    if courtDate < today:
        logging.error("Courtdate is before today")
        raise ValueError("Courtdate cannot be in the past")
    #Otherwise, calculate the diffrence between the two dates in number of days
    else:
        difference = courtDate - today
        logging.info("The days until the court date: " + str(difference.days))
        return difference.days

#Function test billCalc()
assert billCalc(300, 8) == 2600, "$300 / hour for 8 hours should be $2600"
assert billCalc(0, 20) == 200, "$0 / hour at 20 hours should be $200"
assert billCalc(100_000, 0) == 200, "$100,000 / hour for 0 hours should be $200"
assert billCalc(499.88, 12.5) == 6448.5, "$499.88 / hour for 12.5 hours should be $6448.50"
assert billCalc(399.32, 15) == 6189.8, "$399.32 / hour for 15 hours should be $6189.80"
assert billCalc(200, 5.32843) == 1265.69, "$200/ hour for 5.32843 hours should be $1265.69"
#Function test suggestion()
assert suggestion(1, 1, 1) == "Drop the case", "With a score 3 case should be dropped"
assert suggestion(10, 10, 10) == "Pursue the case", "With a score 30 case should be pursued"
assert suggestion(5, 6, 5) == "Let client decide", "With a score 16, client should decide"
assert suggestion(1, 8, 5) == "Drop the case", "With a score 14, case should be dropped"
#Function test dateCalc()
assert dateCalc(2021, 6, 30) == 15, "June 30, 2021 should be 15 days from today"
assert dateCalc(2023, 8, 9) == 785, "August 9, 2023 should be 785 days from today"
assert dateCalc(2021, 6, 29) == 14, "June 29, 2021 should be 14 days from today"
assert dateCalc(2021, 6, 16) == 1, "June 16, 2021 should be 1 day from today"

#Introduction to program
logging.critical("Typing keyboard commands anywhere in the console will crash the program")
print("Welcome to Cliently, Please Enter Your Clients Information to Generate a Report")

#Criminal Cases
caseCount = -1
while caseCount < 0:
    try:
        #Take User input for # of cases they need to file
        caseCount = int(input("How Many Criminal Cases?: "))
        logging.info("The amount of cases entered is: " + str(caseCount))
        if caseCount < 0:
            #Print reminder if # of cases is less than 0
            print("Cases must be 0 or more")
    #Catch exceptions
    except TypeError as e:
        print("A TypeError has occured: " + str(e))
    except ValueError as e:
        print("A ValueError has occured: " + str(e))
    except Exception as e:
        print("An unknown error has occured: " + str(e))

for i in range(0, caseCount, 1):
    #Report Information Storage for Criminal Case
    clientCriminal = {"Type": "Criminal", "Name": 0, "Criminal Charge": 0, "Suggested Decision": 0, "Days Until Court": 0, "Legal Counsel Cost Due": 0}
    logging.debug("Current Report: " + str(clientCriminal))

    #Client Name, no need to check type value as any type of character is allowed in a name
    #Take user input for name
    clientName = input("Client Name: ").strip()
    logging.info("Name Entered: " + str(clientName))
    #Add the client name to the "Name" key
    clientCriminal["Name"] = clientName
    logging.debug("Current Report: " + str(clientCriminal))

    #Negotiated Consultation Rate
    totalBill = -1
    while totalBill == -1:
        try:
            #Take user input for the rate and hours charged
            rate = float(input("Client's Consultation Rate: $"))
            logging.info("Rate Entered: " + str(rate))
            hours = float(input("Hours to be billed: "))
            logging.info("Hours Entered: " + str(hours))
            #Calling bill calculation function
            totalBill = billCalc(rate, hours)
            logging.info("Total Bill calculated: " + str(totalBill))
        #Catching exceptions
        except TypeError as e:
            print("A TypeError has occured: " + str(e))
        except ValueError as e:
            print("A ValueError has occured: " + str(e))
        except Exception as e:
            print("An unknown error has occured: " + str(e))
        else:
            #If try block completes, add bill to the "Legal Counsel Cost Due" key
            clientCriminal["Legal Counsel Cost Due"] = totalBill
            logging.debug("Current Report: " + str(clientCriminal))

    #Charge Declaration, no need to check type value as any character is technically allowed
    #Take user input for their charge
    clientCharge = input("Criminal Charge: ")
    logging.info("Charge Entered: " + str(clientCharge))
    #Add the charge to the "Criminal Charge" key
    clientCriminal["Criminal Charge"] = clientCharge
    logging.debug("Current Report: " + str(clientCriminal))

    #Client case suggestion by program
    clientSuggestion = -1
    while clientSuggestion == -1:
        try:
            #Take user input for the strenth, flexibility, and communication of the case
            strength = int(input("On a scale of 1-10, how strong is the case?: "))
            logging.info("Level of strength: " + str(strength))
            flexibility = int(input("On a scale of 1-10, how flexible is the prosecution?: "))
            logging.info("Level of flexibility: " + str(flexibility))
            communication = int(input("On a scale of 1-10, how is the client's communication?: "))
            logging.info("Level of communication: " + str(communication))
            #Call suggestion function
            clientSuggestion = suggestion(strength, flexibility, communication)
            logging.info("Suggested outcome: " + str(clientSuggestion))
        #Catching exceptions
        except TypeError as e:
            print("A TypeError has occured: " + str(e))
        except ValueError as e:
            print("A ValueError has occured: " + str(e))
        except Exception as e:
            print("An unknown error has occured: " + str(e))
        else:
            #If try block completes, add suggestion to the "Suggested Decision" key
            clientCriminal["Suggested Decision"] = clientSuggestion
            logging.debug("Current Report: " + str(clientCriminal))

    #Days until court date calculation
    daysTillCourt = -1
    while daysTillCourt == -1:
        try:
            #Take user input for the court date
            courtDateInput = input("Court Date in YYYY-MM-DD format: ")
            logging.info("Inputted Court Date: " + str(courtDateInput))
            #Map the values for the year, month, and day entered by the user
            year, month, day = map(int, courtDateInput.split('-'))
            logging.info("Inputted Date: " + str(year) + "/" + str(month) + "/" + str(day))
            #Call dateCalc function
            daysTillCourt = dateCalc(year, month, day)
        #Catch exceptions
        except TypeError as e:
            print("A TypeError has occured: " + str(e))
        except ValueError as e:
            print("A ValueError has occured: " + str(e))
        except Exception as e:
            print("An unknown error has occured: " + str(e))
        else:
            #If try block completes, check if the court date is today and update accordingly
            if daysTillCourt == 0:
                clientCriminal["Days Until Court"] = "TODAY!!!"
                logging.debug("Current Report: " + str(clientCriminal))
            #Otherwise add the days to the "Days Until Court" key
            else:
                clientCriminal["Days Until Court"] = daysTillCourt
                logging.debug("Current Report: " + str(clientCriminal))

    #Report generation
    print("---------------------------------------------------")
    print("***CLIENT REPORT***")
    #Formatting and printing out every item in the stored dictionary for the criminal case
    for item in clientCriminal:
        print("{}: {}".format(item, clientCriminal[item]))
    print("---------------------------------------------------")

#Civil Cases
caseCount = -1
while caseCount < 0:
    try:
        #Take User input for # of cases they need to file
        caseCount = int(input("How Many Civil Cases?: "))
        logging.info("The amount of cases entered is: " + str(caseCount))
        if caseCount < 0:
            #Print reminder if # of cases is less than 0
            print("Cases must be 0 or more")
    #Catch exceptions
    except TypeError as e:
        print("A TypeError has occured: " + str(e))
    except ValueError as e:
        print("A ValueError has occured: " + str(e))
    except Exception as e:
        print("An unknown error has occured: " + str(e))

for i in range(0, caseCount, 1):
    #Report Information Storage for Civil Case
    clientCivil = {"Type": "Civil", "Name": 0, "Lawsuit Claim": 0, "Suggested Decision": 0, "Days Until Court": 0, "Legal Counsel Cost Due": 0}

    #Client Name, no need to check type value as any type of character is allowed in a name
    #Take user input
    clientName = input("Client Name: ").strip()
    logging.info("Name Entered: " + str(clientName))
    #Add the client name to the "Name" key
    clientCivil["Name"] = clientName
    logging.debug("Current Report: " + str(clientCivil))

    #Negotiated Consultation Rate
    totalBill = -1
    while totalBill == -1:
        try:
            #Take user input for rate and hours
            rate = float(input("Client's Consultation Rate: $"))
            logging.info("Rate Entered: " + str(rate))
            hours = float(input("Hours to be billed: "))
            logging.info("Hours Entered: " + str(hours))
            #Call totalBill function
            totalBill = billCalc(rate, hours)
            logging.info("Total Bill calculated: " + str(totalBill))
        #Catch exceptions
        except TypeError as e:
            print("A TypeError has occured: " + str(e))
        except ValueError as e:
            print("A ValueError has occured: " + str(e))
        except Exception as e:
            print("An unknown error has occured: " + str(e))
        else:
            #If try block completes, add the bill to the "Legal Counsel Cost Due" key
            clientCivil["Legal Counsel Cost Due"] = totalBill
            logging.debug("Current Report: " + str(clientCivil))

    #Charge Declaration, no need to check type value as any character is technically allowed
    #Take user input
    clientCharge = input("Client Lawsuit Claim: ")
    logging.info("Lawsuit Entered: " + str(clientCharge))
    #Add the client charge to the "Lawsuit Claim" key
    clientCivil["Lawsuit Claim"] = clientCharge
    logging.debug("Current Report: " + str(clientCivil))

    #Client case suggestion by program
    clientSuggestion = -1
    while clientSuggestion == -1:
        try:
            #Take user input for strength, flexibility, and communication variables
            strength = int(input("On a scale of 1-10, how strong is the case?: "))
            logging.info("Level of strength: " + str(strength))
            flexibility = int(input("On a scale of 1-10, how flexible is the party suing?: "))
            logging.info("Level of flexibility: " + str(flexibility))
            communication = int(input("On a scale of 1-10, how is the client's communication?: "))
            logging.info("Level of communication: " + str(communication))
            #Call the suggestion function
            clientSuggestion = suggestion(strength, flexibility, communication)
            logging.info("Suggested outcome: " + str(clientSuggestion))
        #Catch exceptions
        except TypeError as e:
            print("A TypeError has occured: " + str(e))
        except ValueError as e:
            print("A ValueError has occured: " + str(e))
        except Exception as e:
            print("An unknown error has occured: " + str(e))
        else:
            #If try block completes, update the suggestion to the "Suggested Decision" key
            clientCivil["Suggested Decision"] = clientSuggestion
            logging.debug("Current Report: " + str(clientCivil))
    
    #Days until court date calculation
    daysTillCourt = -1
    while daysTillCourt == -1:
        try:
            #Take user input for courtdate
            courtDateInput = input("Court Date in YYYY-MM-DD format: ")
            logging.info("Inputted Court Date: " + str(courtDateInput))
            #Map the inputted string into int values for year, month, and day
            year, month, day = map(int, courtDateInput.split('-'))
            logging.info("Inputted Date: " + str(year) + "/" + str(month) + "/" + str(day))
            #Call the dateCalc function
            daysTillCourt = dateCalc(year, month, day)
        #Catch exceptions
        except TypeError as e:
            print("A TypeError has occured: " + str(e))
        except ValueError as e:
            print("A ValueError has occured: " + str(e))
        except Exception as e:
            print("An unknown error has occured: " + str(e))
        else:
            #If try block completes, check if the court date is today and update accordingly
            if daysTillCourt == 0:
                clientCivil["Days Until Court"] = "TODAY!!!"
                logging.debug("Current Report: " + str(clientCivil))
            #Otherwise add the days to the "Days Until Court" key
            else:
                clientCivil["Days Until Court"] = daysTillCourt
                logging.debug("Current Report: " + str(clientCivil))

    #Report generation
    print("---------------------------------------------------")
    print("***CLIENT REPORT***")
    #Formatting and printing out every item in the stored dictionary for the civil case
    for item in clientCivil:
        print("{}: {}".format(item, clientCivil[item]))
    print("---------------------------------------------------")

#Filing Cases
caseCount = -1
while caseCount < 0:
    try:
        #Take User input for # of cases they need to file
        caseCount = int(input("How Many Filing Cases?: "))
        logging.info("The amount of cases entered is: " + str(caseCount))
        if caseCount < 0:
            #Print reminder if # of cases is less than 0
            print("Cases must be 0 or more")
    #Catch exceptions
    except TypeError as e:
        print("A TypeError has occured: " + str(e))
    except ValueError as e:
        print("A ValueError has occured: " + str(e))
    except Exception as e:
        print("An unknown error has occured: " + str(e))

for i in range(0, caseCount, 1):
    #Report Information Storage for Filing Case
    clientFiling = {"Type": "Filing", "Name": 0, "Days Until Deadline": 0, "Filing Fee": 0}

    #Client Name, no need to check type value as any type of character is allowed in a name
    #Take user input
    clientName = input("Client Name: ").strip()
    logging.info("Name Entered: " + str(clientName))
    #Add the name entered to the "Name" key
    clientFiling["Name"] = clientName
    logging.debug("Current Report: " + str(clientFiling))

    #Negotiated Filing Rate
    totalBill = -1
    while totalBill == -1:
        try:
            #Take user input for rate and hours
            rate = float(input("Client's Filing Rate: $"))
            logging.info("Rate Entered: " + str(rate))
            hours = float(input("Hours to be billed: "))
            logging.info("Hours Entered: " + str(hours))
            #Call totalBill function
            totalBill = billCalc(rate, hours)
            logging.info("Total Bill calculated: " + str(totalBill))
        #Catch exceptions
        except TypeError as e:
            print("A TypeError has occured: " + str(e))
        except ValueError as e:
            print("A ValueError has occured: " + str(e))
        except Exception as e:
            print("An unknown error has occured: " + str(e))
        else:
            #If try block completes, add the bill to the "Filing Fee" key
            clientFiling["Filing Fee"] = totalBill
            logging.debug("Current Report: " + str(clientFiling))
    
    #Days until court date calculation
    filingDeadline = -1
    while filingDeadline == -1:
        try:
            #Take user input for filing deadline date
            filingDeadlineInput = input("Filing deadline in YYYY-MM-DD format: ")
            logging.info("Inputted deadline date: " + str(filingDeadlineInput))
            #Map the inputted string into int values for year, month, and day
            year, month, day = map(int, filingDeadlineInput.split('-'))
            logging.info("Inputted Date: " + str(year) + "/" + str(month) + "/" + str(day))
            #Call dateCalc function
            filingDeadline = dateCalc(year, month, day)
        #Catch exceptions
        except TypeError as e:
            print("A TypeError has occured: " + str(e))
        except ValueError as e:
            print("A ValueError has occured: " + str(e))
        except Exception as e:
            print("An unknown error has occured: " + str(e))
        else:
            #If try block completes, check if the deadline is today and update accordingly
            if filingDeadline == 0:
                clientFiling["Days Until Deadline"] = "TODAY!!!"
                logging.debug("Current Report: " + str(clientFiling))
            #Otherwise add the days to the "Days Until Deadline" key
            else:
                clientFiling["Days Until Deadline"] = filingDeadline
                logging.debug("Current Report: " + str(clientFiling))

    #Report generation
    print("---------------------------------------------------")
    print("***CLIENT REPORT***")
    #Formatting and printing out every item in the stored dictionary for the filing case
    for item in clientFiling:
        print("{}: {}".format(item, clientFiling[item]))
    print("---------------------------------------------------")

#Program End
