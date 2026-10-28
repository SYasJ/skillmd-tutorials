# Check 03 (Windows) — list the signer of EVERY .exe and .dll in a downloaded folder (unzipped, BEFORE you run anything).
# A real vendor installer is normally one signed file. A ZIP with Setup.exe plus DLLs that are unsigned,
# or signed by someone else, is the Yoba pattern (signed Setup.exe sideloading a malicious winmm.dll).
# NOTE: written for this episode, NOT run on camera (we recorded on a Mac).
# usage (PowerShell): .\check-signatures-windows.ps1 -Path C:\Users\you\Downloads\something-setup
param([Parameter(Mandatory=$true)][string]$Path)
Get-ChildItem -Path $Path -Recurse -Include *.exe,*.dll |
  Get-AuthenticodeSignature |
  Select-Object Status, @{n='Signer';e={$_.SignerCertificate.Subject}}, Path |
  Format-Table -AutoSize -Wrap
