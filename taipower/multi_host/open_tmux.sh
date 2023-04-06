#!/bin/bash
tmux new-session -s $1			\; \
split-window -h  			\; \
split-window -h  			\; \
select-layout even-horizontal 		\; \
select-pane  -t 0 			\; \
split-window -v -p 50 			\; \
select-pane  -t 0 			\; \
split-window -v -p 50 			\; \
select-pane  -t 2 			\; \
split-window -v -p 50 			\; \
select-pane  -t 4 			\; \
split-window -v -p 67 			\; \
select-pane  -t 5			\; \
split-window -v -p 50 			\; \
select-pane  -t 6			\; \
split-window -h				\; \
select-pane  -t 5			\; \
split-window -h 			\; \
select-pane  -t 9			\; \
split-window -v -p 67			\; \
select-pane  -t 10			\; \
split-window -v -p 50 			\; \
select-pane  -t 11			\; \
split-window -h				\; \
select-pane  -t 10			\; \
split-window -h				\; \
select-pane  -t 9			\; \
split-window -h
#select-layout even-vertical \; \


