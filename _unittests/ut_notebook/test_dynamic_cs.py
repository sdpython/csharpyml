"""
@brief      test log(time=2s)
"""
import sys
import os
import unittest
from sklearn import datasets
import pandas
from pyquickhelper.pycode import ExtTestCase, get_temp_folder

try:
    import src
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..")))
    if path not in sys.path:
        sys.path.append(path)
    import src

from src.csharpyml.notebook.csmlmagics import CsMLMagics


class TestDynamicCS(ExtTestCase):
    """Test dynamic compilation."""

    _script = """
        public class IrisObservation
        {
            [Column("0")]
            [ColumnName("Label")]
            public string Label;

            [Column("1")]
            public float Sepal_length;

            [Column("2")]
            public float Sepal_width;

            [Column("3")]
            public float Petal_length;

            [Column("4")]
            public float Petal_width;
        }

        public class IrisPrediction
        {
            public uint PredictedLabel;

            [VectorType(4)]
            public float[] Score;
        }

        public class TrainTestIris
        {
            string _dataset;
            PredictionFunction<IrisObservation, IrisPrediction> _fct;

            public TrainTestIris(string iris)
            {
                _dataset = iris;
            }

            public void Train()
            {
                using (var env = new ConsoleEnvironment(verbose:false))
                {
                    var args = new TextLoader.Arguments()
                    {
                        Separator = ",",
                        HasHeader = true,
                        Column = new TextLoader.Column[] {
                            new TextLoader.Column("Label", DataKind.R4, 0),
                            new TextLoader.Column("Sepal_length", DataKind.R4, 1),
                            new TextLoader.Column("Sepal_width", DataKind.R4, 2),
                            new TextLoader.Column("Petal_length", DataKind.R4, 3),
                            new TextLoader.Column("Petal_width", DataKind.R4, 4),
                        }
                    };

                    var reader = new TextLoader(env, args);
                    var concat = new ColumnConcatenatingEstimator(env,
                                                                  "Features", "Sepal_length",
                                                                  "Sepal_width", "Petal_length", "Petal_width");
                    var km = new MulticlassLogisticRegression(env, "Features", "Label");
                    var pipeline = concat.Append(km);

                    IDataView trainingDataView = reader.Read(new MultiFileSource(_dataset));
                    var model = pipeline.Fit(trainingDataView);

                    var obs = new IrisObservation()
                    {
                        Sepal_length = 3.3f,
                        Sepal_width = 1.6f,
                        Petal_length = 0.2f,
                        Petal_width = 5.1f,
                    };

                    _fct = model.MakePredictionFunction<IrisObservation, IrisPrediction>(env);
                }
            }

            public IrisPrediction Predict(double sl, double sw, double pl, double pw)
            {
                var obs = new IrisObservation()
                {
                    Sepal_length = (float)sl,
                    Sepal_width = (float)sw,
                    Petal_length = (float)pl,
                    Petal_width = (float)pw,
                };
                return _fct.Predict(obs);
            }
        }

        public static TrainTestIris ReturnMLClass(string ds)
        {
            return new TrainTestIris(ds);
        }
        """

    def test_src(self):
        "skip pylint"
        self.assertFalse(src is None)

    def test_magic_cs(self):
        cm = CsMLMagics()
        fct = cm.mlnet("ReturnMLClass", TestDynamicCS._script)
        if fct is None:
            raise Exception(TestDynamicCS._script)

        temp = get_temp_folder(__file__, "temp_nb_mlnet")
        iris = datasets.load_iris()
        X = iris.data
        y = iris.target
        df = pandas.DataFrame(
            X, columns=['Slength', 'Swidth', 'Plength', 'Pwidth'])
        df["Label"] = y
        df = df[["Label"] + ['Slength', 'Swidth', 'Plength', 'Pwidth']]
        dest = os.path.join(temp, "iris_data_id.txt")
        df.to_csv(dest, sep=',', index=False)

        cl = fct(dest)
        cl.Train()
        res = cl.Predict(3.4, 5.4, 3.2, 5.6)
        label = res.PredictedLabel
        score = list(res.Score)
        self.assertEqual(label, 3)
        self.assertEqual(len(score), 3)


if __name__ == "__main__":
    unittest.main()
