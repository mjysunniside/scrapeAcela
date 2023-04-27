import re


def getSizeAndType(description_string_array):
    size = 0
    type = ""
    storage = False

    for index, item in enumerate(description_string_array):
        lower = item.lower()
        if "roof" in lower:
            type = "Roof"
        if "ground" in lower:
            type = "Ground" 
        if "ess" == lower:
            storage == True
        if "kw" in lower:
            if re.match("^kw.*", lower)!=None:
                before_size_nokw = description_string_array[index-1]
                new_size = float(before_size_nokw)
                if size==0:
                    size = new_size
                else:
                    if new_size > size:
                        size = new_size
            else:
                index_kw = lower.index("kw")
                new_size = float(lower[0:index_kw])
                if size==0:
                    size = new_size
                else:
                    if new_size > size:
                        size = new_size

    return {
        "type": type,
        "size": size,
        "storage": storage
    }




def getLicenseValueParcel(more_detail_array):
    value = 0
    cslb = 0
    parcel_num = ''

    for index, item in enumerate(more_detail_array):
        if "Estimated Valuation" in item:
            value_string = more_detail_array[index+1]
            value = float(value_string[1:].replace(',',''))
        if "License Number:" in item:
            cslb = int(more_detail_array[index+1])
        if "Parcel Number:" in item:
            parcel_num = more_detail_array[index+1]

    return {
        "value": value,
        "cslb": cslb,
        "parcel": parcel_num
    }