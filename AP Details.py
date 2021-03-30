import requests, json, re, time, urllib3, certifi, datetime, os, sys

urllib3.disable_warnings()

try:
    while True:
        # Getting Access Token

        headers = {
            'Content-type': 'application/json',
        }
        data = '{"username":"user", "password":"SnapAV704", "grant_type":"password" }'
        responseAT = requests.post('https://192.168.1.184/api/v1/auth/login', headers=headers, data=data, verify=False)

        # Convert To Text Format To Parse

        responseAT_Str = responseAT.text
        splitStr = responseAT_Str.split(',')

        access_token = splitStr[3]
        access_token = access_token[16:-1]

        # Print Current Access Token

        print("")
        print("Current Access token: ", end = " ")
        print(access_token)
        print("")
        print("Press CTRL+C to stop.")
        print("Writing data to file...")
        print("")

        # Getting Device Details Using Access Token

        auth = "Bearer " + access_token + "'"

        # Setting End Time
        
        endTIme = time.time() + 60 * 4

        # Loop For 240 Seconds (4 Mins) 

        while time.time() < endTIme:
            outputFile = open("AP_Output.txt", "a+")

            headers2 = {'Content-type': 'application/json', 'Authorization': ("Bearer " + access_token),}
            deviceDetails = requests.get('https://192.168.1.184/api/v1/deviceinfo', headers=headers2, verify=False)
            deviceDetails_Str = deviceDetails.text
            deviceDetails_Str = deviceDetails_Str.split(",")

            macAddress = deviceDetails_Str[2]
            serialNum = deviceDetails_Str[3]
            upTime = deviceDetails_Str[4]
            memUsed = deviceDetails_Str[5]
            cpu = deviceDetails_Str[6]
            memFree = deviceDetails_Str[7]
            firmwareVersion = deviceDetails_Str[8]

            currentDateTime = datetime.datetime.now()

            # Remove Headers From Data

            memUsed_Str = memUsed[10:]
            memFree_Str = memFree[10:]
            cpu_Str = cpu[6:]
            upTime_Str = upTime[10:-1]

            # Convert String to Integer Format

            memUsed_Int = int(memUsed_Str)
            memFree_Int = int(memFree_Str)

            # Calculate Total Memory

            memTotal = memUsed_Int + memFree_Int
 
            # Calculate Memory Utilization and Format Percentage

            memUtilization = (memUsed_Int / memTotal) * 100
            memUtilization = '{:.1f}'.format(memUtilization)

            # Convert Back to String

            memTotal = str(memTotal)
            memUtilization = str(memUtilization)

            # Print Details in Console

            print(currentDateTime)
            print("UpTime: " + upTime_Str)
            print("Mem Utilization: " + memUtilization + "%")
            print("Mem Total: " + memTotal)
            print("Mem Used: " + memUsed_Str)
            print("Mem Free: " + memFree_Str)
            print("CPU: " + cpu_Str)

            print ("")

            # Print Details to File

            print(currentDateTime, file = outputFile)
            print("UpTime: " + upTime_Str, file = outputFile)
            print("Mem Utilization: " + memUtilization + "%", file = outputFile)
            print("Mem Total: " + memTotal, file = outputFile)
            print("Mem Used: " + memUsed_Str, file = outputFile)
            print("Mem Free: " + memFree_Str, file = outputFile)
            print("CPU: " + cpu_Str, file = outputFile)

            print ("", file = outputFile)

            time.sleep(10)

        outputFile.close()

        time.sleep(10)
except KeyboardInterrupt:
    outputFile = open("AP_Output.txt", "a+")
    print("Stopped!")
    outputFile.close()

