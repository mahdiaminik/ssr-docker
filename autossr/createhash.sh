#!/bin/bash
for i in {1..20}
do
   j=$(printf '%s%02d\n' @Bcdef1234 $i)
   k=$(echo $j | md5sum | cut -c-10)
   printf '%02d %s %s\n' $i $k 'username'

done
