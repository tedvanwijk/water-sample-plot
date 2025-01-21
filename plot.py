import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def deleteString(val):
    try:
        x = float(val)
    except:
        return False
    return True

parameterData = {
    "Influent": {
        "Ammonium": {
            "min": 100,
            "max": 1800
        },
        "Ortho Phosphate": {
            "min": 1.6,
            "max": 30
        },
        "COD": {
            "min": 0,
            "max": 1000
        },
        "BOD": {
            "min": 4,
            "max": 1650
        },
        "Conductivity": {
            "min": -1,
            "max": -1
        },
        "pH": {
            "min": -1,
            "max": -1
        },
        "Nitrogen total": {
            "min": 20,
            "max": 100
        },
        "Turbidity": {
            "min": -1,
            "max": -1
        }
    },
    "Effluent": {
        "Ammonium": {
            "min": 1,
            "max": 12
        },
        "Ortho Phosphate": {
            "min": 1.6,
            "max": 30
        },
        "COD": {
            "min": 0,
            "max": 1000
        },
        "BOD": {
            "min": 4,
            "max": 1650
        },
        "Conductivity": {
            "min": -1,
            "max": -1
        },
        "pH": {
            "min": -1,
            "max": -1
        },
        "Nitrogen total": {
            "min": 20,
            "max": 100
        },
        "Turbidity": {
            "min": -1,
            "max": -1
        }
    },
    "Sludge": {
        "Ammonium": {
            "min": 1,
            "max": 12
        },
        "Ortho Phosphate": {
            "min": 1.6,
            "max": 30
        },
        "COD": {
            "min": 0,
            "max": 1000
        },
        "BOD": {
            "min": 4,
            "max": 1650
        },
        "Conductivity": {
            "min": -1,
            "max": -1
        },
        "pH": {
            "min": -1,
            "max": -1
        },
        "Nitrogen total": {
            "min": 20,
            "max": 100
        },
        "Turbidity": {
            "min": -1,
            "max": -1
        }
    },
}

def checkDataValidity(dataType, parameter, values):
    for value in values:
        if value < 0:
            return 'invalid'
        
        minValue = parameterData[dataType][parameter]['min']
        maxValue = parameterData[dataType][parameter]['max']

        if minValue == -1 and maxValue == -1:
            continue

        if float(value) > maxValue or float(value) < minValue:
            return 'outOfRange'
        
    return 'valid'

def plotAll(dataList, dataListNames, colors=['tab:blue', 'tab:orange', 'tab:green'], avg=True, refData=[], refLabels=[], ref=False, refColors=[], plotLimits=False, parameters=[], limits=[]):
    for iii in range(len(parameters)):
        p = parameters[iii]
        plt.figure()
        for ii in range(len(dataList)):
            data = dataList[ii]
            dateIndices = data['Date']["Indices"]
            dateDays = data['Date']["Days"]
            ydata = np.array([])
            xdata = np.array([])

            ydataOutOfRange = np.array([])
            xdataOutOfRange = np.array([])

            ydataInvalid = np.array([])
            xdataInvalid = np.array([])

            xdataTotal = np.array([])
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

                newYValue = parameterData
                newXValue = np.ones(len(parameterData)) * dateDays[i]

                dataValid = checkDataValidity(dataListNames[ii], p, newYValue)
                
                if avg:
                    newYValue = np.average(parameterData)
                    newXValue = dateDays[i]

                if dataValid == 'invalid':
                    newYValue *= -1
                    xdataInvalid = np.append(xdataInvalid, newXValue)
                    ydataInvalid = np.append(ydataInvalid, newYValue)
                elif dataValid == 'outOfRange':
                    xdataOutOfRange = np.append(xdataOutOfRange, newXValue)
                    ydataOutOfRange = np.append(ydataOutOfRange, newYValue)
                else:
                    xdata = np.append(xdata, newXValue)
                    ydata = np.append(ydata, newYValue)

                xdataTotal = np.append(xdataTotal, newXValue)

            if len(xdata) != 0:
                plt.scatter(xdata, ydata, label=dataListNames[ii], c=colors[ii])
            if len(xdataOutOfRange) != 0:
                plt.scatter(xdataOutOfRange, ydataOutOfRange, label=f'{dataListNames[ii]} (out of range)', marker='^', c=colors[ii])
            if len(xdataInvalid) != 0:
                plt.scatter(xdataInvalid, ydataInvalid, label=f'{dataListNames[ii]} (invalid)', marker='x', c=colors[ii])
        unit = data[p]['unit']
        plt.ylabel(f'{p} {unit}')
        plt.xlabel('Days since BE startup [-]')

        xdataRef = np.array([])
        if ref:
            for i in range(len(refData)):
                data = refData[i]
                label = refLabels[i]
                if p not in data:
                    continue
                ydataRef = data[p]['data']
                xdataRef = data['Date']['Days']
                plt.scatter(xdataRef, ydataRef, label=label, c=refColors[i])

        if iii < len(limits):
            limitValue = limits[iii]
            if limitValue != None and plotLimits:
                if len(xdataRef) > 0 and xdataRef[-1] > xdataTotal[-1]:
                    xdataLimit = xdataRef
                else:
                    xdataLimit = xdataTotal
                if limitValue[0] == '<':
                    plt.fill_between(x=xdataLimit, y1=0, y2=float(limitValue[1:]), color='green', alpha=0.25)
                elif limitValue[0] == '>':
                    plt.fill_between(x=xdataLimit, y1=float(limitValue[1:]), y2=np.max(ydata), color='green', alpha=0.25)
                else:
                    # limitValue is min-max
                    plt.fill_between(x=xdataLimit, y1=float(limitValue.split('-')[0]), y2=float(limitValue.split('-')[1]), color='green', alpha=0.25)

        plt.title(f'{p}')
        plt.legend()
    return

def plotEff(dataSource, color='tab:orange', avg=True, refData=[], refLabels=[], ref=False, refColors=[], parameters=[]):
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

        ydataOutOfRange = np.array([])
        xdataOutOfRange = np.array([])

        ydataInvalid = np.array([])
        xdataInvalid = np.array([])

        xdataTotal = np.array([])
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

            newYValue = parameterData
            newXValue = np.ones(len(parameterData)) * dateDays[i]

            dataValid = checkDataValidity('Effluent', p, newYValue)

            if avg:
                newYValue = np.average(parameterData)
                newXValue = dateDays[i]

            if dataValid == 'invalid':
                newYValue *= -1
                xdataInvalid = np.append(xdataInvalid, newXValue)
                ydataInvalid = np.append(ydataInvalid, newYValue)
            elif dataValid == 'outOfRange':
                xdataOutOfRange = np.append(xdataOutOfRange, newXValue)
                ydataOutOfRange = np.append(ydataOutOfRange, newYValue)
            else:
                xdata = np.append(xdata, newXValue)
                ydata = np.append(ydata, newYValue)

            xdataTotal = np.append(xdataTotal, newXValue)

        if len(xdata) != 0:
            plt.scatter(xdata, ydata, label='Effluent Saxion', c=color)
        if len(xdataOutOfRange) != 0:
            plt.scatter(xdataOutOfRange, ydataOutOfRange, label='Effluent Saxion (out of range)', marker='^', c=color)
        if len(xdataInvalid) != 0:
            plt.scatter(xdataInvalid, ydataInvalid, label='Effluent Saxion (invalid)', marker='x', c=color)
        unit = data[p]['unit']
        plt.ylabel(f'{p} {unit}')
        plt.xlabel('Days since BE startup [-]')

        xdataRef = np.array([])
        if ref:
            for i in range(len(refData)):
                data = refData[i]
                label = refLabels[i]
                if p not in data:
                    continue
                ydataRef = data[p]['data']
                xdataRef = data['Date']['Days']
                plt.scatter(xdataRef, ydataRef, label=label, c=refColors[i])

        limitValue = limits[ii]
        if limitValue != None:
            if len(xdataRef) > xdata.shape[0]:
                xdataLimit = xdataRef
            else:
                xdataLimit = xdataTotal
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

def plotDiff(infData, effData, parameters=[]):
    dateIndicesInf = infData['Date']["Indices"]
    dateDaysInf = infData['Date']["Days"]
    dateIndicesEff = effData['Date']["Indices"]
    dateDaysEff = effData['Date']["Days"]
    dateIndicesLoop = dateIndicesInf
    dateDaysLoop = dateDaysInf

    barWidth = 0.15

    if len(dateIndicesEff) > len(dateIndicesInf):
        dateIndicesLoop = dateIndicesEff
        dateDaysLoop = dateDaysEff
    plt.figure()
    for p in range(len(parameters)):
        parameter = parameters[p]
        ydata = np.array([])
        xdata = np.array([])
        for i in range(len(dateIndicesLoop)):
            parameterDataInf = infData[parameter]['data']
            parameterDataEff = effData[parameter]['data']
            # slicing
            parameterDataInf = parameterDataInf[slice(*dateIndicesLoop[i])]
            parameterDataEff = parameterDataEff[slice(*dateIndicesLoop[i])]

            # remove strings and nan from data
            parameterDataInf = np.array([i for i in parameterDataInf if deleteString(i)])
            parameterDataInf = np.array(parameterDataInf)
            parameterDataInf = np.delete(parameterDataInf, np.where(pd.isnull(parameterDataInf)))

            parameterDataEff = np.array([i for i in parameterDataEff if deleteString(i)])
            parameterDataEff = np.array(parameterDataEff)
            parameterDataEff = np.delete(parameterDataEff, np.where(pd.isnull(parameterDataEff)))

            if len(parameterDataInf) == 0 or len(parameterDataEff) ==0:
                # either inf or eff data missing for this day. Still have to plot so we don't mess up axis data
                diff = 0
                xvalue = 0
            else:
                infAvg = np.average(parameterDataInf)
                effAvg = np.average(parameterDataEff)
                diff = np.abs(effAvg / infAvg * 100)
                if diff > 100:
                    diff = 0
                xvalue = dateDaysInf[i]

            ydata = np.append(ydata, diff)
            xdata = np.append(xdata, xvalue)

        xdataPlot = np.arange(len(xdata))
        xdataPlot = [e + p * barWidth for e in xdataPlot]
        plt.bar(xdataPlot, ydata, label=parameter, width=barWidth)
    plt.legend()
    plt.xlabel('Days since BE startup [-]')
    plt.ylabel('Remnant [%]')
    plt.xticks([r + (p / 2) * barWidth for r in np.arange(len(dateDaysLoop))],
        dateDaysLoop)
    plt.title(f'Remnant in effluent compared to influent. Remnant = 0 corresponds to invalid data')
    plt.grid(axis='y')

    for i in range(len(dateDaysLoop) + 1):
        i = i - 1
        plt.axvline(x = (i + (p / 2) * barWidth + 0.5), color='k', linestyle=':')
