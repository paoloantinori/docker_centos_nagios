Dockerfiles
-----------

##### build
    docker build -t pantinor/centos_nagios github.com/paoloantinori/docker_centos_nagios

##### run
    docker run -i -t -p 127.0.0.1:11111:80 pantinor/centos_nagios

##### test
    curl -u nagiosadmin:nagiosadmin http://127.0.0.1:11111/nagios/
