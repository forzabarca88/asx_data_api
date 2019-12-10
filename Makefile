.PHONY: build
build:
	docker build -t forzabarca/asx_data_api .

.PHONY: run
run:
	docker run -d -p 8080:8080 forzabarca/asx_data_api