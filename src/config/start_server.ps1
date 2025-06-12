Start-Process -WindowStyle Hidden -WorkingDirectory "E:\Project\chatbot" -FilePath "cmd.exe" -ArgumentList "/c", "uvicorn src.main:app --host 0.0.0.0 --port 8080"
