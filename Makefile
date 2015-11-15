unit_test_modules = $(shell find tests/unit_tests -name "*_test.py")
integration_test_modules = $(shell find tests/integration_tests -name "*_test.py")
whodat_modules = $(shell find src -name "*.py")

# $(call test_judge,cmd,ret)
define test_judge
ifeq ($2,0)
	expression = "\033[32m$1\033[m"
else
	expression = "\033[31m$1\033[m"
endif
endef

# $(call pylint_judge,cmd,ret)
define pylint_judge
ifeq ($2,0)
	expression = "\033[32m$1\033[m"
else
	expression = "\033[31m$1\033[m"
endif
endef

# $(call run_test,cmd)
define run_test
$(eval RET := $(shell python $1 2> /dev/null; echo $$?))
$(eval $(call test_judge,$1,$(RET)))
@echo $(expression)
endef

# $(call run_pylint,cmd)
define run_pylint
$(eval RET := $(shell pylint --max-line-length=120 --rcfile=.pylintrc $1 2> /dev/null; echo $$?))
$(eval $(call pylint_judge,$1,$(RET)))
@echo $(expression)
endef

.PHONY: all pylint integration_test unit_test

all: setUp pylint unit_test integration_test tearDown

setUp:
	python scripts/whodat_admin.py runserver -P tests/integration_tests/src 2> /dev/null &

pylint:
	$(info ==================================== Pylint ====================================)
	$(foreach one, $(whodat_modules), $(call run_pylint,$(one)))
	$(foreach one, $(unit_test_modules), $(call run_pylint,$(one)))
	$(foreach one, $(integration_test_modules), $(call run_pylint,$(one)))
	@echo ""

unit_test:
	$(info ================================== Unit tests ==================================)
	$(foreach one, $(unit_test_modules), $(call run_test,$(one)))
	@echo ""

integration_test:
	$(info ============================== Integration tests ===============================)
	$(foreach one, $(integration_test_modules), $(call run_test,$(one)))
	@echo ""

tearDown:
	pkill python
