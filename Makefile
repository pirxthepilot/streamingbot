PROJECT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

export PKGTMP_DIR 		:= $(PROJECT_DIR)/pkgtmp
export LAMBDA_FUNC_FILE := $(PROJECT_DIR)/bot.py
export ZIP_FILE 		:= $(PROJECT_DIR)/package.zip


.PHONY: typecheck
typecheck:
	mypy --ignore-missing-imports streamingbot

.PHONY: lint
lint:
	pylint streamingbot

.PHONY: test-all
test-all: typecheck lint

.PHONY: package
package:
	@./support/package.sh

.PHONY: plan
plan:
	cd terraform &&\
	terraform plan -var-file=config.tfvars -var 'lambda_package=$(ZIP_FILE)'

.PHONY: deploy
deploy:
	cd terraform &&\
	terraform apply -var-file=config.tfvars -var 'lambda_package=$(ZIP_FILE)' -auto-approve

.PHONY: logtail
logtail:
	awslogs get /aws/lambda/streamingbot --timestamp --watch
