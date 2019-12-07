.PHONY: build
build:
	docker build -t forzabarca88/asx_data_api

.PHONY: run
run:
	docker run -d -p 8080:8080 forzabarca88/asx_data_api