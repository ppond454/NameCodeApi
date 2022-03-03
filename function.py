
import numpy as np
import pandas as pd


def convertFunc(namefile):
    df = pd.read_csv("ref/ref.csv", dtype=str)
    with open("file/"+namefile+".csv") as file_name:
        arr = np.loadtxt(file_name, dtype=str)
    result= []
    for i in arr:
        if len(i) == 8 :
            i = i[:-2]
            data= df[df["code"]== i]
            normalize = data["province"].to_string(index=False)+"/"+data["district"].to_string(index=False)+"/"+data["Tambon"].to_string(index=False)
            result.append(normalize)

        elif len(i)==6:
            data = df[df["code"]== i]
            normalize = str(data["province"]+"/"+data["district"]+"/"+data["Tambon"])
            normalize = data["province"].to_string(index=False)+"/"+data["district"].to_string(index=False)+"/"+data["Tambon"].to_string(index=False)
            result.append(normalize)
    

    pd.DataFrame({
        "ADDRCODE" : arr,
        "แปลงที่อยู่": result
    }).to_csv("file/"+namefile+".csv", encoding="utf-8" )
  







