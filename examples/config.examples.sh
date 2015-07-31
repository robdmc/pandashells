#! /usr/bin/env bash

# p.config 
p.config > /dev/null
p.config --io_input_header noheader --io_input_type table > /dev/null
p.config --io_output_header noheader --io_output_type table > /dev/null
p.config --force_defaults > /dev/null

