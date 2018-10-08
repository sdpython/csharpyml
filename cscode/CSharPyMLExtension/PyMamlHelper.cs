// See the LICENSE file in the project root for more information.

using System;
using System.Linq;
using Scikit.ML.DocHelperMlExt;


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
        public static string MamlAll(string script, bool catch_output)
        {
            return MamlHelper.MamlScript(script, catch_output);
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
