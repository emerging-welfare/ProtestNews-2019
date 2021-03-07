#!/bin/bash
data_path=$(pwd)
cd ../collector

if [ ! -d tmp ]; then
    mkdir tmp
fi
if [ ! -d tmp/htmls ]; then
    mkdir tmp/htmls
fi
if [ ! -d tmp/texts ]; then
    mkdir tmp/texts
fi
if [ ! -d ../output ]; then
    mkdir ../output
fi
if [ ! -d ../output/Document ]; then
    mkdir ../output/Document
fi

if [ $(ls $data_path/*.json | wc -l) -lt 1 ]; then
    echo "Please copy all shared json files to the folder."
    exit 0
fi

for data_file in $data_path/*.json
do
    json_file=$(echo "$data_file" | sed -r "s/^.*\/(\w+\/\w+)\.json$/\1_filled.json/")
    echo "Working for $data_file"
    if [ -f ../output/$json_file ]; then
       echo "Already done $data_file"
       continue
    fi

    stale_count=0
    file_count=$(ls tmp/htmls | wc -l)
    while [ $stale_count -lt 3 ]; do
	scrapy crawl sp -a filename="$data_file"
	# python3 -W ignore getnews_selenium.py $data_file

	new_file_count=$(ls tmp/htmls | wc -l)
	if [ $new_file_count == $file_count ]; then
	    let "stale_count+=1"
	else
	    file_count=$new_file_count
	fi
    done

    for filename in tmp/htmls/http*
    do
	ofile=$(echo "$(basename $filename)")
	if [ ! -f tmp/texts/$ofile ]; then
	    if [[ $ofile == *"timesofindia"* ]]; then
		python timesofindia.py $ofile
	    elif [[ $ofile == *"newindianexpress"* ]]; then
		python newindianexpress.py $ofile
	    elif [[ $ofile == *"indianexpress"* ]]; then
		python indianexpress.py $ofile
	    elif [[ $ofile == *"thehindu"* ]]; then
		python thehindu.py $ofile
	    elif [[ $ofile == *"scmp"* ]]; then
		python scmp.py $ofile
	    elif [[ $ofile == *"estadao"* ]]; then
		python estadao.py $ofile
	    elif [[ $ofile == *"pagina12"* ]]; then
		python pagina12.py $ofile
	    elif [[ $ofile == *"clarin"* ]]; then
		python clarin.py $ofile
	    elif [[ $ofile == *"lanacion"* ]]; then
		python lanacion.py $ofile
	    elif [[ $ofile == *"folha"* ]]; then
		python folha.py $ofile
	    elif [[ $ofile == *"people"* ]]; then
		python people.py $ofile
	    else
		echo "No idea what source : $ofile"
	    fi
	fi
    done

    python3 -W ignore $data_path/fill_in_blanks.py $data_file
done
