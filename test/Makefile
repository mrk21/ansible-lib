.PHONY: units
units:
	python $@/http_wait_for_test.py
	python $@/firebrew_test.py

.PHONY: integration
integration:
	ansible-playbook -v -i $@/inventory.ini $@/site.yml
