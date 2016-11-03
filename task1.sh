#!/bin/sh

ls ./data/*.txt|sed 's/ /\n/'|while read row; do python gen_result_xml.py "$row"; done
