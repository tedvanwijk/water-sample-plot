import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta
from reference import importReferenceData
from plot import deleteString, plotAll, plotEff, plotDiff

def loadData(originalData):
    data = {}
    # parameters to be plotted
    parameters = ['Ammonium', 'Ortho Phosphate', 'COD', 'BOD', 'Conductivity', 'pH', 'Nitrogen total', 'Turbidity']

    for p in parameters:
        headerForParameter = p
        for header in originalData.columns:
            trimmedHeader = header[0:len(p)]
            if trimmedHeader == p:
                headerForParameter = header
                break
        
        # Column header for this parameter has been found
        unit = headerForParameter.split(' ')
        if len(unit) == 1:
            unit = '[-]'
        else:
            unit = unit[-1]

        data[p] = {
            'data': originalData[headerForParameter].to_list(),
            'unit': unit
        } 
    data['Date'] = getDateIndices(originalData['Date'].to_list())
    return data

def getDateIndices(dateList):
    date = dateList[0]
    zeroDate = datetime.strptime(date, '%d-%m-%Y')
    dateIndex = 0
    indices = []
    days = []
    for i in range(len(dateList)):
        if dateList[i] != date and not pd.isnull(dateList[i]):
            # new date found
            indices.append((dateIndex, i))
            date = dateList[i]
            dateItem = datetime.strptime(date, '%d-%m-%Y')
            daysPassed = (dateItem - zeroDate).days
            days.append(daysPassed)
            dateIndex = i
    indices.append((dateIndex, i + 1))
    indices.pop(0)
    result = {
        "Indices": indices,
        "Days": days
    }
    return result

def plotData(fileName, referenceFileName):
    path = os.path.join('data', fileName)
    df = pd.read_excel(path, engine='odf', sheet_name=['Influent Measurements', 'Effluent Measurements', 'Sludge Measurements'])

    referencePath = os.path.join('data', referenceFileName)
    referenceDf = pd.read_excel(referencePath, sheet_name='Blad1', header=None)
    refInfData, refEffData, refBluData = importReferenceData(referenceDf)
    
    inf = df['Influent Measurements']
    eff = df['Effluent Measurements']
    slu = df['Sludge Measurements']

    infData = loadData(inf)
    effData = loadData(eff)
    sluData = loadData(slu)

    # plotAll([infData, effData, sluData], ['Influent', 'Effluent', 'Sludge'], avg=False, refData=[refInfData, refEffData, refBluData], refLabels=['Influent ref', 'Effluent ref', 'BE ref'], ref=True)
    # plotEff(effData, avg=False, refData=[refEffData, refBluData], refLabels=['Effluent ref', 'BE ref'], ref=True)
    plotDiff(infData, effData)
    plt.show()

if __name__ == "__main__":
    fileName = 'Sample measurements (12).ods'
    referenceFileName = 'reference.xlsx'
    plotData(fileName, referenceFileName)