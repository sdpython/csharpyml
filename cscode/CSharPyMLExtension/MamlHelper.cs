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
                var sbout = new StringBuilder();
                var sberr = new StringBuilder();
                var sout = new StringWriter(sbout);
                var serr = new StringWriter(sberr);
                var cur_out = Console.Out;
                var cur_err = Console.Error;
                Console.SetOut(sout);
                Console.SetError(serr);

                errCode = Maml.MainAll(script);

                Console.SetOut(cur_out);
                Console.SetError(cur_err);

                res = $"--OUT--\n{sbout.ToString()}\n--ERR--\n{sberr.ToString()}";
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
