batchfile=batchfile.txt
>$batchfile
for file in data/*; do
    name=$(basename $file)
    out=stage/ingest/$name
    tmp=$out.tmp
    echo put $file $tmp >> $batchfile;
    echo rename $tmp $out >> $batchfile;
    done
