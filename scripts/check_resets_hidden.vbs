Set shell = CreateObject("WScript.Shell")

project = "C:\Projects\personal-skills"
python = "C:\Users\rmesq\AppData\Local\Programs\Python\Python314\python.exe"
script = project & "\scripts\check_resets.py"

command = "cmd.exe /c cd /d " & Chr(34) & project & Chr(34) & " && " & Chr(34) & python & Chr(34) & " " & Chr(34) & script & Chr(34)

shell.Run command, 0, False
