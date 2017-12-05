# ParcelCount
Counts the number of data driven pages a given polygon is in.   

To run you need to add the following inputs:
1. Name of County - for file naming purposes
2. List of two shapefile names you will be comparing. 
  a. The shape file of the polygon I want to get the count for.
  b. The data driven pages shapefile.
3. Name of the polygon ID field.  I generally use ParcelID, Parcel_Name, PIN, etc.
4. Name of the data driven page.  I generally use MAP_NAME with my maps. 

The syntax will look like this:

main([CountyName], [List of Polygon and Index shapefiles], PolygonID Field, IndexID Field)

Ex: main('Pinellas', ['Parcels', 'Index'], 'PARCELID_DSP1', 'MAP_NAME')

Note:  For certain ArcGIS tools, the field names must be < a specific number of characters.  In my example ArcGIS automatically renames
my PARCELID_DSPI to PARCELID_D causing an error, in which instance I run the propgram from where that error accord.  You can do this by starting at the get_count() function I have bellow the main().  Again, this will only happen if you have a Field name that is tool long for ArcGIS to handle. 
