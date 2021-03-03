
#!/bin/bash
PATH=$PATH
export PATH
#prepare fifo
#echo -e "hello world!\n"
count=1

if [ ${1} -le  "0"  ]
then
	echo "error, please input number in the right range"
	exit
fi
if [ ${1} -ge  "11" ]
then
	echo "error, please input number in the right range"
	exit
fi
if [ ${2} -le  "7"  ]
then
	echo "error, please input number in the right range"
	exit
fi
if [ ${2} -ge  "13" ]
then
	echo "error, please input number in the right range"
	exit
fi

for a in $(seq 1 ${2})
do
	for b in $(seq $((${a}+1)) ${2})
	do
		for c in $(seq $((${b}+1)) ${2})
	do
		for d in $(seq $((${c}+1)) ${2})
	do
		for e in $(seq $((${d}+1)) ${2})
	do
		for f in $(seq $((${e}+1)) ${2})
	do
		for g in $(seq $((${f}+1)) ${2})
	do
		for h in $(seq $((${g}+1)) ${2})
	do
		all[${count}]=${a}" "${b}" "${c}" "${d}" "${e}" "${f}" "${g}" "${h}
	#	echo ${all[${count}]}
		count=$((${count}+1))
		
	done

	done

	done

	done

	done

	done

	done
done	
count=$((${count}-1))
#echo "now have=" ${count}		

M=${1}
N=${2}
if [ $N == "8" ]
then
	M="1"
fi
if [ $N == "9" ]
then
	if [ $M == "10" ]
	then
		M="9"
	fi
fi
#generate random
for now in $(seq 1 $M)
do
	value=$(($RANDOM+$RANDOM+$(($RANDOM%"2"))))
	table[${now}]=${value}
	#echo "radom number="${table[${now}]}
done

#table[1~n_host] 
mkfifo fifo_0.tmp
for now in $(seq 1 $M)
do
	mkfifo fifo_${now}.tmp
	open="exec "$((${now}+2))"<>fifo_"${now}".tmp"
#	echo $open
	eval $open
	id=$(printf '%d' $((10#${now})))
	key=${id}
	depth=$(printf '%d' $((10#0)))
#	echo "now id=" ${id} ${depth}
	./host ${now} ${table[${now}]} ${depth} &
	echo ${all[${count}]} > fifo_${now}.tmp
	count=$((${count}-1))
	
done

for now in $(seq 1 $N)
do
	score[${now}]=0
done


#generate CN取8
filename="fifo_0.tmp"
exec < $filename
number=${count}


for tmp in $(seq 1 ${number})
do
	for now in $(seq 1 9)
	do
		read line[${now}]
	#	echo ${line[${now}]}
		if [ ${now} != "1" ]
		then
			value=${line[${now}]}
			value2=${line[${now}]}
			player=${value:0:2}
			rank=${value2:2}
	#		echo "now value="$((${player}))"value2="$((${rank}))
			previous=${score[$((10#${player}))]}
			score[$((10#${player}))]=$(($previous + 8))
			previous=${score[$((10#${player}))]}
			score[${player}]=$(($previous - ${rank}))

		fi
	done
	for now in $(seq 1 $M)
	do
		if [ ${table[${now}]} == ${line["1"]} ]
		then
			echo ${all[${count}]}>fifo_${now}.tmp
	#		echo "now host="$now
		fi
	done
	count=$((${count} - 1))
done
for tmp in $(seq 1 $M)
do
	for now in $(seq 1 9)
	do
		read line[${now}]
	#	echo ${line[${now}]}
		if [ ${now} != "1" ]
		then
			value=${line[${now}]}
			value2=${line[${now}]}
			player=${value:0:2}
			rank=${value2:2}
			previous=${score[$((10#${player}))]}
			score[${player}]=$(($previous + 8 - ${rank}))
		fi
	done
done
for tmp in $(seq 1 $N)
do
	echo ${tmp}" "${score[${tmp}]}
done


#send -1 -1 -1 -1 -1 -1\n to all hosts
for now in $(seq 1 $M)
do
	echo "-1 -1 -1 -1 -1 -1 -1 -1">fifo_${now}.tmp
done



#remove FIFO
rm fifo_0.tmp
for now in $(seq 1 $M)
do
	rm fifo_${now}.tmp
done


#wait for all forked process to exit

wait



