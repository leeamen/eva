#!/bin/sh 
filename=$1
tmp=/tmp/convert.tmp.$$
echo $tmp
iconv -f gbk -t utf-8 $filename > $tmp
sed 's///g' $tmp > $tmp.$$
cp -f $tmp.$$  ./${filename}.utf8
rm -f $tmp.$$
rm -f $tmp
