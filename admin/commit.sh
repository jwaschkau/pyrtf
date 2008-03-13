svn diff ChangeLog | \
    egrep '^\+' | \
    sed -e 's/^\+//g'| \
    egrep -v '^\+\+ ChangeLog' > commit-msg
echo "Committing with this message:"
cat commit-msg
echo
FLAG='skip_tests'
if [[ "$1" == "$FLAG" ]];then
    echo 'OK' > test.out
else
    # send the output (stdout and stderr) to both a file for checking and
    # stdout for immediate viewing/feedback
    python test/test_all.py 2>&1|tee test.out
fi
STATUS=`tail -1 test.out|awk '{print $1}'`
if [[ "$STATUS" == 'OK' ]];then
    rm test.out
    if [[ "$1" == "FLAG" ]];then
        echo "Skipping tests..."
    else
        echo "All tests passed."
    fi
    echo "Committing to Subversion now..."
    svn commit --file commit-msg && \
        rm commit-msg || \
        echo "There was an error committing; message preserved."
else
    echo "*** Commit aborting! Test suite failed ***"
fi
