import re
from descriptionParse import getSizeAndType 
text = "Digital. Roof mount PV solar - 6.48kW - 18 panels - 1 inverter. NO MPU. NO BATTERY. Includes two inspections. Final required."
text_array = text.split(" ")



values = getSizeAndType(text_array)

print(values)




