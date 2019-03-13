data_path=$(pwd)
cd ../collector

for data_file in $data_path/*.json
do
    if [ ! -d tmp/htmls ]; then
	mkdir tmp/htmls
    fi
    # scrapy crawl sp -a filename="$data_file"

    if [ ! -d tmp/texts ]; then
	mkdir tmp/texts
    fi
    for filename in tmp/htmls/http*
    do
	ofile=$(echo "$(basename $filename)")
	if [ ! -f tmp/texts/$ofile ]; then
	    if [[ $ofile == *"timesofindia"* ]]; then
		echo "timesofindia"
		python3 justext_gettext.py $ofile
		python3 preprocess_timesofindia.py $ofile
	    elif [[ $ofile == *"newindianexpress"* ]]; then
		echo "newindianexpress"
		python goose_gettext.py $ofile
		python3 preprocess_newindianexpress.py $ofile
	    elif [[ $ofile == *"indianexpress"* ]]; then
		echo "indianexpress"
		python goose_gettext.py $ofile
		python3 preprocess_indianexpress.py $ofile
	    elif [[ $ofile == *"thehindu"* ]]; then
		echo "thehindu"
		python boilerpipe_gettext.py $ofile
		python3 preprocess_thehindu.py $ofile
	    elif [[ $ofile == *"scmp"* ]]; then
		python boilerpipe_gettext.py $ofile
		python3 preprocess_scmp.py $ofile
	    else
		echo "No idea what source : $ofile"
	    fi
	fi
    done

    # python3 ../preprocess.py $data_file
    # python3 ../fill_in_blanks.py $data_file
done
