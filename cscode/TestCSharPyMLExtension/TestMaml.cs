using Microsoft.VisualStudio.TestTools.UnitTesting;
using System;
using System.IO;
using Microsoft.ML.Runtime.Data;
using Scikit.ML.DataManipulation;
using CSharPyMLExtension;


namespace TestCSharPyMLExtension
{
    [TestClass]
    public class TestMaml
    {
        [TestMethod]
        public void TestMamlAll()
        {
            var script = "train " +
                         "data=__DATA__ " +
                         "loader=text{col=Label:U4[0-2]:0 col=Slength:R4:1 " +
                         "col=Swidth:R4:2 col=Plength:R4:3 col=Pwidth:R4:4 sep=, header=+} " +
                         "xf=Concat{col=Features:Slength,Swidth} " +
                         "tr=ova{p=ap} " +
                         "parallel=1 " +
                         "out=__MODEL__";
            script = script.Replace("__DATA__", FileHelper.GetTestFile("iris_data_id.txt"));
            var model = FileHelper.GetOutputFile("model.zip", "TestMamlAll");
            script = script.Replace("__MODEL__", model);
            PyMamlHelper.MamlScript(script, false);
            Assert.IsTrue(File.Exists(model));
        }

        [TestMethod]
        public void TestMamlAllError()
        {
            var script = "train " +
                         "data=__DATA__ " +
                         "loader=text{col=Label:U4[0-2]:0 col=Slength:R4:1 " +
                         "col=Swidth:R4:2 col=Plength:R4:3 col=Pwidth:R4:4 sep=, header=+} " +
                         "xf=Concat{col=Features:Slength,Swidth} " +
                         "tr=ova{p=ap " +
                         "parallel=1 " +
                         "out=__MODEL__";
            script = script.Replace("__DATA__", FileHelper.GetTestFile("iris_data_id.txt"));
            var model = FileHelper.GetOutputFile("model.zip", "TestMamlAll");
            script = script.Replace("__MODEL__", model);
            var res = PyMamlHelper.MamlScript(script, true);
            Assert.IsTrue(res.Contains("Unbalanced quoting"));
        }

        [TestMethod]
        public void TestTrainIris()
        {
            var file = FileHelper.GetTestFile("iris_data_id.txt");
            var df = PyDataFrameHelper.ReadCsv(file);
            df.AddColumn("LabelR4", df["Label"].AsType(NumberType.R4));
            var host = PyEnvHelper.CreateConsoleEnvironment();
            var pipe = PyPipelineHelper.CreateScikitPipeline(new[] { "concat{col=Feat:Slength,Swidth,Plength,Pwidth}" },
                                                             "oova{p=ap}", host);
            DataFrame dfo;
            using (var res = pipe.Train(df, "Feat", "LabelR4"))
                dfo = PyDataFrameHelper.ReadView(pipe.Predict(df));
            Assert.AreEqual(dfo.Shape, new Tuple<int, int>(150, 14));
        }

        [TestMethod]
        public void TestHelp()
        {
            var output = PyMamlHelper.MamlScript("? lr", true);
            Assert.IsTrue(output.Contains("LogisticRegression"));
        }
    }
}
