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
    /// Helpers to run scripts through maml.
    /// </summary>
    public static class PyMamlHelper
    {
        public static string MamlScript(string script, bool catch_output,
                                        int conc = 0, int verbose = 2, int sensitivity = -1,
                                        bool skipFailLoading = false)
        {
            ILogWriter logout, logerr;
            var stout = new StringBuilder();
            var sterr = new StringBuilder();
            if (catch_output)
            {
                logout = new LogWriter((string s) =>
                {
                    stout.Append(s);
                });
                logerr = new LogWriter((string s) =>
                {
                    sterr.Append(s);
                });
            }
            else
            {
                logout = new LogWriter((string s) => { Console.Write(s); });
                logerr = new LogWriter((string s) => { Console.Error.Write(s); });
            }

            using (var env = new DelegateEnvironment((int?)null, verbose, (MessageSensitivity)sensitivity, conc, logout, logerr))
            {
                if (skipFailLoading)
                {
                    try
                    {
                        ComponentHelper.AddStandardComponents(env);
                    }
                    catch (Exception e)
                    {
                        sterr.Append($"Unable to load an assembly due to {e.ToString()}.\n");
                    }
                }
                else
                    ComponentHelper.AddStandardComponents(env);

                string res = null;
                try
                {
                    res = MamlHelper.MamlScript(script, false, env);
                    if (!string.IsNullOrEmpty(res))
                        stout.Append(res);
                }
                catch (InvalidOperationException e)
                {
                    if (!string.IsNullOrEmpty(res))
                        sterr.Append(res + "\n");
                    sterr.Append($"[PyMamlHelper-InvalidOperationException] catch_output={catch_output}\n" + e.ToString() + "\n");
                }
                catch (MamlException e)
                {
                    if (!string.IsNullOrEmpty(res))
                        sterr.Append(res + "\n");
                    sterr.Append($"[PyMamlHelper-MamlException] catch_output={catch_output}\n" + e.ToString() + "\n");
                }
                if (sterr.Length > 0)
                    return string.Format("---OUT---\n{0}\n---ERR---\n{1}", stout.ToString(), sterr.ToString());
                else
                    return stout.ToString();
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
