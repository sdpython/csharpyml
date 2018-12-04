using Microsoft.ML;
using Microsoft.ML.Runtime.Api;
using Microsoft.ML.Runtime.Data;
using Microsoft.ML.Transforms;
using Microsoft.ML.Runtime.Learners;
using System.IO;


namespace TestCSharPyMLExtension
{
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

        public void Train(string dest)
        {
            using (var env = new ConsoleEnvironment(verbose: false))
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
                var km = new MulticlassLogisticRegression(env, "Label", "Features");
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
                using (var stdest = File.OpenWrite(dest))
                    model.SaveTo(env, stdest);
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

    public static class g
    {
        public static TrainTestIris ReturnMLClass(string ds)
        {
            return new TrainTestIris(ds);
        }
    }
}
