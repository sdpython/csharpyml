// See the LICENSE file in the project root for more information.

using System;
using System.IO;
using System.Text;
using Microsoft.ML.Runtime.Tools;


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
    /// Helpers to run script through maml.
    /// </summary>
    public static class MamlHelper
    {
        public static string MamlAll(string script, bool catch_output)
        {
            int errCode;
            string res;
            if (catch_output)
            {
                using (var capture = new StdCapture())
                {
                    errCode = Maml.MainAll(script);
                    var sout = capture.StdOut;
                    var serr = capture.StdErr;
                    res = $"--OUT--\n{sout}\n--ERR--\n{serr}";
                }
            }
            else
            {
                errCode = Maml.MainAll(script);
                res = string.Empty;
            }
            if (errCode != 0)
                throw new MamlException($"Unable to run script, error code={errCode}\n{script}\n{res}");
            return res;
        }
    }
}
