// See the LICENSE file in the project root for more information.

using System;
using System.Linq;
using System.Text;
using Microsoft.ML.Runtime;
using Scikit.ML.DocHelperMlExt;
using Scikit.ML.PipelineHelper;
using Scikit.ML.ScikitAPI;


namespace CSharPyMLExtension
{
    /// <summary>
    /// Raised when a script cannot be executed.
    /// </summary>
    public class MamlException : Exception
    {
        public MamlException(string msg) : base(msg)
        {
        }
    }

    /// <summary>
    /// Helpers to run scripts through maml.
    /// </summary>
    public static class PyMamlHelper
    {
        public static string MamlScript(string script, bool catch_output, int conc = 0, int verbose = 2, int sensitivity = -1)
        {
            ILogWriter logout, logerr;
            var stout = new StringBuilder();
            var sterr = new StringBuilder();
            if (catch_output)
            {
                logout = new LogWriter((string s) => { stout.Append(s); });
                logerr = new LogWriter((string s) => { sterr.Append(s); });
            }
            else
            {
                logout = new LogWriter((string s) => { Console.Write(s); });
                logerr = new LogWriter((string s) => { Console.Error.Write(s); });
            }

            using (var env = new DelegateEnvironment((int?)null, verbose, (MessageSensitivity)sensitivity, conc, logout, logerr))
            {
                ComponentHelper.AddStandardComponents(env);
                var res = MamlHelper.MamlScript(script, false, env);
                if (catch_output)
                {
                    if (sterr.Length > 0)
                        return string.Format("---OUT---\n{0}\n---ERR---\n{1}", stout.ToString(), sterr.ToString());
                    else
                        return stout.ToString();
                }
                else
                    return res;
            }
        }

        public static string[] GetAllKinds()
        {
            return MamlHelper.GetAllKinds();
        }

        public static MamlHelper.ComponentDescription[] ListOfComponents(string kind)
        {
            return MamlHelper.EnumerateComponents(kind).ToArray();
        }
    }
}
