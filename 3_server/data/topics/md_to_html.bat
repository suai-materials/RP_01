@echo off
set /A num = 1

setlocal ENABLEDELAYEDEXPANSION

:: Преобразование всех .md файлов в .html
for /R %%f in (*.md) do (
    pandoc "%%f" --mathjax -o _html\!num!.html
    echo !num!.html
    SET /A num+=1
)
