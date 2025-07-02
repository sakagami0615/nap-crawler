
OUTPUT_PATH ?= .crawl_data
OUTPUT_TYPE ?= HTML
WAIT_TIME_SEC ?= 1
HEADLESS ?= True
LOG_LEVEL ?= INFO

windows:
	powershell -Command "$$env:PYTHONPATH = './'; poetry run python ./napcrawler/app.py $(OUTPUT_PATH) -t $(OUTPUT_TYPE) -w $(WAIT_TIME_SEC) --headless $(HEADLESS) --log_level ${LOG_LEVEL}"

mac:
	PYTHONPATH="./" poetry run python ./napcrawler/app.py $(OUTPUT_PATH) -t $(OUTPUT_TYPE) -w $(WAIT_TIME_SEC) --headless $(HEADLESS) --log_level ${LOG_LEVEL}
