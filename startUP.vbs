Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "cmd /c startUP.bat"
oShell.Run strArgs, 0, false