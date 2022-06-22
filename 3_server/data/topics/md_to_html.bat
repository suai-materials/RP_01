@echo off
set /A num = 1
for /R %%f in (*.md) do (
    pandoc %%f -o _html\%num%.html
    SET /A num = %num% + 1
)
