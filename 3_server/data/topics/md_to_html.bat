@echo off
set /A num = 1

setlocal ENABLEDELAYEDEXPANSION


for /R %%f in (*.md) do (
    pandoc "%%f" -o _html\!num!.html
    echo !num!.html
    SET /A num+=1
)
