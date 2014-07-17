ansible-lib
===========

Ansible module libraries.

Modules
==========

## http\_wait\_for

Waits the HTTP request for a condition before continuing.

### Options

| parameter | required | default | choices | comments |
| --------- | -------- | ------- | ------- | ---------|
| host | no | 127.0.0.1 | |  Hostname |
| port | no | 80 or 443 | | Port |
| path | no | / | | Path |
| ssl | no | no | yes, no | Using SSL |
| status | no | 200 | | OK status |
| interval | no | 3 | | Access interval (sec) |
| timeout | no | 60 | | Time out (sec) |

### Examples

Install Jenkins Git Plugin:

```yaml
---
- name: start jenkins server
  command: java -jar jenkins.war
  
- http_wait_for: port=8080 timeout=300
  
- name: install git plugin
  command: java -jar jenkins-cli.jar -s http://127.0.0.1:8080 install-plugin git
  
- name: restart jenkins server
  command: java -jar jenkins-cli.jar -s http://127.0.0.1:8080 safe-restart
  
- http_wait_for: port=8080 timeout=300
```

## firebrew

Manage the Firefox Add-ons.

### Options

| parameter | required | default | choices | comments |
| --------- | -------- | ------- | ------- | ---------|
| name | yes | | | Extension name |
| state | no | present | present, absent | Install or Uninstall |
| base\_dir | no | | | The profiles.ini path |
| profile | no | | | Target profile name |
| firefox | no | | | The Firefox command path |

### Examples

```yaml
---
- name: install Vimperator
  firebrew: name=Vimperator state=present
  
- name: uninstall Japanese Language Pack
  firebrew: name='Japanese Language Pack' state=absent
```
