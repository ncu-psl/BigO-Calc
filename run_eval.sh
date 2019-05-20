for entry in "challenge"/*.c
do
	echo $entry
	python3 bigo_calc.py $entry C
	echo
done
