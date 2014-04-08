ansible-lib
===========

Ansible module libraries.

Modules
==========

## http_wait_for

### Parameters

* **host**: Hostname [default: 127.0.0.1]
* **port**: Port [default: 80 or 443]
* **path**: Path [default: /]
* **ssl**: Using SSL [default: no]
* **status**: OK status [default: 200]
* **interval**: Access interval (sec) [default: 3]
* **timeout**: Time out (sec) [default: 60]

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
