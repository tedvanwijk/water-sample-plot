import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def deleteString(val):
    try:
        x = float(val)
    except:
        return False
    return True

def plotAll(dataList, dataListNames, avg=True, refData=[], refLabels=[], ref=False):
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

def plotEff(dataSource, avg=True, refData=[], refLabels=[], ref=False):
    parameters = ['Ammonium', 'Ortho Phosphate', 'COD', 'BOD', 'Conductivity', 'pH', 'Nitrate total', 'Turbidity']
    # https://wetten.overheid.nl/BWBR0041313/2024-07-01#BijlageV
    limits = ['<1.5', '<0.9', None, None, None, '7-9', '<50', None]
    for ii in range(len(parameters)):
        p = parameters[ii]
        plt.figure()
        data = dataSource
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
        plt.scatter(xdata, ydata, label='Effluent Saxion')
        unit = data[p]['unit']
        plt.ylabel(f'{p} {unit}')
        plt.xlabel('Day# [-]')

        xdataRef = np.array([])
        if ref:
            for i in range(len(refData)):
                data = refData[i]
                label = refLabels[i]
                if p not in data:
                    continue
                ydataRef = data[p]['data']
                xdataRef = data['Date']['Days']
                plt.scatter(xdataRef, ydataRef, label=label, marker='x')

        limitValue = limits[ii]
        if limitValue != None:
            if (len(xdataRef) > len(xdata)):
                xdataLimit = xdataRef
            else:
                xdataLimit = xdata
            if limitValue[0] == '<':
                plt.fill_between(x=xdataLimit, y1=0, y2=float(limitValue[1:]), color='green', alpha=0.25)
            elif limitValue[0] == '>':
                plt.fill_between(x=xdataLimit, y1=float(limitValue[1:]), y2=np.max(ydata), color='green', alpha=0.25)
            else:
                # limitValue is min-max
                plt.fill_between(x=xdataLimit, y1=float(limitValue.split('-')[0]), y2=float(limitValue.split('-')[1]), color='green', alpha=0.25)

        plt.title(f'{p}: Effluent data')
        plt.legend()

        
    return