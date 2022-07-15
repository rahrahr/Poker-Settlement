rm -r ./1
rm temp.txt
rm player_stats.txt
rm player_stats.xlsx
rm hand_history.txt
rm copy.json

if [ -z "$1" ]
# Default parse all directories named '...ledgers...' and '...logs...'
then
    mkdir ./1
    cp -r ./*ledgers*/* ./1
    python poker_settle.py ./1
    rm -r ./1

    mkdir ./1
    cp -r ./*logs*/* ./1
    cp agg_log.py ./1
    cd ./1
    python agg_log.py
    cd ..

elif [ "$1" = "training" ]
then
    mkdir ./1
    cp -r ./ledger_$1/* ./1
    python poker_settle.py ./1
    rm -r ./1

    mkdir ./1
    cp -r ./log_$1/* ./1
    cp agg_log.py ./1
    cd ./1
    python agg_log.py
    cd ..
else
    mkdir ./1
    cp -r ./ledgers_$1/* ./1
    python poker_settle.py ./1
    rm -r ./1

    mkdir ./1
    cp -r ./logs_$1/* ./1
    cp agg_log.py ./1
    cd ./1
    python agg_log.py
    cd ..
fi

python log_processor.py ./1/logs.csv > temp.txt
sed -n '/^Play Stats (What happened when you played in a round?)$/,$p' temp.txt > player_stats.txt
sed -n '/Play Stats (What happened when you played in a round?)$/q;p' temp.txt > hand_history.txt

python parse_stats.py

rm temp.txt
# rm player_stats.txt
# rm copy.json
rm -r ./1