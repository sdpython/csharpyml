// See the LICENSE file in the project root for more information.

using Microsoft.VisualStudio.TestTools.UnitTesting;
using System;
using System.IO;
using System.Runtime.InteropServices;
using System.Linq;
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
            var pipe = PyPipelineHelper.CreateScikitPipeline(new string[] { "Concat{col=Features:Slength,Swidth}" }, 
                                                             "mlr", env3.Item1);
            pipe.Train(df, "Features", "Label");
            var sout = env3.Item2.ToString();
            Assert.IsNotNull(sout);
        }

        internal static class Mkl
        {
            private const string DllName = "MklImports";

            public enum Layout
            {
                RowMajor = 101,
                ColMajor = 102
            }

            public enum UpLo : byte
            {
                Up = (byte)'U',
                Lo = (byte)'L'
            }

            [DllImport(DllName, EntryPoint = "LAPACKE_dpptrf")]
            public static extern int PptrfInternal(Layout layout, UpLo uplo, int n, Double[] ap);
        }

        [TestMethod]
        public void TestScikitAPI_MKL()
        {
            Mkl.PptrfInternal(Mkl.Layout.ColMajor, Mkl.UpLo.Lo, 2, new double[] { 0.1, 0.3 });
        }

        [TestMethod]
        public void TestPipelineDiabete()
        {
            var diab = FileHelper.GetTestFile("diabete.csv");
            var cols = Enumerable.Range(0, 10).Select(c => NumberType.R4).ToArray();
            var colsName = string.Join(',', Enumerable.Range(0, 10).Select(c => $"F{c}"));
            var df = DataFrameIO.ReadCsv(diab, sep: ',', dtypes: cols);
            var env3 = PyEnvHelper.CreateStoreEnvironment();
            var pipe = PyPipelineHelper.CreateScikitPipeline(new string[] { $"Concat{{col=Features:{colsName}}}" }, "ols", env3.Item1);
            pipe.Train(df, "Features", "Label");
            var sout = env3.Item2.ToString();
            Assert.IsNotNull(sout);
            DataFrame pred = PyPipelineHelper.FastPredictOrTransform(pipe, df);
            Assert.IsTrue(df.Shape[0] > 0);
        }
    }
}


