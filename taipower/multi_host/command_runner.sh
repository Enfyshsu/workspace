#!/bin/bash
session=$1
window=${session}:0

echo "Current window: $window"

for _pane in $(tmux list-panes -F '#P'); do
    tmux send-keys -t ${_pane} C-l
done

# e1
pane=${window}.0
tmux send-keys -t "$pane" 'attsg e1' C-m
tmux send-keys -t "$pane" 'iperf3 -s' C-m

# e9
pane=${window}.4
tmux send-keys -t "$pane" 'attsg e9' C-m
tmux send-keys -t "$pane" 'iperf3 -c 10.0.1.201 -t 180' C-m

# e8
pane=${window}.1
tmux send-keys -t "$pane" 'attsg e8' C-m
tmux send-keys -t "$pane" 'python3 /latencyTest/receiver.py -t XMPP' C-m

# d2
pane=${window}.2
tmux send-keys -t "$pane" 'attsg d2' C-m
tmux send-keys -t "$pane" 'python3 /latencyTest/receiver.py -t DNP3' C-m

# v2
pane=${window}.3
tmux send-keys -t "$pane" 'attsg v2' C-m
tmux send-keys -t "$pane" 'python3 /latencyTest/receiver.py -t UDP' C-m

# e2
pane=${window}.9
tmux send-keys -t "$pane" 'attsg e2' C-m
tmux send-keys -t "$pane" 'python3 /latencyTest/transmitter.py -t XMPP -st 10 -lt 120 -a 10.0.3.208' C-m

# e3
pane=${window}.10
tmux send-keys -t "$pane" 'attsg e3' C-m
tmux send-keys -t "$pane" 'python3 /latencyTest/transmitter.py -t XMPP -st 10 -lt 120 -a 10.0.3.208' C-m

# e4
pane=${window}.11
tmux send-keys -t "$pane" 'attsg e4' C-m
tmux send-keys -t "$pane" 'python3 /latencyTest/transmitter.py -t XMPP -st 10 -lt 120 -a 10.0.3.208' C-m

# e5
pane=${window}.12
tmux send-keys -t "$pane" 'attsg e5' C-m
tmux send-keys -t "$pane" 'python3 /latencyTest/transmitter.py -t XMPP -st 10 -lt 120 -a 10.0.3.208' C-m

# e6
pane=${window}.13
tmux send-keys -t "$pane" 'attsg e6' C-m
tmux send-keys -t "$pane" 'python3 /latencyTest/transmitter.py -t XMPP -st 10 -lt 120 -a 10.0.3.208' C-m

# e7
pane=${window}.14
tmux send-keys -t "$pane" 'attsg e7' C-m
tmux send-keys -t "$pane" 'python3 /latencyTest/transmitter.py -t XMPP -st 10 -lt 120 -a 10.0.3.208' C-m

# d1
pane=${window}.5
tmux send-keys -t "$pane" 'attsg d1' C-m
tmux send-keys -t "$pane" 'python3 /latencyTest/transmitter.py -t DNP3 -st 20 -lt 60 -a 10.0.2.212' C-m

# d3
pane=${window}.6
tmux send-keys -t "$pane" 'attsg d3' C-m
tmux send-keys -t "$pane" 'python3 /latencyTest/transmitter.py -t DNP3 -st 20 -lt 60 -a 10.0.2.212' C-m

# v1
pane=${window}.7
tmux send-keys -t "$pane" 'attsg v1' C-m
tmux send-keys -t "$pane" 'python3 /latencyTest/transmitter.py -t UDP -st 40 -lt 100 -a 10.0.2.222' C-m

# v3
pane=${window}.8
tmux send-keys -t "$pane" 'attsg v3' C-m
tmux send-keys -t "$pane" 'python3 /latencyTest/transmitter.py -t UDP -st 40 -lt 100 -a 10.0.2.222' C-m