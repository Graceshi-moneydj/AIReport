# AIReport
GPT報告轉檔

## mergefile
### Purpose
把GPT報告產生的txt合併成一份檔案
### Usage
```
mergefile.py -f<input folder> -o<output file> -b<backup folder>
```
#### 參數說明
f: GPT報告所有txt檔案  
o: 合併後的檔案  
b: 備份目錄  
### Sample
```
mergefile.py -f\\s-vcfs02\dbdata\AI_report\ -o\\s-vcfs02\dbdata\AI_report\temp\all_report.txt -b\\s-vcfs02\dbdata\AI_report\backup\
```

## 轉檔相關
排程: [s-daily8] Import_AIReport 
時間:每週一~五 12:15 18:15
* batch: \\s-daily8\AIReport\run.bat
* log: \\s-daily8\AIReport\log\
* source:\\s-vcfs02\dbdata\AI_report  (大約12:00 18:00前會更新)
* backup:\\s-vcfs02\dbdata\AI_report\backup
* Batch流程:
  - mergefile把\\s-vcfs02\dbdata\AI_report的txt檔合併成all_report.txt, 並備份到\\s-vcfs02\dbdata\AI_report\backup\
  - all_report.txt先轉到s-db35
  - 用bcp out匯出 s-db35 JDTWS..tmpAI_report 放在\\s-vcfs02\dbdata\BCP\tmpAI_report.csv
  - 更新s-db35的ExpireTime
  - bcp in tmpAI_report.csv到各台DB
  - 更新各台ExpireTime

## DB相關
* Table: JDTWS..AI_report  
* spj 
  JDTWS..spj_add_AI_report --更新s-db35
  JDTWS..spj_sync_AI_report --更新XQDBs(no s-db35)
  JDTWS..spj_JS000032 --給前端

## Expire相關
exec JDAQ..[spj_JQExpireTime] 'TWAI','Y','N'
exec JDAQ..[spj_JQExpireTimeXS] 'TWAI','Y','N'

## 監控
資料監控: Monitordata results - Dataitem: 台股AI Report
Log監控: [s-daily3] C:\Mon\CheckTLogs.bat

## 維運相關
### 檔案跑失敗處理
1.從 "\\s-vcfs02\dbdata\AI_report\backup\日期\" 底下
   把失敗的檔案放到 \\s-vcfs02\dbdata\AI_report\
2.執行\\s-daily8\AIReport\run.bat即可

### sqlscript
script:\\j-nas01\db_admins\dev\20240419_AIReport\script.sql

### 文件
https://docs.google.com/document/d/1BZ0G9Zj7Hm_mmDzvN8HdHmXPrrU1weZN/edit
https://docs.google.com/spreadsheets/d/1Zese6hAIcewqn22Gule3vaPmqn68M6VN46kDnIuyYbA/edit#gid=2072330034
