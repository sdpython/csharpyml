// See the LICENSE file in the project root for more information.

using Microsoft.VisualStudio.TestTools.UnitTesting;
using System;
using System.IO;
using Microsoft.ML.Runtime.Data;
using Scikit.ML.DataManipulation;
using CSharPyMLExtension;


namespace TestCSharPyMLExtension
{
    [TestClass]
    public class TestPipeline
    {
        [TestMethod]
        public void TestPipelineIris()
        {
            var iris = FileHelper.GetTestFile("iris_data_id.txt");
            var df = DataFrameIO.ReadCsv(iris, sep: ',', dtypes: new[] { NumberType.R4, NumberType.R4, NumberType.R4 });
            var env3 = PyEnvHelper.CreateStoreEnvironment();
            var pipe = PyPipelineHelper.CreateScikitPipeline(new string[] { "Concat{col=Features:Slength,Swidth}" }, "mlr", env3.Item1);
            pipe.Train(df, "Features", "Label");
            var sout = env3.Item2.ToString();
            Assert.IsNotNull(sout);
        }
    }
}


