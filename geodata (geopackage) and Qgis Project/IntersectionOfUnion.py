# 16.01.23 final Version, Paul G.

import processing

# Parameter der Funktion mapLayersByName()
a1 = QgsProject.instance().mapLayersByName('OSMGebäudeVolkertshausen')[0]
a2 = QgsProject.instance().mapLayersByName('ALKISGebäudeVolkertshausen')[0]

#Verschneidung
tmpVerschneidung = processing.run("native:intersection",
{'INPUT': a1,
'OVERLAY': a2,
'INPUT_FIELDS': 'fid',
'OVERLAY_FIELDS': 'fid',
'OUTPUT':'memory:'})['OUTPUT']

tmpVerschneidungAndersrum = processing.run("native:intersection",
{'INPUT': a2,
'OVERLAY': a1,
'INPUT_FIELDS': 'fid',
'OVERLAY_FIELDS': 'fid',
'OUTPUT':'memory:'})['OUTPUT']
#berechnung der Verschnittenen Fläche

tmpFeldrechner = processing.run("native:fieldcalculator",
{'INPUT': tmpVerschneidung,
'FIELD_NAME': 'areaVerschneidung',
'FIELD_TYPE': 0 ,
'FORMULA': '$area',
'OUTPUT':'memory:'})['OUTPUT']

tmpFeldrechnerAndersherum = processing.run("native:fieldcalculator",
{'INPUT': tmpVerschneidungAndersrum,
'FIELD_NAME': 'areaVerschneidung2',
'FIELD_TYPE': 0 ,
'FORMULA': '$area',
'OUTPUT':'memory:'})['OUTPUT']


#QgsProject.instance().addMapLayer(tmpFeldrechner)

tmpJoinIntersection = processing.run("native:joinattributestable",
{'INPUT': tmpFeldrechner,
'FIELD': 'fid',
'INPUT_2': tmpFeldrechnerAndersherum,
'FIELD_2': 'fid',
'OUTPUT':'memory:'})['OUTPUT']

tmpFeldrechnerFürGesamtVerschneidung = processing.run("native:fieldcalculator",
{'INPUT': tmpJoinIntersection,
'FIELD_NAME': 'areaGesamtVerschneidung',
'FIELD_TYPE': 0 ,
'FORMULA': '"areaVerchneidung" + "areaVerschneidung2" ',
'OUTPUT':'memory:'})['OUTPUT']



#Vereinigung
tmpUnion = processing.run("qgis:union",
{'INPUT': a1,
'OVERLAY': a2,
'INPUT_FIELDS': 'fid',
'OVERLAY_FIELDS': 'fid',
'OUTPUT':'memory:'})['OUTPUT']

#Berechnung der einzelnen Vereinigungsfläche
tmpFeldrechnerUnion = processing.run("native:fieldcalculator",
{'INPUT': tmpUnion,
'FIELD_NAME': 'areaVereinigung',
'FIELD_TYPE': 0 ,
'FORMULA': '$area',
'OUTPUT':'memory:'})['OUTPUT']

#QgsProject.instance().addMapLayer(tmpFeldrechnerUnion)

# die Gesamtfläche der Vreinigung berechnen
tmpFeldrechnerGesamt = processing.run("native:fieldcalculator",
{'INPUT': tmpFeldrechnerUnion,
'FIELD_NAME': 'gesamt',
'FIELD_TYPE': 0 ,
'FORMULA': 'sum("areaVereinigung" , group_by:= "fid" )',
'OUTPUT':'memory:'})['OUTPUT']

#QgsProject.instance().addMapLayer(tmpFeldrechnerGesamt)

#Tabellen nach fid zueinanderführen
tmpJoin = processing.run("native:joinattributestable",
{'INPUT': tmpFeldrechnerFürGesamtVerschneidung,
'FIELD': 'fid',
'INPUT_2': tmpFeldrechnerGesamt,
'FIELD_2': 'fid',
'OUTPUT':'memory:'})['OUTPUT']

#QgsProject.instance().addMapLayer(tmpJoin)

# Berechnung des Intersection of Union
tmpIntersectionOfUnion = processing.run("native:fieldcalculator",
{'INPUT': tmpJoin,
'FIELD_NAME': 'Intersection of Union',
'FIELD_TYPE': 0 ,
'FORMULA': '"areaVereinigung" / "gesamt" ',
'OUTPUT':'memory:'})['OUTPUT']

QgsProject.instance().addMapLayer(tmpIntersectionOfUnion)
