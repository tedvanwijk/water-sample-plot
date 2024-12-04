import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta
from reference import importReferenceData
from plot import deleteString, plotAll, plotEff

def loadData(originalData):
    data = {}
    # parameters to be plotted
    parameters = ['Ammonium', 'Ortho Phosphate', 'COD', 'BOD', 'Conductivity', 'pH', 'Nitrate total', 'Turbidity']

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

def plot(dataList, dataListNames, avg=True, refData=[], refLabels = [], ref=False):
    parameters = ['Ammonium', 'Ortho Phosphate', 'COD', 'BOD', 'Conductivity', 'pH', 'Nitrate total', 'Turbidity']
    for p in parameters:
        plt.figure()
        for ii in range(len(dataList)):
            data = dataList[ii]
            dateIndices = data['Date']["Indices"]
            dateDays = data['Date']["Days"]
            ydata = np.array([])
            xdata = np.array([])
            for i in range(len(dateIndices)):
                parameterData = data[p]['data']
                # slicing
                parameterData = parameterData[slice(*dateIndices[i])]

                # remove strings and nan from data
                parameterData = np.array([i for i in parameterData if deleteString(i)])
                parameterData = np.array(parameterData)
                parameterData = np.delete(parameterData, np.where(pd.isnull(parameterData)))
                if len(parameterData) == 0:
                    continue

                if avg:
                    ydata = np.append(ydata, np.average(parameterData))
                    xdata = np.append(xdata, dateDays[i])
                else:
                    ydata = np.append(ydata, parameterData)
                    xdata = np.append(xdata, np.ones(len(parameterData)) * dateDays[i])

            plt.scatter(xdata, ydata, label=dataListNames[ii])
            unit = data[p]['unit']
        plt.ylabel(f'{p} {unit}')
        plt.xlabel('Day# [-]')

        if ref:
            for i in range(len(refData)):
                data = refData[i]
                label = refLabels[i]
                if p not in data:
                    continue
                ydata = data[p]['data']
                xdata = data['Date']['Days']
                plt.scatter(xdata, ydata, label=label, marker='x')

        plt.title(f'{p}')
        plt.legend()
    return

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
    plotEff(effData, avg=False, refData=[refEffData, refBluData], refLabels=['Effluent ref', 'BE ref'], ref=True)
    plt.show()

if __name__ == "__main__":
    fileName = 'Sample measurements (9).ods'
    referenceFileName = 'reference.xlsx'
    plotData(fileName, referenceFileName)