; Inno Setup installer script for Exerset
; Download Inno Setup from: https://jrsoftware.org/isdl.php
; Then run: iscc exerset-installer.iss

[Setup]
AppName=Exerset
AppVersion=1.0.0
AppPublisher=Dr. Josh PT
AppPublisherURL=https://www.youtube.com/@DrJoshPT
DefaultDirName={autopf}\Exerset
DefaultGroupName=Exerset
OutputDir=dist\windows
OutputBaseFilename=Exerset-Setup
SetupIconFile=assets\icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
UninstallDisplayIcon={app}\Exerset.exe

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
Name: "startmenushortcut"; Description: "Add to Start Menu"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "dist\windows\Exerset\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Exerset"; Filename: "{app}\Exerset.exe"; WorkingDir: "{app}"
Name: "{group}\{cm:UninstallProgram,Exerset}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Exerset"; Filename: "{app}\Exerset.exe"; Tasks: desktopicon; WorkingDir: "{app}"

[Run]
Filename: "{app}\Exerset.exe"; Description: "{cm:LaunchProgram,Exerset}"; Flags: nowait postinstall skipifsilent

[Code]
procedure InitializeWizard;
begin
  WizardForm.Welcome.Font.Size := 12;
end;
