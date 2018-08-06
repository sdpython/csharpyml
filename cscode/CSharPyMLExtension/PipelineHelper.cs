// See the LICENSE file in the project root for more information.

using System.IO;
using Microsoft.ML.Runtime;
using Scikit.ML.ScikitAPI;


namespace CSharPyMLExtension
{
    /// <summary>
    /// Easier functions to use from Python.
    /// </summary>
    public static class PipelineHelper
    {
        public static ScikitPipeline CreateScikitPipeline(string filename, IHostEnvironment host = null)
        {
            return new ScikitPipeline(filename, host);
        }

        public static ScikitPipeline CreateScikitPipeline(Stream st, IHostEnvironment host = null)
        {
            return new ScikitPipeline(st, host);
        }

        public static ScikitPipeline CreateScikitPipeline(string[] transforms = null, string predictor = null, IHostEnvironment host = null)
        {
            return new ScikitPipeline(transforms, predictor, host);
        }
    }
}
