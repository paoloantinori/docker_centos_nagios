Readme
-----------

https://github.com/paoloantinori/dockercentosnagios


##### description
- Installs nagios through EPEL repository
- Installs perl4jmx nagios plugin to monitor JMX based java application
- Provide sample nagios checks for perl4jmx
- Installs a perl script to debug nagios custom commands


##### build
    docker build -t pantinor/centos-nagios-jmx .

##### run
    docker run -i -t -p 11111:80 pantinor/centos-nagios-jmx

##### nagios test
    curl -u nagiosadmin:nagiosadmin http://127.0.0.1:11111/nagios/
    # it could be that you need to open some port on your host firewall, ex. sudo iptables -A INPUT -p tcp  --dport 8012 -j ACCEPT

##### check_p4jmx test
    /usr/local/bin/check_jmx4perl --user=admin --password=admin -u http://172.17.42.1:8012/jolokia --alias MEMORY_HEAP_USED --base MEMORY_HEAP_MAX --warning 80 --critical 90

##### j4psh test
    j4psh --user admin --password admin http://172.17.42.1:8012/jolokia
