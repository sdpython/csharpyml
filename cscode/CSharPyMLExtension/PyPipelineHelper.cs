// See the LICENSE file in the project root for more information.

using System;
using System.IO;
using Microsoft.ML.Runtime;
using Scikit.ML.ScikitAPI;
using Scikit.ML.DataManipulation;


namespace CSharPyMLExtension
{
    /// <summary>
    /// Easier functions to use from Python.
    /// </summary>
    public static class PyPipelineHelper
    {
        public static ScikitPipeline CreateScikitPipeline(string filename, IHostEnvironment host = null)
        {
            if (host == null)
                throw new ArgumentNullException("host cannot be null.");
            return new ScikitPipeline(filename, host);
        }

        public static ScikitPipeline CreateScikitPipeline(Stream st, IHostEnvironment host = null)
        {
            if (host == null)
                throw new ArgumentNullException("host cannot be null.");
            return new ScikitPipeline(st, host);
        }

        public static ScikitPipeline CreateScikitPipeline(string[] transforms = null, string predictor = null, IHostEnvironment host = null)
        {
            if (host == null)
                throw new ArgumentNullException("host cannot be null.");
            return new ScikitPipeline(transforms, predictor, host);
        }

        public static DataFrame FastPredictOrTransform(ScikitPipeline pipe, DataFrame df, int conc = 1)
        {
            DataFrame res = null;
            pipe.Predict(df, ref res, conc);
            return res;
        }
    }
}
