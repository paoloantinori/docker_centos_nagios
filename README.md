Readme
-----------

https://github.com/paoloantinori/dockercentosnagios  
https://index.docker.io/u/pantinor/centos-nagios-jmx/


##### description

Centos based container that provides Nagios + plugins and sample configuration and scripts to monitor Java Application Servers/Container(JBoss AS, Fuse ESB, Tomcat...) via JMX over HTTP using jolokia.

- Installs nagios through EPEL repository
- Installs perl4jmx nagios plugin to monitor JMX based java application
- Provide sample nagios checks for perl4jmx
- Installs a perl script to debug nagios custom commands

##### build 
    # you can skip this and download the image directly from Docker public registry
    # https://index.docker.io/u/pantinor/centos-nagios-jmx/
    docker build -t pantinor/centos-nagios-jmx .

##### run
    docker run -i -t -p 11111:80 pantinor/centos-nagios-jmx

##### nagios test
    curl -u nagiosadmin:nagiosadmin http://127.0.0.1:11111/nagios/
    # it could be that you need to open some port on your host firewall,
    # ex. 
    # sudo iptables -A INPUT -p tcp  --dport 8012 -j ACCEPT


##### check_p4jmx test
    /usr/local/bin/check_jmx4perl --user=admin --password=admin \
        -u http://172.17.42.1:8012/jolokia \
        --alias MEMORY_HEAP_USED \
        --base MEMORY_HEAP_MAX \
        --warning 80 \
        --critical 90

##### j4psh test
    j4psh --user admin --password admin http://172.17.42.1:8012/jolokia
    
##### configuration
[/etc/nagios/conf.d/commands_p4jmx.cfg](https://github.com/paoloantinori/docker_centos_nagios/blob/master/nagios_conf/commands_p4jmx.cfg)  
[/etc/nagios/conf.d/services.cfg](https://github.com/paoloantinori/docker_centos_nagios/blob/master/nagios_conf/services.cfg)  
`/var/log/nagios/spool` - working folder for `check_bundle_by_name.py` plugin
