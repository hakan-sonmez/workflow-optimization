# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 16:59:39 2017

@author: Hakan.X.Sonmez
"""

############# IMPORTING LIBRARIES ##########################
#import sys
#import os
import glob
import datetime

############## CREATING ERROR CODES DICTIONARY ############
Error_Codes_Dictionary = {
        '000.002.00048': 'Common COP message: Error writing nr of remaining shots to starter vial 1',
        '000.012.00196': 'Maintenance process completed with integrity errors',
        '000.017.00162': 'Too many subsequent washer aspiration failures',
        '005.000.00035': 'Integrity error(s) occured during system test',
        '018.002.00010': 'Target not reached: Pusher Incubator Washer', 
        '018.003.00010': 'Target not reached: Cuvette transport' ,
        '018.004.00010': 'Target not reached: Pusher Washer Incubator could not reach target',   
        '018.005.00010': 'Target not reached: Pusher Supply', 
        '019.000.00032': 'Aspiration detection failure',
        '019.003.00010': 'Target not reached: Washer',
        '020.00x.00010': 'Target not reached: Luminometer Reader',
        '022.000.00010': 'Target not reached: Internal Systems',
        '064.001.00070': 'RFID reader IC error: No RFID tag found',
        '069.001.00073': 'RFID reader IC error: Bitframing error',
        '262.001.00001': 'Mechanical error: Aborted job ',
        '262.002.00017': 'Failed to dispense into measuring cuvette',
        '262.009.00016': 'Reagent integrity error: Failed to aspirate',
        '262.012.00001': 'Washer Aspiration Failure',
        '262.132.00001': 'Sample integrity error',
        '262.133.00001': 'Reagent integrity error :Aborted job',
        '263.000.00004': 'Error while transmitting data to LIS',
        '270.009.00002': 'Aspiration Error occurred for Light Check',
        }


############## USER INPUT COLLECTION TEST LINES ############
"""
print "Please Enter DiaSorin XL Analyzer Serial Number ?" 
serial_no = raw_input("> ")
print "DiaSorin XL Serial Number: ", serial_no
print""
"""


"""
print "ERROR CODES DICTIONARY"
print ""
print "Length of Error Codes Dictionary=", len(Error_Codes_Dictionary)
print ""
print "Error Code:     Error Description" 
for i in Error_Codes_Dictionary:
    print i,":", Error_Codes_Dictionary[i]  
print ""
"""

############## MERGE INPUT LOG FILES INTO SINGLE FILE ############
day_count=0

#os.makedirs('MergedLogs_Folder')


read_files = glob.glob("LogFile*.txt")

with open("MergedLogs.txt", "wb") as outfile:
    for f in read_files:
        day_count=day_count+1
        with open(f, "rb") as infile:
            outfile.write(infile.read())

############## REDIRECTING THE OUTPUT TO REPORT FILE ############
            
"""
orig_stdout = sys.stdout
f2 = open('Output_Report.txt', 'w')
sys.stdout = f2
"""

############## DECLARING VARIABLES and INITIALIZING COUNTERS #############
lines = []

total_error_count = 0
#integrity_error_count = 0

counter_000_002_00048=0
counter_000_012_00196=0
counter_000_017_00162=0
counter_005_000_00035=0
counter_018_002_00010=0
counter_018_003_00010=0
counter_018_004_00010=0
counter_018_005_00010=0
counter_019_000_00032=0
counter_019_003_00010=0
counter_020_00x_00010=0
counter_022_000_00010=0
counter_064_001_00070=0
counter_069_001_00073=0
counter_262_001_00001=0
counter_262_002_00017=0
counter_262_009_00016=0
counter_262_012_00001=0
counter_262_132_00001=0
counter_262_133_00001=0
counter_263_000_00004=0
counter_270_009_00002=0

############## FIND ERRORS ########################################

searchfile = open("MergedLogs.txt",'r')

for line in searchfile:
    lines.append(line)
    
    if "error" in line or "Error" in line:
        print line
        total_error_count = total_error_count +1
              
    if "000.002.00048" in line:
        counter_000_002_00048 = counter_000_002_00048 + 1
        
    if "000.012.00196" in line:
        counter_000_012_00196 = counter_000_012_00196 + 1

    if "000.017.00162" in line:
        counter_000_017_00162 = counter_000_017_00162 + 1

    if "005.000.00035" in line:
        counter_005_000_00035 = counter_005_000_00035 + 1

    if "018.002.00010" in line:
        counter_018_002_00010 = counter_018_002_00010 + 1

    if "018.003.00010" in line:
        counter_018_003_00010 = counter_018_003_00010 + 1	

    if "018.004.00010" in line:
        counter_018_004_00010 = counter_018_004_00010 + 1	

    if "018.005.00010" in line:
        counter_018_005_00010 = counter_018_005_00010 + 1

    if "019.000.00032" in line:
        counter_019_000_00032 = counter_019_000_00032 + 1

    if "019.003.00010" in line:
        counter_019_003_00010 = counter_019_003_00010 + 1

    if "020.00x.00010" in line:
        counter_020_00x_00010 = counter_020_00x_00010 + 1
	
    if "022.000.00010" in line:
        counter_022_000_00010 = counter_022_000_00010 + 1
	
    if "064.001.00070" in line:
        counter_064_001_00070 = counter_064_001_00070 + 1		

    if "069.001.00073" in line:
        counter_069_001_00073 = counter_069_001_00073 + 1

    if "262.001.00001" in line:
        counter_262_001_00001 = counter_262_001_00001 + 1 
    
    if "262.002.00017" in line:
        counter_262_002_00017 = counter_262_002_00017 + 1

    if "262.009.00016" in line:
        counter_262_009_00016 = counter_262_009_00016 + 1

    if "262.012.00001" in line:
        counter_262_012_00001 = counter_262_012_00001 + 1

    if "262.132.00001" in line:
        counter_262_132_00001 = counter_262_132_00001 + 1	
		
    if "262.133.00001" in line:
        counter_262_133_00001 = counter_262_133_00001 + 1

    if "263.000.00004" in line:
        counter_263_000_00004 = counter_263_000_00004 + 1
		
    if "270.009.00002" in line:
        counter_270_009_00002 = counter_270_009_00002 + 1
    
searchfile.close()

print ""
print "============================================================================================="
print "XL LOGS ANALYZER REPORT"
print ""
print "REPORT GENERATION DATE:", datetime.date.today()
#print ""

#print(lines[1])
lhs_firstline, rhs_firstline = lines[1].split("_", 1)
#print(lines[-1])
lhs_lastline, rhs_lastline = lines[-1].split("_", 1)

print "Log Analysis Completed For the Dates between:", lhs_firstline, "and", lhs_lastline 
#print ""

print "Number of Days (Log Files) Analyzed=", day_count ,"days"
#print ""

print "Length of Merged Log File=", len(lines), "lines"
print ""

print "ERROR COUNTS SUMMARY"
print ""

#print "Total Error Messages Found:", total_error_count
#print ""

print "CRITICAL ERRORS WITH IMPACT ON REAGENT WASTE:"
print ""

print "Event ID      :  Error Description:       Error Count="  
print "--------      :  -----------------        -----------" 
print "262.009.00016 :  REAGENT INTEGRITY ERROR: Failed to aspirate Errors Found= ", counter_262_009_00016
print "262.133.00001 :  REAGENT INTEGRITY ERROR: Aborted job Errors Found= ", counter_262_133_00001
print "262.132.00001 :  SAMPLE INTEGRITY ERRORS Found= ", counter_262_132_00001


#print "018.002.00010 :  Target not reached: Pusher Incubator Washer Errors Found= ", counter_018_002_00010
#print "018.003.00010 :  Target not reached: Cuvette transport Errors Found= ", counter_018_003_00010
print "018.004.00010 :  TARGET NOT REACHED: Pusher Washer Incubator could not reach target Errors Found= ", counter_018_004_00010
#print "018.005.00010 :  Target not reached: Pusher Supply Errors Found= ", counter_018_005_00010

print "262.001.00001 :  MECHANICAL ERROR: Aborted job Errors Found= ", counter_262_001_00001

print ""
print "NON-CRITICAL ERRORS:"
#print ""

print "Event ID      :  Error Description:       Error Count="  
print "--------      :  -----------------        -----------" 
#print "262.009.00016':  Reagent integrity error: Failed to aspirate Errors Found= ", counter_262_009_00016
#print "262.133.00001':  Reagent integrity error: Aborted job Errors Found= ", counter_262_133_00001
#print "262.132.00001':  Sample integrity error Errors Found= ", counter_262_132_00001
#print "262.001.00001':  Mechanical error: Aborted job Errors Found= ", counter_262_001_00001
print "064.001.00070 :  RFID reader IC error: No RFID tag found Errors Found= ", counter_064_001_00070
print "262.002.00017 :  Failed to dispense into measuring cuvette Errors Found= ", counter_262_002_00017
print "263.000.00004 :  Error while transmitting data to LIS Errors Found= ", counter_263_000_00004
print "069.001.00073 :  RFID reader IC error: Bitframing error Errors Found= ", counter_069_001_00073
print "270.009.00002 :  Aspiration Error occurred for Light CheckErrors Found= ", counter_270_009_00002
print "019.000.00032 :  Aspiration detection failure Errors Found= ", counter_019_000_00032
print "262.012.00001 :  Washer Aspiration Failure Errors Found= ", counter_262_012_00001
#print "000.002.00048':  Common COP message: Error writing nr of remaining shots to starter vial 1' Errors Found= ", counter_000_002_00048
print "000.012.00196 :  Maintenance process completed with integrity Errors Found= ", counter_000_012_00196
print "000.017.00162 :  Too many subsequent washer aspiration failures Errors Found= ", counter_000_017_00162
print "005.000.00035 :  Integrity error(s) occured during system test Errors Found= ", counter_005_000_00035
#print "018.002.00010 :  Target not reached: Pusher Incubator Washer Errors Found= ", counter_018_002_00010
#print "018.003.00010 :  Target not reached: Cuvette transport Errors Found= ", counter_018_003_00010
#print "018.004.00010 :  Target not reached: Pusher Washer Incubator could not reach target Errors Found= ", counter_018_004_00010
#print "018.005.00010 :  Target not reached: Pusher Supply Errors Found= ", counter_018_005_00010
#print "019.000.00032 :  Aspiration detection failure Errors Found= ", counter_019_000_00032

if counter_019_003_00010 > 0 :
    print "019.003.00010 :  Target not reached: Washer Errors Found= ", counter_019_003_00010

if counter_020_00x_00010  > 0 :
    print "020.00x.00010 :  Target not reached: Luminometer Reader Errors Found= ", counter_020_00x_00010

if counter_022_000_00010  > 0 :
    print "022.000.00010 :  Target not reached: Internal Systems Errors Found= ", counter_022_000_00010


#print "263.000.00004':  Error while transmitting data to LIS Errors Found= ", counter_263_000_00004
#print "270.009.00002':  Aspiration Error occurred for Light CheckErrors Found= ", counter_270_009_00002
print ""

"""
print "000.002.00048':  Common COP message: Error writing nr of remaining shots to starter vial 1' Errors Found= ", counter_000_002_00048
print "000.012.00196':  Maintenance process completed with integrity Errors Found= ", counter_000_012_00196
print "000.017.00162':  Too many subsequent washer aspiration failures Errors Found= ", counter_000_017_00162
print "005.000.00035':  Integrity error(s) occured during system test Errors Found= ", counter_005_000_00035
print "018.002.00010':  Target not reached: Pusher Incubator Washer Errors Found= ", counter_018_002_00010
print "018.003.00010':  Target not reached: Cuvette transport Errors Found= ", counter_018_003_00010
print "018.004.00010':  Target not reached: Pusher Washer Incubator could not reach target Errors Found= ", counter_018_004_00010
print "018.005.00010':  Target not reached: Pusher Supply Errors Found= ", counter_018_005_00010
print "019.000.00032':  Aspiration detection failure Errors Found= ", counter_019_000_00032
print "019.003.00010':  Target not reached: Washer Errors Found= ", counter_019_003_00010
print "020.00x.00010':  Target not reached: Luminometer Reader Errors Found= ", counter_020_00x_00010
print "022.000.00010':  Target not reached: Internal Systems Errors Found= ", counter_022_000_00010
print "064.001.00070':  RFID reader IC error: No RFID tag found Errors Found= ", counter_064_001_00070
print "069.001.00073':  RFID reader IC error: Bitframing error Errors Found= ", counter_069_001_00073
print "262.001.00001':  Mechanical error: Aborted job Errors Found= ", counter_262_001_00001
print "262.002.00017':  Failed to dispense into measuring cuvette Errors Found= ", counter_262_002_00017
print "262.009.00016':  Reagent integrity error: Failed to aspirate Errors Found= ", counter_262_009_00016
print "262.012.00001':  Washer Aspiration Failure Errors Found= ", counter_262_012_00001
print "262.132.00001':  Sample integrity error Errors Found= ", counter_262_132_00001
print "262.133.00001':  Reagent integrity error: Aborted job Errors Found= ", counter_262_133_00001
print "263.000.00004':  Error while transmitting data to LIS Errors Found= ", counter_263_000_00004
print "270.009.00002':  Aspiration Error occurred for Light CheckErrors Found= ", counter_270_009_00002
print ""
"""

print "SUMMARY OF REAGENT INTEGRITY ERRORS"
print ""

if counter_262_009_00016 > 0 :
   print "Reagent Integrity Error: Failed to aspirate (Event ID:262.009.00016) Errors Found:", counter_262_009_00016
   print "Description: A reagent intergity error occured."
   print "Action: 1.Check the reagent vials 2.Start the job again 3.If the problem persists, call service to check XL system"
print ""

if counter_262_133_00001 > 0 :
   print "Reagent Integrity Error: Aborted job (Event ID:262.133.00001) Errors Found:", counter_262_133_00001
   print "Description: A reagent intergity error occured."
   print "Action: 1.Check the reagent vials 2.Start the job again 3.If the problem persists, call service to check XL system"
print ""


print "SUMMARY OF SAMPLE INTEGRITY ERRORS"
print ""

if counter_262_132_00001 > 0 :
   print "Sample Integrity Error: Aborted job (Event ID:262.132.00001) Errors Found:", counter_262_132_00001
   print "Description: A reagnet intergity error occured."
   print "Action: 1.Check the sample for anomalies 2.Start the job again 3.If the problem persists, call service to check XL system"
print ""


print "SUMMARY OF MECHANICAL ERRORS"
print ""

if counter_262_001_00001 > 0 :
   print "Mechanical Error: Aborted job (Event ID:262.001.00001)Errors Found:", counter_262_001_00001
   print "Description: A problem with the movements of mechanical subassemblies has occurred."
   print "Action: Check LIAISON®XL system about jammed cuvettes or disposable tips. 2. If possible, start job again. 3. Call service to check the mechanical subassemblies of LIAISON®XL system."
print ""


"""
if counter_064_001_00070 > 0 :
   print "RFID reader IC Errors (Event ID:064.001.00070) Found:", counter_064_001_00070
   print "Description: RFID reader IC error: No RFID tag found"
   print "Action: If error reoccurs, call service"
print ""
"""




print "END OF LOGS ANALYZER REPORT"   
print "============================================================================================="

############## REDIRECTING THE OUTPUT TO REPORT FILE ############   
   
"""    
sys.stdout = orig_stdout
f2.close()
"""
