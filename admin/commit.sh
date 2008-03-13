svn diff ChangeLog | \
    egrep '^\+' | \
    sed -e 's/^\+//g'| \
    egrep -v '^\+\+ ChangeLog' > commit-msg
echo "Committing with this message:"
cat commit-msg
echo
if [[ "$1" == 'run_tests' ]];then
    python test/test_all.py &> test.out
else
    echo 'OK' > test.out
fi
STATUS=`tail -1 test.out|awk '{print $1}'`
if [[ "$STATUS" == 'OK' ]];then
    rm test.out
    if [[ "$1" == 'run_tests' ]];then
        echo "All tests passed."
    else
        echo "Skipping tests..."
    fi
    echo "Committing to Subversion now..."
    svn commit --file commit-msg && \
        rm commit-msg || \
        echo "There was an error committing; message preserved."
else
    echo "*** Commit aborting! Test suite failed ***"
    cat test.out
fi
