# written by Alex Din
# this script creates a field with a Composite Index Score for a variable (e.g. vacant homes)
# this example is written using USPS vacancy data so change the variables below (feat, theVar, ratioField and indexField) to what is relevant for you
import arcpy, numpy
arcpy.env.overwriteOutput = True
# set up the variables
feat = "Census_Tracts_PRJ"     # feature class in question here
theVar = "Residences_Vacant"   # the variable you want to analyze
ratioField = "RatioField"      # a temporary field where the ratio is calculated before it is normalized
indexField = "VacantIndex"     # the output index field
# do the actions
field = arcpy.da.TableToNumPyArray(feat, theVar, skip_nulls=True)
totalTheVar = field[theVar].sum()
arcpy.AddField_management(feat, ratioField, "DOUBLE", 6)
arcpy.AddField_management(feat, indexField, "DOUBLE", 6)
expression1 = '((float(!' + theVar +'!) ) / {} )'.format(totalTheVar)
arcpy.CalculateField_management(feat, ratioField, expression1, "PYTHON_9.3")
field = arcpy.da.TableToNumPyArray(feat, ratioField, skip_nulls=True)
maxRatio = field[ratioField].max()
expression2 = '((float(!' + ratioField +'!) ) / {} )'.format(maxRatio)
arcpy.CalculateField_management(feat, indexField, expression2, "PYTHON_9.3")
arcpy.DeleteField_management(feat, ratioField)