.DEFAULT_GOAL := units

.PHONY: units
units:
	python $@.py $(subst :, ,$f)

.PHONY: integration
integration:
	ansible-playbook -v -i $@/inventory.ini $@/site.yml $(if $t, -t $t,)
