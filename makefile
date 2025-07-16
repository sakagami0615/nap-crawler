
# デフォルト引数
OUTPUT_PATH ?= .crawl_data
REGION ?= 
OUTPUT_TYPE ?= HTML
WAIT_TIME_SEC ?= 1
HEADLESS ?= True
LOG_LEVEL ?= INFO


# コマンドオプション設定
REGION_OPT := $(if $(strip $(REGION)),-r $(REGION),)
OUTPUT_TYPE_OPT := -t $(OUTPUT_TYPE)
WAIT_TIME_OPT := -w $(WAIT_TIME_SEC)
HEADLESS_OPT := --headless $(HEADLESS)
LOG_LEVEL_OPT := --log_level $(LOG_LEVEL)

# app実行コマンド設定
APP_CMD := poetry run python ./napcrawler/app.py $(OUTPUT_PATH) $(REGION_OPT) $(OUTPUT_TYPE_OPT) $(WAIT_TIME_OPT) $(HEADLESS_OPT) $(LOG_LEVEL_OPT)

# 環境変数 & 実行コマンド設定
# OS: Windows
ifeq ($(OS),Windows_NT)
    OS_TYPE := windows
    ENV_CMD := $$env:PYTHONPATH = './';
    RUN_CMD := powershell -Command "$(ENV_CMD) $(APP_CMD)"
# OS: UNIX
else
    OS_TYPE := unix
    ENV_CMD := PYTHONPATH="./"
    RUN_CMD := $(ENV_CMD) $(APP_CMD)
endif


run:
	@echo "Running on $(OS_TYPE)"
	@echo "command: [ $(RUN_CMD) ]"
	@$(RUN_CMD)

help:
	@echo ------------------------------------------------------------
	@echo Usage
	@echo ------------------------------------------------------------
	@echo [OUTPUT_PATH]
	@echo     Specify the folder to save the downloaded file (default: .crawl_data)
	@echo     (ex) make run OUTPUT_PATH=output_data
	@echo [REGION]
	@echo     Specify the region of the data to crawl (default: crawling all)
	@echo     (ex) make run REGION=tokyo
	@echo          make run REGION=tokyo,kyoto
	@echo          make run REGION=tokyo/izuhichito_ogasawara
	@echo [OUTPUT_TYPE]
	@echo     Specify the format of the downloaded file (default: HTML)
	@echo     (ex) make run OUTPUT_TYPE=HTML
	@echo     (ex) make run OUTPUT_TYPE=Text
	@echo [WAIT_TIME_SEC]
	@echo     Request execution time interval (seconds) (default: 1)
	@echo     (ex) make run WAIT_TIME_SEC=3
	@echo [HEADLESS]
	@echo     Browser headless mode (default: True)
	@echo     (ex) make run HEADLESS=False
	@echo [LOG_LEVEL]
	@echo     Specify the log level of the Logger (default: INFO)
	@echo     (ex) make run LOG_LEVEL=DEBUG
	@echo          make run LOG_LEVEL=WARNING
	@echo          make run LOG_LEVEL=ERROR
	@echo          make run LOG_LEVEL=CRITICAL
