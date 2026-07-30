pyinstaller --onefile --windowed ^
  --hidden-import pystray ^
  --hidden-import PIL ^
  --hidden-import playsound ^
  --add-data "media;media" ^
  --icon "media/icon.ico" ^
  src\main.py