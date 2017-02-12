from subprocess import call
import os
import glob

files = glob.glob("train-*.arff")

for fil in files:
    call(["java", "-cp", "/u/cs401/WEKA/weka.jar", "weka.classifiers.trees.J48", "-t", fil, "-T", "test.arff", "-no-cv", "-o", ">" "{}.txt".format(fil)])
