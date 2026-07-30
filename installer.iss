[Setup]
AppName=Echo_Replay
AppVersion={#AppVersion}
DefaultDirName={autopf}\Echo_Replay
DisableDirPage=no
DefaultGroupName=Echo_Replay
OutputDir=installer
OutputBaseFilename=Echo_ReplaySetup
Compression=lzma
SolidCompression=yes
SetupIconFile=media\icon.ico

[Code]
var
  ClipDirPage: TInputDirWizardPage;

function IsOBSInstalled(): Boolean;
begin
  Result :=
    FileExists(ExpandConstant('{autopf}\obs-studio\bin\64bit\obs64.exe')) or
    FileExists(ExpandConstant('{pf}\obs-studio\bin\64bit\obs64.exe')) or
    RegKeyExists(HKLM, 'SOFTWARE\OBS Studio') or
    RegKeyExists(HKLM, 'SOFTWARE\WOW6432Node\OBS Studio');
end;

function InitializeSetup(): Boolean;
begin
  Result := True;
  if not IsOBSInstalled() then
  begin
    if MsgBox(
      'OBS Studio was not detected. Echo_Replay requires OBS Studio. Continue anyway?',
      mbConfirmation,
      MB_YESNO
    ) = IDNO then
    begin
      Result := False;
    end;
  end;
end;

procedure InitializeWizard();
begin
  ClipDirPage := CreateInputDirPage(
    wpSelectDir,
    'Echo Replay Output Folder',
    'Choose where clips should be saved:',
    'Select the folder where Echo Replay will store recordings.',
    True,
    'Clips'
  );
  ClipDirPage.Add(ExpandConstant('{userdocs}') + '\Videos\Echo Replay');
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  ConfigPath: String;
  ConfigAnsi: AnsiString;
  Config: String;
  OutputFolder: String;
  ReplaceCount: Integer;
begin
  if CurStep = ssPostInstall then
  begin
    ConfigPath := ExpandConstant('{app}\config.json');
    if FileExists(ConfigPath) then
    begin
      LoadStringFromFile(ConfigPath, ConfigAnsi);
      Config := String(ConfigAnsi);
      OutputFolder := ClipDirPage.Values[0];
      ReplaceCount := StringChangeEx(OutputFolder, '\', '\\', False);
      ReplaceCount := StringChangeEx(
        Config,
        '"output_directory": "output_directory_path"',
        '"output_directory": "' + OutputFolder + '"',
        False
      );
      ConfigAnsi := AnsiString(Config);
      SaveStringToFile(ConfigPath, ConfigAnsi, False);
    end;
  end;
end;

[Files]
Source: "dist\Echo_Replay.exe"; DestDir: "{app}"
Source: "config.json"; DestDir: "{app}" 
Source: "media\*"; DestDir: "{app}\media"; Flags: recursesubdirs


[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"
Name: "startup"; Description: "Start Echo_Replay when Windows starts"


[Registry]
Root: HKCU; \
Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; \
ValueType: string; \
ValueName: "Echo_Replay"; \
ValueData: """{app}\Echo_Replay.exe"""; \
Tasks: startup


[Icons]
Name: "{group}\Echo_Replay"; Filename: "{app}\Echo_Replay.exe"
Name: "{commondesktop}\Echo_Replay"; Filename: "{app}\Echo_Replay.exe"; Tasks: desktopicon


[Run]
Filename: "powershell.exe"; \
Parameters: "-NoProfile -ExecutionPolicy Bypass -Command ""Write-Host 'Echo_Replay installed'"""; \
Flags: runhidden

Filename: "{app}\Echo_Replay.exe"; \
Description: "Launch Echo_Replay"; \
Flags: nowait postinstall skipifsilent