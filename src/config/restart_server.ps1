Start-Sleep -Seconds 3
Get-Process -Name uvicorn -ErrorAction SilentlyContinue | ForEach-Object { $_.Kill() }
Start-Process "uvicorn" "src.main:app --host 0.0.0.0 --port 8080"
