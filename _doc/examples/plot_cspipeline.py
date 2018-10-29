"""
Trains a Random Forest on Iris dataset
======================================

The following example shows how to create and train
a pipeline using :ref:`l-fasttree-boosted-trees-classification`.
"""
import sys
import os
import unittest
import numpy
from sklearn import datasets
from sklearn.model_selection import train_test_split
import pandas
from csharpyml.binaries import CSPipeline

##############################
# Let's first retrieve the data.

X, y = datasets.load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X.astype(numpy.float32), y.astype(numpy.float32))
df_train = pandas.DataFrame(data=X_train, columns=["FA", "FB", "FC", "FD"])
df_train["Label"] = y_train

df_test = pandas.DataFrame(data=X_test, columns=["FA", "FB", "FC", "FD"])
df_test["Label"] = y_test

##############################
# Let's create a pipeline.
pipe = CSPipeline(["concat{col=Feat:FA,FB,FC,FD}"],
                  "oova{p=ft}", verbose=2)

#############################
# Let's train it.
pipe.fit(df_train, feature="Feat", label="Label")

###############################################
# Let's show the output.

print(pipe.StdOut)

#################################
# Let's predict.

pred = pipe.predict(df_test)
print(pred.head())

###########################
# Let's save the model.

outfile = "model.zip"
pipe.save(outfile)

#############################
# Let's load it.

pipe2 = CSPipeline.load(outfile)
pred2 = pipe2.predict(df_test)
print(pred2.head())
