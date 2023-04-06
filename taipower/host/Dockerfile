FROM lscr.io/linuxserver/wireshark:latest
MAINTAINER enfyshsu

RUN ["/bin/bash", "-c", "echo 'nameserver 8.8.8.8' > /etc/resolv.conf"]
RUN ["/bin/bash", "-c", "touch /root/.bashrc"]
RUN ["/bin/bash", "-c", "echo 'export LD_LIBRARY_PATH=/usr/local/lib64' > /root/.bashrc"]
RUN apk update
RUN apk add --no-cache python3 python3-dev vim openssh git iperf3 build-base wget linux-headers g++ gcc cmake make iftop
ADD ./config/sshd_config /etc/ssh/sshd_config
RUN apk add --no-cache openrc
RUN apk add py3-pip 
RUN pip3 install pybind11 swig xmpppy numpy

# install pydnp3
WORKDIR /
RUN git clone --recursive http://github.com/Kisensum/pydnp3
WORKDIR /pydnp3
RUN python3 setup.py install
WORKDIR /
RUN rm -r pydnp3/

# build libiec61850
RUN git clone https://github.com/mz-automation/libiec61850.git
WORKDIR /libiec61850
RUN cmake -DBUILD_PYTHON_BINDINGS=ON .
RUN make install
WORKDIR /

#RUN echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_configi
#RUN adduser -h /home/vivek -s /bin/sh -D vivek
RUN echo -n 'root:test' | chpasswd
COPY ssh_entrypoint.sh /

EXPOSE 22

