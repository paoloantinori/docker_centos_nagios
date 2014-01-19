Dockerfiles
-----------

##### build
    docker build -t pantinor/centos_nagios .

##### run
    docker run -i -t -p 127.0.0.1:11111:80 pantinor/centos_nagios

##### nagios test
    curl -u nagiosadmin:nagiosadmin http://127.0.0.1:11111/nagios/
    
##### check_p4jmx
    /usr/local/bin/check_jmx4perl --user=admin --password=admin -u http://10.21.21.253:8012/jolokia --alias MEMORY_HEAP_USED --base MEMORY_HEAP_MAX --warning 80 --critical 90