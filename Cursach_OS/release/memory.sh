#!/bin/bash

for pid in $(ps -ef | awk '{print $2}'); do
    if [ -f /proc/$pid/smaps ]; then
            echo "* Mem usage for PID $pid"
            echo "-- Size:"
            sudo cat /proc/$pid/smaps | grep -m 1 -e ^Size: | awk '{print $2}'
            echo "-- Rss:"
            sudo cat /proc/$pid/smaps | grep -m 1 -e ^Rss: | awk '{print $2}'
            echo "-- Pss:"
            sudo cat /proc/$pid/smaps | grep -m 1 -e ^Pss: | awk '{print $2}'
            echo "Shared Clean"
            sudo cat /proc/$pid/smaps | grep -m 1 -e '^Shared_Clean:' | awk '{print $2}'
            echo "Shared Dirty"
            sudo cat /proc/$pid/smaps | grep -m 1 -e '^Shared Dirty:' | awk '{print $2}'
    fi
done
