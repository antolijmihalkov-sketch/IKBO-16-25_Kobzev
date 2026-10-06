#!/bin/bash

grep -v '^#' /etc/protocols | awk 'NF {print $2, $1}' | sort -nr | head -n 5
