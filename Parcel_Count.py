#V7 Full Working Version

'''Variables that need name changes/add county name at beginning of variable:

line 141 - main()
'''
import arcpy
import csv
import pandas as pd 
import os

def repair_geo(ft_list, ml):
	try:
		arcpy.env.workspace = ml
	except:
		print('Unable to connect to workspace \n')
		quit()
	for ft in ft_list:
		ft =ml + '\\' + ft 
		print('Repairing feature: {}'.format(ft) + '\n')
		arcpy.RepairGeometry_management(ft)
	print('Done Repairing Parcel and Index' + '\n')
	time.sleep(30)

def get_intersect(ml, fl, countyName):
	'''process: find all parcels that intersect quarter (index) lines'''
	poly_intersect_index_fname = countyName + '_poly_intersect_index_fc'
	
	try:
		arcpy.env.workspace = ml
	except:
		print("Unable to connect to workspace")
		quit()
	
	print('Working on get_intersect')
	
	#getting inFeatures
	pc = ml + '\\' + fl[0] #Parcels
	fc = ml + '\\' + fl[1] #Index
	inFeatures = [pc, fc] #Note that opposite order from the ToolBox on arcmap for whatever reason. 
	
	try:
		outFeatures = ml + '\\' + poly_intersect_index_fname
		parcels_intersect_index_fc = arcpy.Intersect_analysis(inFeatures, outFeatures, 'ALL','', 'INPUT')
		print('Intersect Analysis worked like a charm, here is the data type: ' + str(type(parcels_intersect_index_fc)) + '\n')
		return parcels_intersect_index_fc
	except:
		print('poly_intersect_py_test already exists, moving on')
		parcels_intersect_index_fc = ml + '\\' + poly_intersect_index_fname
		return parcels_intersect_index_fc
	
def write_csv(parcels_intersect_index_fc, ml, countyName):
	'''Converts the polycount shapefile to a csv that get_count() will use'''
	
	#Getting vars for FeatureClassToShapefile_conversion
	parcel_intersect_index_csv = countyName + '_parcel_intersect_index.csv'
	Input_Features = parcels_intersect_index_fc.split('\\')[-1] #getting just the filename (poly_intersect_py_test_#) without the full path
	Output_Folder = "D:\\Data\\Poly_Count_Conversion"
	
	arcpy.FeatureClassToShapefile_conversion(Input_Features, Output_Folder)
	shapefile = Output_Folder + '\\' + Input_Features + '.shp'
	
	print("Converted Shapefile Layer")
	csv_file = arcpy.TableToTable_conversion(shapefile, Output_Folder, parcel_intersect_index_csv)

	print("This is the csv file: ", csv_file)
	print('CSV Conversion worked like a charm \n')

	return csv_file
	
		
def get_count(csv_fname, ml, countyName, parcel_name_field, map_name_field):
	'''converst the csv that was created into a dict 
	PARCELID as key and MAP_NAME count as value 
	then counts the number of Pages for each PARCELID'''
	
	print('Now going to get the count \n')
	
	try:
		conversion_fname = os.path.abspath(os.path.dirname(csv_fname))
	except:
		csv_fname = str(csv_fname)
		conversion_fname = os.path.abspath(os.path.dirname(csv_fname)) #apperently this is a list object?
	
	#creating dict with no duplicates
	counts_dict = dict()
	df = pd.read_csv(csv_fname)
	df1 = df[[parcel_name_field, map_name_field]] #creates data frame with just ParcelID and MAP_NAME
	print('Number of rows is: ', df1.shape[0])
	df2 = df1.drop_duplicates()
	print('After removing duplicates, number of rows is: {}'.format(df2.shape[0]) + '\n')
	
	for item in df2[parcel_name_field]: #loops through PARCELID column
		PARCELID = str(item)
		counts_dict[PARCELID] = counts_dict.get(PARCELID,0) + 1 #adds Count to ParcelID (dict key) or creates new ParcelID key if not already found
	
	with open(conversion_fname + '\\' + countyName + '_poly_count.csv', 'wb') as op_file: #writes poly_count.csv
		dict_writer = csv.writer(op_file)
		dict_writer.writerow([parcel_name_field, 'Poly_Count']) #creates headers
		for key, value in counts_dict.items(): 
			dict_writer.writerow(["'" + key + "'", value]) #loops through dictionary and writes the key (PARCELID) & values (Poly_Count)
	op_file.close()
	
	op_file = conversion_fname + '\\' + countyName + '_poly_count.csv'
	csv_to_geodb = arcpy.TableToGeodatabase_conversion(op_file, ml)
	print("All Done.")


def main(C_Name, f_list, countyName,parcelName, mapName):
	
	map_location = os.path.abspath(os.path.dirname(__file__))
	arcpy.env.workspace = map_location
	feature_list = f_list
	countyName = C_Name
	
	#Create loop to find the parcel and index layer and add to feature list? 
	print('map_location: \n', map_location)
	repair_geo(feature_list, map_location)
	
	parcels_intersect_index = get_intersect(map_location, feature_list, countyName)
	print('Done with get_intersect function, here is the poly_count file: {} \n'.format(parcels_intersect_index))
	
	csv_file = write_csv(str(parcels_intersect_index), map_location, countyName)
	print('Here is the csv file: {}'.format(csv_file))
	print ('Here is the type: {}'.format(type(csv_file)) + '\n')
	
	get_count(csv_file, map_location, countyName,parcelName, mapName)
	print('Success!')
'''	
if __name__ == "__main__":
	main()
'''
#main(Name of County, list of parcel and index shapefile names, name of PareclID field, name of MapName field)
main('Pinellas', ['Parcels', 'Index'], 'PARCELID_DSP1', 'MapName') 

'''This line below was ran because everything worked up to this block, 
and I didn't want to have to rerun it'''
#get_count("D:\\Data\\Poly_Count_Conversion\\Pinellas_parcel_intersect_index.csv", os.path.abspath(os.path.dirname(__file__)), "Pinellas", 'PARCELID_D', 'MapName')
