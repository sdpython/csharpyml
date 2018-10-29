// See the LICENSE file in the project root for more information.

using System;
using Microsoft.ML.Runtime;
using Scikit.ML.PipelineHelper;
using Scikit.ML.ScikitAPI;


namespace CSharPyMLExtension
{
    /// <summary>
    /// Easier functions to use from Python.
    /// </summary>
    public static class PyEnvHelper
    {
        public static MessageSensitivity MessageSensitivityFromString(string sens)
        {
            switch (sens)
            {
                case "Unknown": return MessageSensitivity.Unknown;
                case "All": return MessageSensitivity.All;
                case "None": return MessageSensitivity.None;
                case "UserData": return MessageSensitivity.UserData;
                case "Schema": return MessageSensitivity.Schema;
                default:
                    throw new Exception(string.Format("Unable to interpret '{0}'", sens));
            }
        }

        public static IHostEnvironment CreateEnvironment(int seed = -1, int verbose = 0,
                                                  string sensitivity = "All", int conc = 0,
                                                  ILogWriter outWriter = null, ILogWriter errWriter = null)
        {
            var env = new DelegateEnvironment(seed: seed < 0 ? null : (int?)seed, verbose: verbose,
                                           sensitivity: MessageSensitivityFromString(sensitivity),
                                           conc: conc, outWriter: outWriter, errWriter: errWriter);
            ComponentHelper.AddStandardComponents(env);
            return env;
        }

        public static IHostEnvironment CreateConsoleEnvironment(int seed = -1, int verbose = 0,
                                                  string sensitivity = "All", int conc = 0)
        {
            var outWriter = new LogWriter(s => Console.Write(s));
            var errWriter = new LogWriter(s => Console.Error.Write(s));
            var env = new DelegateEnvironment(seed: seed < 0 ? null : (int?)seed, verbose: verbose,
                                           sensitivity: MessageSensitivityFromString(sensitivity),
                                           conc: conc, outWriter: outWriter, errWriter: errWriter);
            ComponentHelper.AddStandardComponents(env);
            return env;
        }

        public delegate void PrintDelegate(string text);

        public static IHostEnvironment CreatePythonEnvironment(int seed = -1, int verbose = 0,
                                                               string sensitivity = "All", int conc = 0,
                                                               PrintDelegate outFctWriter = null,
                                                               PrintDelegate errFctWriter = null)
        {
            var outWriter = new LogWriter(s => outFctWriter(s));
            var errWriter = new LogWriter(s => errFctWriter(s));
            var env = new DelegateEnvironment(seed: seed < 0 ? null : (int?)seed, verbose: verbose,
                                              sensitivity: MessageSensitivityFromString(sensitivity),
                                              conc: conc, outWriter: outWriter, errWriter: errWriter);
            ComponentHelper.AddStandardComponents(env);
            return env;
        }
    }
}
