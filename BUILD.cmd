pyinstaller --onefile --windowed --name "trener szpilek" --icon="resources/skull.ico" main.py
copy resources "dist/resources" /y
copy README.md dist /y
copy LICENSE.txt dist /y