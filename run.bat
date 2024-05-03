set filePath=\\s-daily8\AIReport\
set sourcePath=\\s-vcfs02\dbdata\AI_report\
set backupPath=%sourcePath%backup\
set tempPath=%sourcePath%temp\
set logPath=%filePath%log\

set SQLUser=FileAdmin
set SQLPWD=FileAdmin466e

py %filePath%mergefile.py -f%sourcePath% -o%tempPath%all_report.txt -b%backupPath% > %logPath%mergefile.log

if exist "%tempPath%all_report.txt" (

	sqlcmd -S S-DB35 -U %SQLUser% -P %SQLPWD% -Q "exec JDTWS..spj_add_AI_Report '%tempPath%all_report.txt'" -o "%logPath%ImportAIReport_S-DB35.log"
	sqlcmd -S S-DB35 -U %SQLUser% -P %SQLPWD% -Q "exec Serializer..spj_Update_ImportDataTime 'TWAI',0"


	bcp JDTWS..tmpAI_report out \\s-vcfs02\dbdata\BCP\tmpAI_report.csv -N -SS-DB35 -U%SQLUser% -P%SQLPWD%


	sqlcmd -S S-DB30 -U %SQLUser% -P %SQLPWD% -Q "exec JDTWS..spj_sync_AI_Report 'z:\s-vcfs02\dbdata\BCP\tmpAI_report.csv'" -o "%logPath%ImportAIReport_S-DB30.log"
	sqlcmd -S S-DB30 -U FileAdmin -P FileAdmin466e -Q "exec Serializer..spj_Update_ImportDataTime 'TWAI',0"

	sqlcmd -S S-DB37 -U %SQLUser% -P %SQLPWD% -Q "exec JDTWS..spj_sync_AI_Report 'z:\s-vcfs02\dbdata\BCP\tmpAI_report.csv'" -o "%logPath%ImportAIReport_S-DB37.log"
	sqlcmd -S S-DB37 -U FileAdmin -P FileAdmin466e -Q "exec Serializer..spj_Update_ImportDataTime 'TWAI',0"

	sqlcmd -S S-DB29 -U %SQLUser% -P %SQLPWD% -Q "exec JDTWS..spj_sync_AI_Report 'z:\s-vcfs02\dbdata\BCP\tmpAI_report.csv'" -o "%logPath%ImportAIReport_S-DB29.log"
	sqlcmd -S S-DB29 -U FileAdmin -P FileAdmin466e -Q "exec Serializer..spj_Update_ImportDataTime 'TWAI',0"

	sqlcmd -S T-DB20 -U %SQLUser% -P %SQLPWD% -Q "exec JDTWS..spj_sync_AI_Report 'z:\s-vcfs02\dbdata\BCP\tmpAI_report.csv'" -o "%logPath%ImportAIReport_T-DB20.log"
	sqlcmd -S T-DB20 -U FileAdmin -P FileAdmin466e -Q "exec Serializer..spj_Update_ImportDataTime 'TWAI',0"

	sqlcmd -S T-DB21 -U %SQLUser% -P %SQLPWD% -Q "exec JDTWS..spj_sync_AI_Report 'z:\s-vcfs02\dbdata\BCP\tmpAI_report.csv'" -o "%logPath%ImportAIReport_T-DB21.log"
	sqlcmd -S T-DB21 -U FileAdmin -P FileAdmin466e -Q "exec Serializer..spj_Update_ImportDataTime 'TWAI',0"

	sqlcmd -S T-DB25 -U %SQLUser% -P %SQLPWD% -Q "exec JDTWS..spj_sync_AI_Report 'z:\s-vcfs02\dbdata\BCP\tmpAI_report.csv'" -o "%logPath%ImportAIReport_T-DB25.log"
	sqlcmd -S T-DB25 -U FileAdmin -P FileAdmin466e -Q "exec Serializer..spj_Update_ImportDataTime 'TWAI',0"


del /F %tempPath%all_report.txt
)
exit