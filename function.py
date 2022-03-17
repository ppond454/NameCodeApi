
import numpy as np
import pandas as pd
import os

encoding_list = ['utf_8','ascii', 'big5', 'big5hkscs', 'cp037', 'cp273', 'cp424', 'cp437', 'cp500', 'cp720', 'cp737', 'cp775', 'cp850', 'cp852', 'cp855', 'cp856', 'cp857', 'cp858', 'cp860', 'cp861', 'cp862', 'cp863', 'cp864', 'cp865', 'cp866', 'cp869', 'cp874', 'cp875', 'cp932', 'cp949', 'cp950', 'cp1006', 'cp1026', 'cp1125', 'cp1140', 'cp1250', 'cp1251', 'cp1252', 'cp1253', 'cp1254', 'cp1255', 'cp1256', 'cp1257', 'cp1258', 'euc_jp', 'euc_jis_2004', 'euc_jisx0213', 'euc_kr', 'gb2312', 'gbk', 'gb18030', 'hz', 'iso2022_jp', 'iso2022_jp_1', 'iso2022_jp_2',
                 'iso2022_jp_2004', 'iso2022_jp_3', 'iso2022_jp_ext', 'iso2022_kr', 'latin_1', 'iso8859_2', 'iso8859_3', 'iso8859_4', 'iso8859_5', 'iso8859_6', 'iso8859_7', 'iso8859_8', 'iso8859_9', 'iso8859_10', 'iso8859_11', 'iso8859_13', 'iso8859_14', 'iso8859_15', 'iso8859_16', 'johab', 'koi8_r', 'koi8_t', 'koi8_u', 'kz1048', 'mac_cyrillic', 'mac_greek', 'mac_iceland', 'mac_latin2', 'mac_roman', 'mac_turkish', 'ptcp154', 'shift_jis', 'shift_jis_2004', 'shift_jisx0213', 'utf_32', 'utf_32_be', 'utf_32_le', 'utf_16', 'utf_16_be', 'utf_16_le', 'utf_7', 'utf_8_sig']


def encodeFile(fpath):
    for encoding in encoding_list:
        worked = True
        try:
            df = pd.read_csv(fpath, dtype=str, header=None, encoding=encoding)
        except:
            worked = False
        if worked:
            return df



def convertFunc(namefile):
    isNotValidate = False
    fpath = str("file/"+namefile+".csv")

    isEmpty = os.path.isfile(fpath) and os.path.getsize(fpath) > 0

    if not isEmpty:
        print("file is Empty")
        isNotValidate = True
        return "Empty"

    df = encodeFile(fpath)


    if type(df) == type(None) :
        print("FileError")
        isNotValidate = True
        return "FileError"
    
    print(df)
    if len(df.axes[1]) > 1:
        print("Over1Col")
        isNotValidate = True
        return "Over1Col"

    code = []
    result = []
    dfRef = pd.read_csv("ref/ref.csv", dtype=str)

    for i in df.iloc[:, 0]:
        print(i)
        if not i.isnumeric() : 
            isNotValidate = True
            break
        if len(i) == 8:
            i = i[:-2]
            data = dfRef[dfRef["code"] == i]
            normalize = data["province"].to_string(
                index=False)+"/"+data["district"].to_string(index=False)+"/"+data["Tambon"].to_string(index=False)
            result.append(normalize)
            code.append(i)

        elif len(i) == 6:
            data = dfRef[dfRef["code"] == i]
            normalize = str(data["province"]+"/" +
                            data["district"]+"/"+data["Tambon"])
            normalize = data["province"].to_string(
                index=False)+"/"+data["district"].to_string(index=False)+"/"+data["Tambon"].to_string(index=False)
            result.append(normalize)
            code.append(i)

        elif len(i) >= 7:
            isNotValidate = True
            break
        elif len(i) <= 9:
            isNotValidate = True
            break
    print(result)

    if not isNotValidate :
        pd.DataFrame({
            "ADDRCODE" : code,
            "แปลงที่อยู่": result
        }).to_csv("file/"+namefile+".csv", encoding="utf-8" )
        return "success"
    else:
        return "fail"
