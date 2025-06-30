windows:
	powershell -Command "$$env:PYTHONPATH = './'; poetry run python ./napcrawler/app.py"

mac:
	PYTHONPATH="./" poetry run python ./napcrawler/app.py
