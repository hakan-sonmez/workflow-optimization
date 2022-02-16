"""
Load Distributor Tool - Version 1.5
Author: Hakan Sonmez, hakan.x.sonmez@questdiagnostics.com                       
"""

### IMPORTING PYTHON LIBRARIES##########
from pulp import * 
# from math import *
import math
import numpy as np
import time

print""
print""
print""
print ("======================PROGRAM STARTS HERE===============")
print ""
print "Load Distributor Tool "
print "Note: All user input values should be entered as integers."
print ""

### DEFAULT USER INPUT PARAMETERS ##################################

# Billable Test Volumes:
Vol_0=706       # Borrelia (Lyme)
Vol_1=619       # Measles IgG      
Vol_2=601       # Mumps IgG
Vol_3=830       # Rubella IgG
Vol_4=721       # VZV IgG
Vol_5=469       # HSV-1 IgG
Vol_6=537       # HSV-2 IgG
Vol_7=210       # VCA IgG
Vol_8=210       # EBV IgM
Vol_9=143       # EBNA IgG
Vol_10=86       # Toxo IgG
Vol_11=54       # Toxo IgM
Vol_12=22       # Rubella IgM
Vol_13=109      # CMV IgG
Vol_14=97       # CMV IgM
Vol_15=0        # Trepenoma  (Syphilis)
Vol_16=0        # EA IgG (EBV IgG)
Vol_17=0        # Vitamin D 

# Number of Analyzers on Site
n=7

#Number of Days on Site
days=5

#Input Type is set to Daily by Default
input_type = "Daily" # Please enter input type as "Weekly" if you are entering weekly Billable Test Volumes
#input_type =="Weekly"

# User Given Constraints/Constants:
daily_instrument_capacity = 1000

load_balancing_constraint=100 #Load Balancing Deviation from Average Upper Bound

B=200 # Load Balancing Upper Bound 

###USER INPUT ENTRY BLOCK############################

print "Enter the number of analyzers on the site:"
n = int(raw_input("> "))
print 'Number of analyzers entered =', n
print""

print "Enter the maximum daily instrument capacity constraint [maximum tests/day per instrument] (Default value is 1000 tests):"
daily_instrument_capacity = int(raw_input("> "))
print 'Maximum daily tests per instrument entered =', daily_instrument_capacity
print""

print "Enter the load balancing constraint (maximum daily test volume difference between any two instruments) (Default value is 150 tests):"
balance_constraint = int(raw_input("> "))
print 'Load balancing constraint entered = ', balance_constraint
print""
load_balancing_constraint=math.floor(balance_constraint/2)

##print 'Enter "D" to input the Daily volumes or Enter "W" to input the Weekly volumes. (Default entry type is Daily volumes) :'
##input_volume_type = raw_input("> ")
##if input_volume_type == "W":
##    input_type = "Weekly"
##    print "Assay Volume Entry Type entered:", input_type
##if input_volume_type == "D":
##    input_type = "Daily"
##    print "Assay Volume Entry Type entered:", input_type
##print""
##
##if input_type == "Weekly":
##    print "Enter the number of Operational Days in a week on the site as an integer [1-7](Default value is 5 days) :"
##    days = int(raw_input("> "))
##    while days > 7 or days < 1:
##        print "Number of operational days should be entered between 1 and 7. Please re-enter the number of Operational Days in a week on the site as an integer (Default value is 5 days) :"
##        days = int(raw_input("> "))
##    print 'Number of operational days  entered =', days
##print""


### USER INPUT PARAMETERS END HERE ##################################


###Secondary Inputs (indirect Inputs)
#Number of Assays Tested
rows=18
rows_merged=rows-9   # 8: Number of Merged assays

weekly_instrument_capacity = days*daily_instrument_capacity

qc_freq= 0.01 # QC Frequency

### LP PROBLEM DEFINITION:
prob = LpProblem("test1", LpMinimize) 

### DICTIONARIES DEFINITIONS ##########################
Assay_Codes_Dictionary = {
                          1: 'Borrelia (Lyme)',
                          2: 'Measles IgG',
                          3: 'Mumps IgG',
                          4: 'Rubella IgG',
                          5: 'VZV IgG',
                          6: 'HSV-1 IgG',
                          7: 'HSV-2 IgG',
                          8: 'VCA IgG',
                          9: 'EBV IgM',
                          10: 'EBNA IgG',
                          11: 'Toxo IgG',
                          12: 'Toxo IgM',
                          13: 'Rubella IgM',
                          14: 'CMV IgG',
                          15: 'CMV IgM',
                          16: 'Trepenoma (Syphilis)',
                          17: 'EA IgG (EBV IgG)',
                          18: 'Vitamin D ', 
                          }

Assay_Codes_Dictionary_Merged = {
                          1: 'Borrelia (Lyme)',
                          2: 'Measles IgG & Mumps IgG',
                          3: 'Rubella IgG',
                          4: 'VZV IgG',
                          5: 'HSV-1 IgG & HSV-2 IgG',
                          6: 'VCA IgG',
                          7: 'CLEAN Procedure Assays: EBV IgM & EBNA IgG & EA IgG/EBV IgG + Toxo IgG & Toxo IgM + Rubella IgM + CMV IgG & CMV IgM',
                          8: 'Trepenoma (Syphilis)',
                          9: 'Vitamin D ', 
                          }                    
# Note: IgM Assays require CLEAN procedure                                              
    
QC_Frequency_Dictionary = {
                          1: 0.01, #  Borrelia (Lyme/Seasonal)
                          2: 0.01, # Measles
                          3: 0.01, # Mumps
                          4: 0.01, #'Rubella IgG',
                          5: 0.01, # 'VZV',
                          6: 0.01, # 'HSV-1',
                          7: 0.01, # 'HSV-2',
                          8: 0.01, # 'VCA-G',
                          9: 0.01, # 'EBV IgM',
                          10: 0.01, # 'EBNA',
                          11: 0.01, # 'Toxo IgG',
                          12: 0.01, # 'Toxo IgM',
                          13: 0.01, # 'Rubella IgM',
                          14: 0.01, # 'CMV IgG',
                          15: 0.01, # 'CMV IgM',
                          16: 0.01, # 'Trepenoma (Syphilis)',
                          17: 0.01, # 'EA-G (EBV IgG / Not on most sites)',
                          18: 0.01, # 'Vitamin D', 
                          }

Throughput_Rate_Dictionary = {
                          1: 135, # 'Borrelia (Lyme/Seasonal)',
                          2: 161, #'Measles',
                          3: 161, #'Mumps',
                          4: 161, #'Rubella IgG',
                          5: 161, #'VZV',
                          6: 171, #'HSV-1',
                          7: 171, #'HSV-2',
                          8: 161, #'VCA-G',
                          9: 161, #'EBV IgM',
                          10: 161, #'EBNA',
                          11: 171, #'Toxo IgG',
                          12: 171, #'Toxo IgM',
                          13: 90, #'Rubella IgM',
                          14: 161, #'CMV IgG',
                          15: 86, #'CMV IgM',
                          16: 140, #'Trepenoma (Syphilis)',
                          17: 161, #'EA-G (EBV IgG / Not on most sites)',
                          18: 161, #'Vitamin D (Seperate Labs)', 
                          }

Incubation_Time_Dictionary = {
                          1: 20, #'Borrelia (Lyme/Seasonal)',
                          2: 20, #'Measles',
                          3: 20, #'Mumps',
                          4: 20, #'Rubella IgG',
                          5: 20, #'VZV',
                          6: 20, #'HSV-1',
                          7: 20, #'HSV-2',
                          8: 20, #'VCA-G',
                          9: 20, #'EBV IgM',
                          10: 20, #'EBNA',
                          11: 20, #'Toxo IgG',
                          12: 25, #'Toxo IgM',
                          13: 30, #'Rubella IgM',
                          14: 20, #'CMV IgG',
                          15: 30, #'CMV IgM',
                          16: 30, #'Trepenoma (Syphilis)',
                          17: 20, #'EA-G (EBV IgG / Not on most sites)',
                          18: 20, #'Vitamin D (Seperate Labs)', 
                          }
Time_To_First_Result_Dictionary = {
                          1: 35, #'Borrelia (Lyme/Seasonal)',
                          2: 35, #'Measles',
                          3: 35, #'Mumps',
                          4: 35, #'Rubella IgG',
                          5: 35, #'VZV',
                          6: 35, #'HSV-1',
                          7: 35, #'HSV-2',
                          8: 35, #'VCA-G',
                          9: 35, #'EBV IgM',
                          10: 35, #'EBNA',
                          11: 35, #'Toxo IgG',
                          12: 40, #'Toxo IgM',
                          13: 45, #'Rubella IgM',
                          14: 35, #'CMV IgG',
                          15: 45, #'CMV IgM',
                          16: 40, #'Trepenoma (Syphilis)',
                          17: 35, #'EA-G (EBV IgG / Not on most sites)',
                          18: 35, #'Vitamin D (Seperate Labs)', 
                          }


### Entering Test Volumes Assays
inputed_volumes = list(range(rows))
for i in range(rows):
    print "Enter the daily billable test volume for assay", Assay_Codes_Dictionary[i+1], ":"
    inputed_volumes[i] = int(raw_input("> "))
    print "Volume entered for Assay",Assay_Codes_Dictionary[i+1],'=',inputed_volumes[i]
    print""
print ""

# Billable Test Volumes:
Vol_0=inputed_volumes[0]       # Borrelia  (Lyme Disease/Seasonal)
Vol_1=inputed_volumes[1]       # Measles       
Vol_2=inputed_volumes[2]       # Mumps
Vol_3=inputed_volumes[3]       # Rubella IgG
Vol_4=inputed_volumes[4]       # VZV
Vol_5=inputed_volumes[5]       # HSV-1
Vol_6=inputed_volumes[6]       # HSV-2
Vol_7=inputed_volumes[7]       # VCA-G
Vol_8=inputed_volumes[8]       # EBV IgM
Vol_9=inputed_volumes[9]       # EBNA
Vol_10=inputed_volumes[10]     # Toxo IgG
Vol_11=inputed_volumes[11]     # Toxo IgM
Vol_12=inputed_volumes[12]     # Rubella IgM
Vol_13=inputed_volumes[13]     # CMV IgG
Vol_14=inputed_volumes[14]     # CMV IgM
Vol_15=inputed_volumes[15]     # Trepenoma  (Syphilis)
Vol_16=inputed_volumes[16]     # EA-G  (i.e EBV IgG, not tested on most sites at the moment)
Vol_17=inputed_volumes[17]     # Vitamin D  (Seperate labs usually)

                      
### INPUT PARAMETERS ##################################
print ("=========================INPUT VALUES===================")
print ""

if input_type == "Weekly":
    Vol_0= math.ceil(float(Vol_0)/days)       # Borrelia  (Lyme Disease/Seasonal)
    Vol_1= math.ceil(float(Vol_1)/days)       # Measles       
    Vol_2= math.ceil(float(Vol_2)/days)       # Mumps
    Vol_3= math.ceil(float(Vol_3)/days)       # Rubella IgG
    Vol_4= math.ceil(float(Vol_4)/days)       # VZV
    Vol_5= math.ceil(float(Vol_5)/days)       # HSV-1
    Vol_6= math.ceil(float(Vol_6)/days)       # HSV-2
    Vol_7= math.ceil(float(Vol_7)/days)       # VCA-G
    Vol_8= math.ceil(float(Vol_8)/days)       # EBV IgM
    Vol_9= math.ceil(float(Vol_9)/days)       # EBNA
    Vol_10=math.ceil(float(Vol_10)/days)      # Toxo IgG
    Vol_11=math.ceil(float(Vol_11)/days)      # Toxo IgM
    Vol_12=math.ceil(float(Vol_12)/days)      # Rubella IgM
    Vol_13=math.ceil(float(Vol_13)/days)      # CMV IgG
    Vol_14=math.ceil(float(Vol_14)/days)      # CMV IgM
    Vol_15=math.ceil(float(Vol_15)/days)      # Trepenoma  (Syphilis)
    Vol_16=math.ceil(float(Vol_16)/days)      # EA-G  (i.e EBV IgG, not tested on most sites at the moment)
    Vol_17=math.ceil(float(Vol_17)/days)      # Vitamin D  (Seperate labs usually)


print "Number of Analyzers=",n
print ""

print "Maximum Daily Instrument Capacity Constraint=", daily_instrument_capacity
print ""

print "Load Balancing Upper Bound =", balance_constraint, "tests between instruments"
print ""

Daily_Volumes = [Vol_0, Vol_1, Vol_2, Vol_3, Vol_4, Vol_5, Vol_6, Vol_7, Vol_8, Vol_9, Vol_10,
                  Vol_11, Vol_12, Vol_13, Vol_14, Vol_15, Vol_16, Vol_17]
        
Daily_Volumes_Merged = [Vol_0, Vol_1 + Vol_2, Vol_3, Vol_4, Vol_5 + Vol_6, Vol_7, Vol_8 + Vol_9 + Vol_16 + Vol_10 +
                  Vol_11 + Vol_12 + Vol_13 + Vol_14, Vol_15, Vol_17]                  

print "Billable Test Volumes Entered for Each Assay:"                                   
for i in range(rows): 
   if Daily_Volumes[i] !=0:
        print "Assay", Assay_Codes_Dictionary[i+1], 'Volume =', Daily_Volumes[i]       
print""
          
#for i in range(rows_merged): 
#   if Daily_Volumes_Merged[i] !=0:
#        print "Assay", Assay_Codes_Dictionary_Merged[i+1], 'Volume =', Daily_Volumes_Merged[i]       
#print""
                                 
#print 'Daily Volumes=',Daily_Volumes
#print ""                  

#print 'Daily Volumes Merged=',Daily_Volumes_Merged
#print ""     

Total_Weekly_Volume= sum(Daily_Volumes)

Total_Weekly_Volume_Merged= sum(Daily_Volumes_Merged)

print 'Total Daily Volume=', Total_Weekly_Volume
print""

Average_Vol_per_Analyzer=np.around(Total_Weekly_Volume/n)
print "Average Volume per Analyzer=", Average_Vol_per_Analyzer
print ""

print "Calculating Optimal Solution..."
time.sleep(3)
print ""

#print 'Total Daily Volume Merged=', Total_Weekly_Volume_Merged
#print""

#################################################

# Intermediate Variables: 
mrows = list(range(rows))
#print "Number of Assays:", mrows
#print""

mrows_merged = list(range(rows_merged))
#print "Number of Assays Merged:", mrows_merged
#print""

ncolumns = list(range(n))
#print "Number of Analyzers ncolumns:",ncolumns
#print""

# Defining Linear Programming Decision Variables: 
#Non-Merged Case
#Volxx = LpVariable.matrix("Volxx", (mrows,ncolumns),lowBound=0, cat='Integer') 

#Merged Case
Volxx = LpVariable.matrix("Volxx", (mrows_merged,ncolumns),lowBound=0, cat='Integer') 

#print "Volumes per Instruments Matrix:", Volxx
#print""

## UPDATED CONSTRAINTS:
 
# Meeting Daily Test Volumes for Each Assay as a Sum of All Instruments Constraint
# Non-Merged Case
#for i in range (rows):
#    prob += sum(Volxx[i][j] for j in range(n)) == Daily_Volumes[i]

# Merged Case
for i in range (rows_merged):
    prob += sum(Volxx[i][j] for j in range(n)) == Daily_Volumes_Merged[i]

#Calculating Total Volume of Tests on Each Instrument To Be Used in Constaints
Volxn = list(range(n))

#Non-Merged Case
#for j in range(n):
#    Volxn[j] = sum(Volxx[i][j] for i in range(rows))

# Merged Case    
for j in range(n):
    Volxn[j] = sum(Volxx[i][j] for i in range(rows_merged))    
        
#Instrument Capacity Constraint
for j in range(n):
    prob += Volxn[j] <= daily_instrument_capacity

#Load Balancing Between Instruments Constraint
#for j in range(n):
#    for k in range (n):
#        if (j != k): 
#            prob += Volxn[j] - Volxn[k] <= B
##            #print "Volxn" ,j, '-', 'Volxn', k, '<=B' 
#


#Alternative Load Balancing Between Instruments Constraint Using Deviation from Average Instrument Volume
for j in range(n):
            prob += Volxn[j] - Average_Vol_per_Analyzer <= load_balancing_constraint
            prob += Volxn[j] - Average_Vol_per_Analyzer >= -load_balancing_constraint

#Minimum Volume on An Instrument Constraint
#print max(Daily_Volumes)
#print min(Daily_Volumes)
#for i in range (rows):
#    for j in range (n):
#        if Daily_Volumes[i] != 0:
#            prob += Volxx[i][j] > 100             

#print ""    
 
print"" 
print "=========================OPTIMAL SOLUTION==================="
print""

# UPDATED OBJECTIVE FUNCTION -4:
# Objective Function for Non-Merged Assays Case
#prob += lpSum( lpSum (((Volxx[i][j]*qc_freq)) + np.sign(Volxx[i][j])*3 for j in ncolumns) for i in mrows)

# Objective Function for Merged Assays Case
prob += lpSum( lpSum (((Volxx[i][j]*qc_freq)) + np.sign(Volxx[i][j])*3 for j in ncolumns) for i in mrows_merged)

# The problem is solved using PuLP's choice of Solver
prob.solve()
#prob.solve(GLPK())

# The status of the solution is printed to the screen
print "STATUS OF SOLUTION:", LpStatus[prob.status]
print""

#print "Status of Solution-1-2:",LpStatus[status]
#print""

# Alternative Way of Triggering Solution
#status = prob.solve()
#print "Status of Solution:",LpStatus[status]

# Solution 
#for v in prob.variables(): 
#    print v.name, "=", v.varValue
#print""

##############BLOCK TO DISPLAY RESULTS#########################################
Sum_merged = list(range(n))
Site_Sum_merged = 0
QC_Count_Sum_merged = list(range(n))

## For Merged Case
for j in range(n):
    Sum_merged[j]=0
    QC_Count_Sum_merged[j]=0    
    #print "-----------------------------------"
    #print 'INSTRUMENT #:',j+1 
    #print 'Assay Name | Volume (Tests)'
    for i in range(rows_merged):
        if Volxx[i][j].varValue != 0:
            #print Assay_Codes_Dictionary_Merged[i+1], ":", Volxx[i][j].varValue 
            Sum_merged[j] = Sum_merged[j] + Volxx[i][j].varValue
            QC_Count_Sum_merged[j]= QC_Count_Sum_merged[j] + math.ceil(Volxx[i][j].varValue*qc_freq)-1 + 4
    #print "--"
    #print 'Total Volume on Analyzer=', Sum_merged[j]
    #print 'Total QC Count on Analyzer=', QC_Count_Sum_merged[j]
    #print "-----------------------------------"
    Site_Sum_merged = Site_Sum_merged + Sum_merged[j]
    #print""  

#for x in range(1):    
#    print "UN-MERGED DISTIBUTION STARTS HERE============================================"
#print ""

### OLD: Unmerging Assays Method:
#for j in range(n):
#    print "-----------------------------------"
#    print 'INSTRUMENT #:',j+1 
#    #print 'Assay Name | Volume (Tests)'
#    for i in range(rows_merged):
#        if Volxx[i][j].varValue != 0:
#            if i == 1: 
#                print Assay_Codes_Dictionary[2], ":", np.around((Volxx[i][j].varValue/Daily_Volumes_Merged[i])*Daily_Volumes[1])  
#                print Assay_Codes_Dictionary[3], ":", np.around((Volxx[i][j].varValue/Daily_Volumes_Merged[i])*Daily_Volumes[2])
#            elif i == 4: 
#                print Assay_Codes_Dictionary[6], ":", np.around((Volxx[i][j].varValue/Daily_Volumes_Merged[i])*Daily_Volumes[5])  
#                print Assay_Codes_Dictionary[7], ":", np.around((Volxx[i][j].varValue/Daily_Volumes_Merged[i])*Daily_Volumes[6])
#            elif i == 6: 
#                print Assay_Codes_Dictionary[9], ":", np.around((Volxx[i][j].varValue/Daily_Volumes_Merged[i])*Daily_Volumes[8])  
#                print Assay_Codes_Dictionary[10], ":", np.around((Volxx[i][j].varValue/Daily_Volumes_Merged[i])*Daily_Volumes[9])
#                print Assay_Codes_Dictionary[17], ":", np.around((Volxx[i][j].varValue/Daily_Volumes_Merged[i])*Daily_Volumes[16])  
#                print Assay_Codes_Dictionary[11], ":", np.around((Volxx[i][j].varValue/Daily_Volumes_Merged[i])*Daily_Volumes[10])
#                print Assay_Codes_Dictionary[12], ":", np.around((Volxx[i][j].varValue/Daily_Volumes_Merged[i])*Daily_Volumes[11])
#            elif i == 7: 
#                print Assay_Codes_Dictionary[13], ":", np.around((Volxx[i][j].varValue/Daily_Volumes_Merged[i])*Daily_Volumes[12])  
#                print Assay_Codes_Dictionary[14], ":", np.around((Volxx[i][j].varValue/Daily_Volumes_Merged[i])*Daily_Volumes[13])
#                print Assay_Codes_Dictionary[15], ":", np.around((Volxx[i][j].varValue/Daily_Volumes_Merged[i])*Daily_Volumes[14])
#            else:     
#                print Assay_Codes_Dictionary_Merged[i+1], ":", Volxx[i][j].varValue 
#                Sum[j] = Sum[j] + Volxx[i][j].varValue
#                QC_Count_Sum[j]= QC_Count_Sum[j] + math.ceil(Volxx[i][j].varValue*qc_freq)-1 + 4
#    print "--"
#    print""   

    
### Defining Un-merge Matrix:    
Volyy = [[0 for j in ncolumns] for i in mrows] 
#for j in range(n):
#    for i in range(rows):
#        print Volyy[i][j]

for j in range(n):
    Volyy[0][j] = Volxx[0][j].varValue   # Borrelia
    Volyy[1][j] = (Volxx[1][j].varValue*Daily_Volumes[1])/Daily_Volumes_Merged[1]  # Measles
    Volyy[2][j] = (Volxx[1][j].varValue*Daily_Volumes[2])/Daily_Volumes_Merged[1]  #Mumps
    Volyy[3][j] = Volxx[2][j].varValue  # Rubella IgG
    Volyy[4][j] = Volxx[3][j].varValue  # VZV
    Volyy[5][j] = (Volxx[4][j].varValue*Daily_Volumes[5])/Daily_Volumes_Merged[4]  # HSV-1
    Volyy[6][j] = (Volxx[4][j].varValue*Daily_Volumes[6])/Daily_Volumes_Merged[4]  # HSV-2
    Volyy[7][j] = Volxx[5][j].varValue  # VCA-G
    Volyy[8][j] = (Volxx[6][j].varValue*Daily_Volumes[8])/Daily_Volumes_Merged[6]  # EBV IgM
    Volyy[9][j] = (Volxx[6][j].varValue*Daily_Volumes[9])/Daily_Volumes_Merged[6]  # EBNA
    Volyy[10][j] = (Volxx[6][j].varValue*Daily_Volumes[10])/Daily_Volumes_Merged[6]  # Toxo-IgG
    Volyy[11][j] = (Volxx[6][j].varValue*Daily_Volumes[11])/Daily_Volumes_Merged[6]  # Toxo-IgM
    Volyy[12][j] = (Volxx[6][j].varValue*Daily_Volumes[12])/Daily_Volumes_Merged[6]  # Rubella-IgM
    Volyy[13][j] = (Volxx[6][j].varValue*Daily_Volumes[13])/Daily_Volumes_Merged[6]  # CMV-IgG
    Volyy[14][j] = (Volxx[6][j].varValue*Daily_Volumes[14])/Daily_Volumes_Merged[6]  # CMV-IgM
    Volyy[15][j] = Volxx[7][j].varValue  # Trepenoma
    Volyy[16][j] = (Volxx[6][j].varValue*Daily_Volumes[16])/Daily_Volumes_Merged[6]  # EA-G
    Volyy[17][j] = Volxx[8][j].varValue # VitaminD

# For verification
#for j in range(n):
#    for i in range(rows):
#        print 'Volyy, i:',i, 'j:',j, '=', Volyy[i][j]

#After Non-Merged Operation

print "PROPOSED DISTRIBUTION OF ASSAYS TO INSTRUMENTS"

for j in range(n): 
    print ""
    print 'INSTRUMENT #:',j+1 
    #print 'Assay Name | Volume (Tests)'
    for i in range(rows):
        if Volyy[i][j] != 0:
            print Assay_Codes_Dictionary[i+1] 
    #print "--"

print""     
Sum = list(range(n))
Site_Sum = 0
QC_Count_Sum = list(range(n))
daily_minimum_runtime = list(range(n))


print "-----------------------------------"
print ""
print "PROPOSED LOAD DISTRIBUTION DETAILS"
print ""

for j in range(n):
    Sum[j]=0
    QC_Count_Sum[j]=0  
    daily_minimum_runtime[j]=0  
    print "-----------------------------------"
    print 'INSTRUMENT #:',j+1 
    #print 'Assay Name | Volume (Tests)'
    for i in range(rows):
        if Volyy[i][j] != 0:
            print Assay_Codes_Dictionary[i+1], ":", np.around(Volyy[i][j]) 
            #print Assay_Codes_Dictionary[i+1], ":", np.around(Volyy[i][j]) , "||| Required QC=", math.ceil(Volyy[i][j]*qc_freq)-1 + 4
            Sum[j] = Sum[j] + Volyy[i][j]
            QC_Count_Sum[j]= QC_Count_Sum[j] + math.ceil(Volyy[i][j]*qc_freq)-1 + 4
    #print "--"
    print 'Total Volume on Analyzer=', Sum[j]
    print 'Total QC Count on Analyzer=', QC_Count_Sum[j]
    daily_minimum_runtime[j] = ((Sum[j]*60)/Throughput_Rate_Dictionary[2]) + Incubation_Time_Dictionary[1] + Time_To_First_Result_Dictionary[1]
    #print 'Approximate Minimum Run Time (in minutes):' , math.ceil(daily_minimum_runtime[j]) , 'minutes'
    #print "-----------------------------------"
    Site_Sum = Site_Sum + Sum[j]
    print""


### INFORMATIVE OUTPUTS AFTER PROBLEM SOLUTION ################################   
print "======================TOTAL COUNTS SUMMARY ==================="   
print"" 

### For Verification
#print 'Total Volume on All Analyzers, Site Sum =', Site_Sum_merged
#print""    

### Showing Insrument Assignment for Each Assay for Merged Case 
#print "Assay Distribution over Instruments Summary - Merged Case"
#print ""
#for i in range(rows_merged): 
#    if Daily_Volumes_Merged[i] !=0:
#        print "Assay", Assay_Codes_Dictionary_Merged[i+1], 'is on instruments:' 
#        for j in range(n):
#            if (Volxx[i][j].varValue != 0):
#                print "Instrument#", j+1
#    print""
#
#### Showing Insrument Assignemnt for Each Assay for Merged Case
#print "Assay Distribution over Instruments Summary - Non-Merged Case"
#print ""
#for i in range(rows): 
#    if Daily_Volumes[i] !=0:
#        print "Assay", Assay_Codes_Dictionary[i+1], 'is on instruments:' 
#        for j in range(n):
#            if (Volyy[i][j] != 0):
#                print "Instrument#", j+1
#        print""

       
### For Verification
#SumAssay = list(range(rows))
#for i in range(rows):
#    SumAssay[i]=0
#    for j in range(n):
#        SumAssay[i] = SumAssay[i] + Volyy[i][j]
#    print 'Sum for Assay:', Assay_Codes_Dictionary[i+1], '=',SumAssay[i]
#print""  


#print "Solution Status Outputs:"
#print ""
#print "Status of Solution:",LpStatus[status]
#print""

print "Status of Solution:", LpStatus[prob.status]
print""

#print "Objective Function Value=", value(prob.objective), 'QC Tests Done '
#print""

#print 'Objective Function Value at Optimal Solution=', prob.objective.value()
#print ""


### Unmerged Case
for j in range (n):
    print 'Instrument#',j+1, ':Daily Volume=', Sum[j]
print""

### Merged Case
#for j in range (n):
#    print 'For Merged: Instrument#',j+1, ':Daily Volume=', Sum_merged[j]
#print""

### Unmerged Case
print 'Total Volume on All Instruments =', sum(Sum)
print""

### Merged Case
#print 'Total Volume on All Instruments =', sum(Sum_merged)
#print""

print "Average Volume per Analyzer=", Average_Vol_per_Analyzer
print""

print "Max Daily Instrument Capacity Constraint=", daily_instrument_capacity
print ""

#print 'Total QC Count Sum on All Instruments (Merged)=', sum(QC_Count_Sum_merged)
#print ""

print 'Total QC Count Sum on All Instruments=', sum(QC_Count_Sum)
print ""

#QC_Count_Sum = 0
#print "QC Count Sums per instrument (Merged)=",QC_Count_Sum_merged
#print""

#print "QC Count Sum per instrument (Non-Merged)=",QC_Count_Sum
#print""


print "======================PROGRAM ENDS HERE==================="   
print ""
print ""
