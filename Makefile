#Настройки

PROJECT_NAME = Project #Имя нашей папки проекта
PYTHON = python3  #Или python
PIP = $(PYTHON) -m pip #Путь к pip
DOCS_DIR = docs  #Путь к нашей папке с документацией Sphinx
BUILD_DIR = _build  #Папка для сгенерированной документации

#Цели

.PHONY: help install run docs clean

help: #Выводит список доступных команд
	@echo "Доступные команды:"
	@echo "  install  - Установить зависимости проекта."
	@echo "  run      - Запустить бота."
	@echo "  docs     - Собрать документацию."
	@echo "  clean    - Удалить сгенерированную документацию."

install:
	$(PIP) install -r requirements.txt  #установим все зависимости, перечисленные в файле requirements

run:
	$(PYTHON) $(PROJECT_NAME)/bot.py #имя главного файла

docs: #Переходим в папку docs и запускает sphinx для сборки документации
	cd $(DOCS_DIR) && $(PYTHON) -m sphinx -b html . $(BUILD_DIR)
	@echo "Документация собрана в $(DOCS_DIR)/$(BUILD_DIR)/html"

clean: #Удаляет сгенерированную документацию, чтобы мы могли начать с чистого листа
	rm -rf $(DOCS_DIR)/$(BUILD_DIR)

# Чтобы Makefile  собирал документацию с помощью sphinx-quickstart и sphinx
sphinx:
	cd $(DOCS_DIR) && $(PYTHON) -m sphinx -b html . $(BUILD_DIR)
	@echo "Документация собрана в $(DOCS_DIR)/$(BUILD_DIR)/html"

