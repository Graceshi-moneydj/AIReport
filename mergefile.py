import sys, getopt, traceback, os, shutil, csv
import json
from datetime import date

def Usageinfo():
    print('mergefile.py -f <sourcefolder> -o <outputfile> -b <backupfolder>')
    print('Options:')
    print('    -f:Input source folder    ex: -f ".\\folder\\"')
    print('    -o:Output csv file       ex: -o ".\\all_report.txt"')
    print('Example:')
    print('    py mergefile.py -f "\\\\s-vcfs02\\AIReport\\" -o "\\\\s-vcfs02\\AIReport\\tmp\\all_report.txt" -b "\\\\s-vcfs02\\AIReport\\backup\\"')


def MoveFiles(source_dir: str, destination_dir: str):
    files = os.listdir(source_dir)
    for fname in files:
        if fname.endswith(".txt"):
            source_file = os.path.join(source_dir, fname)
            destination_file = os.path.join(destination_dir, fname)
            shutil.move(source_file, destination_file)

def MergeFiles(folder: str, outfilepath: str):
    files = os.listdir(folder)
    all_list = []
    header = None
    result = []
    for fname in files:
        fname_split = fname.split("_")
        if len(fname_split) < 3:
            continue

        datestr = fname_split[0]
        fdate = date(int(datestr[:3]) + 1911, int(datestr[3:5]), int(datestr[5:]))
        with open(os.path.join(folder, fname), "r", newline="", encoding="utf-8") as csvfile:
            # 創建CSV閱讀器對象
            csvreader = csv.reader(csvfile)
            #略過headline
            header = next(csvreader)
            # 逐行讀取CSV文件, 並插入日期
            for i, row in enumerate(csvreader):
                row.insert(1, date.strftime(fdate, "%Y-%m-%d"))
            result.append(row)

    # 寫出CSV文件
    header.insert(1, "date")
    with open(outfilepath, "w", newline="", encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(header)  # 寫入 CSV 文件的標題行
        csvwriter.writerows(result)  # 寫入數據

def main(argv):
    input_folder = ''
    output_filename = ''
    backup_folder = ''
    tmp_folder = ''
    try:
      opts, args = getopt.getopt(argv,"hf:o:b:",["sourcefolder=","output=","backupfolder="])
    except getopt.GetoptError:
      Usageinfo()
      sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            Usageinfo()
            sys.exit()
        elif opt in ("-f", "--sourcefolder="):
           input_folder = arg
        elif opt in ("-o", "--outputfile"):
           output_filename = arg
        elif opt in ("-b", "--backupfolder"):
           backup_folder = arg

    try:
        tmp_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)),'tmp')
        backup_folder = os.path.join(backup_folder, date.strftime(date.today(), '%Y%m%d'))

        if not os.path.exists(tmp_folder):
            os.mkdir(tmp_folder, os.W_OK)
        
        if not os.path.exists(backup_folder):
            os.mkdir(backup_folder, os.W_OK)

        files = os.listdir(input_folder)
        if not any(file.endswith(".txt") for file in files):
            print("%s has no txt file", input_folder)
            return

        # all txt move to temp folder
        MoveFiles(input_folder, tmp_folder)

        MergeFiles(tmp_folder, output_filename)

        MoveFiles(tmp_folder, backup_folder)
        
    except Exception as err : #Exception error
        err_type = err.__class__.__name__ # 取得錯誤的class 名稱
        info = err.args[0] # 取得詳細內容
        detains = traceback.format_exc() # 取得完整的tracestack
        n1, n2, n3 = sys.exc_info() #取得Call Stack
        lastCallStack =  traceback.extract_tb(n3)[-1] # 取得Call Stack 最近一筆的內容
        fn = lastCallStack [0] # 取得發生事件的檔名
        lineNum = lastCallStack[1] # 取得發生事件的行數
        funcName = lastCallStack[2] # 取得發生事件的函數名稱
        errMesg = f"FileName: {fn}, lineNum: {lineNum}, Fun: {funcName}, reason: {info}, trace:\n {traceback.format_exc()}"
        print("Fail: "+errMesg)


if __name__ == "__main__":
    main(sys.argv[1:])
