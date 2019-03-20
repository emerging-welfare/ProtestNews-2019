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

for data_file in $data_path/*.json
do
    if [[ $data_file == *"_filled.json" ]]; then
	continue
    fi
    echo "Working for $data_file" | tee -a $data_path/log.txt
    scrapy crawl sp -a filename="$data_file"
    python3 -W ignore getnews_selenium.py $data_file

    for filename in tmp/htmls/http*
    do
	ofile=$(echo "$(basename $filename)")
	if [ ! -f tmp/texts/$ofile ]; then
	    if [[ $ofile == *"timesofindia"* ]]; then
		python3 justext_gettext.py $ofile | tee -a $data_path/log.txt
		python3 preprocess_timesofindia.py $ofile | tee -a $data_path/log.txt
	    elif [[ $ofile == *"newindianexpress"* ]]; then
		python2 goose_gettext.py $ofile | tee -a $data_path/log.txt
		python3 preprocess_newindianexpress.py $ofile | tee -a $data_path/log.txt
	    elif [[ $ofile == *"indianexpress"* ]]; then
		python2 goose_gettext.py $ofile | tee -a $data_path/log.txt
		python3 preprocess_indianexpress.py $ofile | tee -a $data_path/log.txt
	    elif [[ $ofile == *"thehindu"* ]]; then
		python2 boilerpipe_gettext.py $ofile | tee -a $data_path/log.txt
		python3 preprocess_thehindu.py $ofile | tee -a $data_path/log.txt
	    elif [[ $ofile == *"scmp"* ]]; then
		python2 boilerpipe_gettext.py $ofile | tee -a $data_path/log.txt
		python3 preprocess_scmp.py $ofile | tee -a $data_path/log.txt
	    else
		echo "No idea what source : $ofile" | tee -a $data_path/log.txt
	    fi
	fi
    done

    python3 -W ignore $data_path/fill_in_blanks.py $data_file | tee -a $data_path/log.txt
done
