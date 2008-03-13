. ./admin/repoVars.sh
./admin/syncLocalRepo.sh
./admin/sfUpload.sh
./admin/syncSFRepo.py $MIRROR/$DUMP.gz \
    $SF_ID $MIN_DAYS $PICKLE_FILE
rm $MIRROR/$DUMP.gz
