# Read version.yaml
$versionFile = "version.yaml"
$yaml = Get-Content $versionFile

$major = ($yaml | Select-String '^major:').ToString().Split(':', 2)[1].Trim()
$minor = ($yaml | Select-String '^minor:').ToString().Split(':', 2)[1].Trim()
$patch = ($yaml | Select-String '^patch:').ToString().Split(':', 2)[1].Trim()

$match = $yaml | Select-String '^name:'
$name = if ($match) { $match.ToString().Split(':', 2)[1].Trim() } else { "" }

if ([string]::IsNullOrWhiteSpace($name)) {
    $version = "$major.$minor.$patch"
} else {
    $version = "$major.$minor.$patch.$name"
}

Write-Host "Building Echo_Replay version $version"


# Build EXE manually
pyinstaller --onefile --windowed `
  --name Echo_Replay `
  --hidden-import pystray `
  --hidden-import PIL `
  --hidden-import playsound `
  --add-data "media;media" `
  --add-data "config.json;."`
  --icon "media/icon.ico" `
  src\main.py


# Build installer
iscc "/DAppVersion=$version" "installer.iss"