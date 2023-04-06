FROM lscr.io/linuxserver/wireshark:latest
MAINTAINER enfyshsu

RUN ["/bin/bash", "-c", "echo 'nameserver 8.8.8.8' > /etc/resolv.conf"]
RUN apk update
RUN apk add --no-cache python3 vim openssh git iperf3
ADD ./config/sshd_config /etc/ssh/sshd_config
RUN apk add --no-cache openrc
RUN apk add py3-pip 
RUN pip3 install scapy

#RUN echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_configi
#RUN adduser -h /home/vivek -s /bin/sh -D vivek
RUN echo -n 'root:test' | chpasswd
COPY ssh_entrypoint.sh /

EXPOSE 22

