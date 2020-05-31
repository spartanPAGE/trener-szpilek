pyinstaller --onefile --windowed --name "trener szpilek" --icon="resources/skull.ico" main.py
xcopy resources "dist\resources\" /S /E /Y
copy README.md dist /Y
copy LICENSE.txt dist /y