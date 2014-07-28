.PHONY: units
units:
	python $@.py

.PHONY: integration
integration:
	ansible-playbook -v -i $@/inventory.ini $@/site.yml
