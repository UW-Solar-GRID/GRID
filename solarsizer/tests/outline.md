Gui 
:Check Lat/Lon (within US)
  
Utilities
1. Pull irradiance 
:Set year as global variable 
:Try, Catch for irradiance file 
  
2. Convert Load Profile 
:Clean up current file type parse
:Should only take in CSV 
:Check length of .txt file 
:Check that none of the values are NAN - might need to try this ourselves 
  
3. Parse Load Profile 
:Remove this 

Pysam Utils
1. run_pvmodel 
:check for no negative values and within limits 
:does nrel have documentation on load limits?

One shot: We could do this with the above smoke test or create another set up where we know the output

Edge test: Too many panels, 1-7 panels in string, 1-30 strings, 1-30 inverters 

Pattern test: Run twice with different number of panels, array with more panels should have greater uptime percentage 

