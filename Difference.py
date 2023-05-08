import processing

Layer1 = QgsProject.instance().mapLayersByName('ALKISGebäudeVolkertshausen')[0]
Layer2 = QgsProject.instance().mapLayersByName('OSMGebäudeVolkertshausen')[0]




differenceSmall = processing.run("qgis:difference",
{'INPUT': Layer1,
'OVERLAY': Layer2,
'OUTPUT':'memory:'})['OUTPUT']

lengthSmall = differenceSmall.featureCount()


#QgsProject.instance().addMapLayer(differenceSmall)
differenceBig = processing.run("qgis:difference",
{'INPUT': Layer2,
'OVERLAY': Layer1,
'OUTPUT':'memory:'})['OUTPUT']

lengthBig = differenceBig.featureCount()



#Fläche der DifferenzBig
differenceBigArea = processing.run("native:fieldcalculator",
{'INPUT': differenceBig,
'FIELD_NAME': 'differenceBigArea',
'FIELD_TYPE': 0 ,
'FORMULA': '$area',
'OUTPUT':'memory:'})['OUTPUT']


#Fläche der DifferenzSmall
differenceSmallArea = processing.run("native:fieldcalculator",
{'INPUT': differenceSmall,
'FIELD_NAME': 'differenceSmallArea',
'FIELD_TYPE': 0 ,
'FORMULA': '$area',
'OUTPUT':'memory:'})['OUTPUT']




differenceSmallMittelwert = processing.run("native:fieldcalculator",
{'INPUT': differenceSmallArea,
'FIELD_NAME': 'differenceSmallArea',
'FIELD_TYPE': 0 ,
'FORMULA': '"differenceSmallArea" / lengthSmall',
'OUTPUT':'memory:'})['OUTPUT']

differenceBigMittelwert = processing.run("native:fieldcalculator",
{'INPUT': differenceBigArea,
'FIELD_NAME': 'differenceBigArea',
'FIELD_TYPE': 0 ,
'FORMULA': '"differenceBigArea" / lengthBig',
'OUTPUT':'memory:'})['OUTPUT']


QgsProject.instance().addMapLayer(differenceBigArea)

QgsProject.instance().addMapLayer(differenceSmallArea)



