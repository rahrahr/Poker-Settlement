rm -r ./1
rm temp.txt
rm player_stats.txt
rm stats/hand_history.txt

mkdir ./1
cp -r ./ledgers_geyige/* ./old_ledgers/* ./1
python poker_settle.py ./1
rm -r ./1

mkdir ./1
cp -r ./logs_geyige/* ./old_logs/* ./1
cd ./1
python agg_log.py
cd ..

python log_processor.py ./1/logs.csv > temp.txt
sed -n '/^Play Stats (What happened when you played in a round?)$/,$p' temp.txt > player_stats.txt
sed -n '/Play Stats (What happened when you played in a round?)$/q;p' temp.txt > hand_history.txt

rm temp.txt
rm -r ./1