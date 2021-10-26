if [ ! -n "$1" -o ! -n "$2" ]; then
  echo "Usage: ./ctdicom2raw.sh <indir> <outdir> [outparam (first | every)]"
  exit
fi

outparam="first"
if [ -n "$3" ]; then
  outparam=$3
fi

if [ -e "_TempCodeRunner.py" ]; then
  rm _TempCodeRunner.py
fi

echo "
from ctdicom2raw import ctdicom2raw
ctdicom2raw(\"$1\", \"$2\", outputParam=\"$outparam\", verbose=True)
" >> _TempCodeRunner.py

python _TempCodeRunner.py

rm _TempCodeRunner.py

exit
