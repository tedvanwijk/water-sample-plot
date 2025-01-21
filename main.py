import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta
from reference import importReferenceData
from plot import deleteString, plotAll, plotEff, plotDiff

class Plotter:
    def __init__(self):
        super(Plotter, self).__init__()

    def loadData(self, fileName, sheetName):
        path = os.path.join('data', fileName)
        df = pd.read_excel(path, engine='odf', sheet_name=sheetName)

        data = {}
        # parameters to be plotted
        parameters = ['Ammonium', 'Ortho Phosphate', 'COD', 'BOD', 'Conductivity', 'pH', 'Nitrogen total', 'Turbidity']

        for p in parameters:
            headerForParameter = p
            for header in df.columns:
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
                'data': df[headerForParameter].to_list(),
                'unit': unit
            } 
        data['Date'] = self.getDateIndices(df['Date'].to_list())
        return data

    def loadReferenceData(self, fileName, sheetName):
        referencePath = os.path.join('data', fileName)
        referenceDf = pd.read_excel(referencePath, sheet_name=sheetName, header=None)
        data = importReferenceData(referenceDf)
        return data

    def getDateIndices(self, dateList):
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

if __name__ == "__main__":
    plotter = Plotter()

    fileName = 'Sample measurements (18).ods'
    referenceFileName = 'reference.xlsx'

    infData = plotter.loadData(fileName, 'Influent Measurements')
    effData = plotter.loadData(fileName, 'Effluent Measurements')
    sluData = plotter.loadData(fileName, 'Sludge Measurements')

    refInfData, refEffData, refBluData = plotter.loadReferenceData(referenceFileName, 'Blad1')

    plotAll([infData, effData, sluData], ['Influent', 'Effluent', 'Sludge'], avg=False, refData=[refInfData, refEffData, refBluData], refLabels=['Influent ref', 'Effluent ref', 'BE ref'], ref=False, refColors=['tab:red', 'tab:purple', 'tab:brown'], plotLimits=True)
    plotEff(effData, avg=False, refData=[refEffData, refBluData], refLabels=['Effluent de Sumpel', 'Effluent BluElephant de Sumpel'], ref=True, refColors=['tab:purple', 'tab:brown'])
    plotDiff(infData, effData)

    plt.show()