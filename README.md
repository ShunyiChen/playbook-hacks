
*******
PLAYBOOK HACKS
*******

PLAYBOOK HACKS is a automation platform that makes your applications and
system easiter to do Data Collection(CPU,Memory,HC reports,etc) or Health Check from remote servers.
Avoid writing scripts or custom code to update your applications, And then 
all this is now left to be implemented by the yaml file - PLAYBOOK file.


Health Check Example
=======
Customize a playbook: 
<pre>
<code>  
- name: example 
  hosts: all 
  gather_facts: no 
  become: yes 
  tasks: 
    - name: connect over ssh
      open_ssh:
        host: 10.10.10.10
        usr: root
        passwd: cDe3@wsx0n
      timeout: timeout_quit
  
    - name: ssh -i /root/.ssh/5g_lab_key eccd@10.221.221.221
      invoke_shell:
        cmd: ssh -i /root/.ssh/5g_lab_key eccd@10.221.221.221
      timeout: timeout_quit

    - name: kubectl exec -n pcc1 -ti eric-pc-mm-controller-0 -- tcsh
      invoke_shell:
              cmd: kubectl exec -n pcc1 -ti eric-pc-mm-controller-0 -- tcsh
      register: return_value

    - name: Check 1
      quit_procedure:  
      when:  return_value.endswith(('=== rp-pcc-1 root@eric-pc-mm-controller-0 ANCB / *# '))

    - name: su system_admin
      invoke_shell:
        cmd: su system_admin
      register: return_value

    - name: Check 2
      quit_procedure:  
      when:  return_value.endswith(('=== rp-pcc-1 system_admin@eric-pc-mm-controller-0 ANCB / *# '))

    - name: health_check.pl -l
      invoke_shell:
        cmd: health_check.pl -l

    - name: quit_shell - exit
      quit_shell:
      register: return_value
    
    - name: Check 3
      quit_procedure:  
      when:  return_value.endswith(('=== rp-pcc-1 root@eric-pc-mm-controller-0 ANCB / *# '))

    - name: quit_shell - logout
      quit_shell:
      register: return_value
 
    - name: Check 4
      quit_procedure:  
      when: return_value.endswith(('eccd@director-0-eccd1:~> '))

    - name: close_channel
      close_channel:
</code>
</pre>

Running the playbook 
=======
<pre>
<code>
cd /playbook-hacks/engine/core  
python3 playbook.py -i ../playbook/healthcheck-example.yaml -o temp.py 
</code>
</pre>
Result:  

![Image text](https://github.com/ShunyiChen/playbook-hacks/blob/master/health_check_example.png)



Authors
=======

PLAYBOOK HACKS was created by `Shunyi Chen`
