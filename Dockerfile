FROM centos

MAINTAINER Paolo Antinori <pantinor@redhat.com>

RUN yum -y install http://download.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm
RUN yum -y install nagios nagios-common nagios-plugins nagios-plugins-by_ssh nagios-plugins-disk nagios-plugins-http nagios-plugins-load nagios-plugins-nagios nagios-plugins-perl nagios-plugins-ping nagios-plugins-procs nagios-plugins-ssh nagios-plugins-swap nagios-plugins-users
RUN yum -y install perl-Class-Accessor perl-common-sense perl-Config-Tiny perl-Crypt-Blowfish_PP perl-ExtUtils-CBuilder perl-ExtUtils-ParseXS perl-File-BaseDir perl-JSON perl-JSON-Any perl-JSON-XS perl-Math-Calc-Units perl-Module-Build perl-Module-Find perl-Nagios-Plugin perl-Term-ShellUI perl-Config-General perl-Test-Simple perl-Time-HiRes perl-Sys-SigAction

RUN service httpd start ; service nagios start

ADD http://search.cpan.org/CPAN/authors/id/R/RO/ROLAND/jmx4perl-1.07.tar.gz /root/

RUN tar -xvf /root/jmx4perl* -C /root
# change default values
RUN awk '/\$msg,"y"/{c+=1;done=0}{if(done==0 && (c>2) ){sub("\"y\"","\"n\"",$0);done=1};print}' /root/jmx4perl-1.07/Build.PL > /root/jmx4perl-1.07/BuildAnswered.PL
RUN cd /root/jmx4perl-1.07 ; PERL_MM_USE_DEFAULT=1 perl /root/jmx4perl-1.07/BuildAnswered.PL
RUN cd /root/jmx4perl-1.07 ; /root/jmx4perl-1.07/Build test
RUN cd /root/jmx4perl-1.07 ; /root/jmx4perl-1.07/Build install
#RUN rm /root/jmx4perl-1.07* -rf
RUN sed -i s/+epn/-epn/g /usr/local/bin/check_jmx4perl

ADD http://www.waggy.at/nagios/capture_plugin.txt /etc/nagios/capture_plugin.pl
RUN chmod 0755 /etc/nagios/capture_plugin.pl


RUN htpasswd -bc /etc/nagios/passwd nagiosadmin nagiosadmin
RUN chmod -R a+rwx /var/log/nagios /var/spool/nagios/cmd/

ADD . /bin
RUN chmod +x /bin/startNagios.sh

EXPOSE  80
CMD ["/bin/startNagios.sh"]

