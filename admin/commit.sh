function abort {
    echo "*** Commit aborting! Test suite failed ***"
}

function error {
    echo "There was an error committing; message preserved."
}

function succeed {
    rm commit-msg
    echo -n "Commit succeeded; sync Google and SourceForge? [y/n] "; read CHECK
    if [[ "$CHECK" == "y" ]]; then
        ./admin/syncRepos.sh
    fi
}

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
    svn commit --file commit-msg && succeed || error
else
    abort
fi
