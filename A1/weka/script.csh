#!/local/bin/tcsh

#foreach file (`ls train*.arff`)
#    `java -cp /u/cs401/WEKA/weka.jar weka.classifiers.trees.J48 -t $file -T test.arff -no-cv -o > $file.txt`
#end

foreach n (0 1 2 3 4 5 6 7 8 9)
    `java -cp /u/cs401/WEKA/weka.jar weka.classifiers.trees.J48 -t ptrain-$n.arff -T ptest-$n.arff -o >> j48-cv.txt`
    `java -cp /u/cs401/WEKA/weka.jar weka.classifiers.bayes.NaiveBayes -t ptrain-$n.arff -T ptest-$n.arff -o >> bayes-cv.txt`
    `java -cp /u/cs401/WEKA/weka.jar weka.classifiers.functions.SMO -t ptrain-$n.arff -T ptest-$n.arff -o >> smo-cv.txt`
end
