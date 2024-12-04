import numpy as np
from datetime import datetime, timedelta
import pandas as pd

def importReferenceData(df):
    df = df.to_numpy()
    rows = 9
    cols = 3
    sampleTypes = ['inf', 'eff', 'blu']
    dataTypes = ['COD', 'BOD', 'Ammonium', '', '', '', 'Nitrate total', 'Ortho Phosphate', '', '']
    dataUnits = ['mg/L', 'mg/L', 'mg/L', '', '', '', 'mg/L', 'mg/L', '', '']
    infData = {
        'Date': {
            'Days': []
        }
    }
    effData = {
        'Date': {
            'Days': []
        }
    }
    bluData = {
        'Date': {
            'Days': []
        }
    }
    startRow = 3
    rowOffset = 14
    startCol = 1
    colOffset = 4
    zeroDate = df[startRow][startCol]

    for row in range(rows):
        for col in range(cols):
            dateRow = startRow + row * rowOffset
            dateCol = startCol + col * colOffset
            date = df[dateRow][dateCol]
            if (isinstance(date, str)):
                date = datetime.strptime(date, '%d/%m/%Y')
            daysPassed = (date - zeroDate).days
            infData['Date']['Days'].append(daysPassed)
            effData['Date']['Days'].append(daysPassed)
            bluData['Date']['Days'].append(daysPassed)
            for sampleIndex in range(len(sampleTypes)):
                sampleCol = dateCol + sampleIndex
                sampleType = sampleTypes[sampleIndex]
                for dataIndex in range(len(dataTypes)):
                    if dataTypes[dataIndex] == '':
                        continue
                    sampleRow = dateRow + 1 + dataIndex
                    sampleValue = df[sampleRow][sampleCol]
                    sampleValue = deleteString(sampleValue)

                    dataType = dataTypes[dataIndex]
                    if sampleType == 'inf':
                        if dataType in infData:
                            infData[dataType]['data'].append(sampleValue)
                        else:
                            infData[dataType] = {
                                'data': [sampleValue],
                                'unit': dataUnits[dataIndex]
                            }
                    if sampleType == 'eff':
                        if dataType in effData:
                            effData[dataType]['data'].append(sampleValue)
                        else:
                            effData[dataType] = {
                                'data': [sampleValue],
                                'unit': dataUnits[dataIndex]
                            }
                    if sampleType == 'blu':
                        if dataType in bluData:
                            bluData[dataType]['data'].append(sampleValue)
                        else:
                            bluData[dataType] = {
                                'data': [sampleValue],
                                'unit': dataUnits[dataIndex]
                            }

    return infData, effData, bluData

def deleteString(val):
    try:
        x = float(val)
        return x
    except:
        return np.nan