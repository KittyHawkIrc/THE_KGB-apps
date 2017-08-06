pip install pint

wget https://raw.githubusercontent.com/KittyHawkIrc/core/master/encoder.py
wget https://raw.githubusercontent.com/KittyHawkIrc/core/master/arsenic_helper.py

for f in *.py
do
    echo Testing: [$f]
    python $f
done
