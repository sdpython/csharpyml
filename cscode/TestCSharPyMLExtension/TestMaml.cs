using Microsoft.VisualStudio.TestTools.UnitTesting;
using System.IO;
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
            PyMamlHelper.MamlAll(script, false);
            Assert.IsTrue(File.Exists(model));
        }
    }
}
