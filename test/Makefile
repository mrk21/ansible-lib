.PHONY: unit
unit:
	python $@/http_wait_for_test.py

.PHONY: integration
integration:
	ANSIBLE_LIBRARY=/usr/share/ansible:../library ansible-playbook -i $@/inventory.ini $@/site.yml
