// See the LICENSE file in the project root for more information.

using System;
using System.IO;
using System.Text;


namespace CSharPyMLExtension
{
    /// <summary>
    /// Captures standard output and error.
    /// </summary>
    public class StdCapture: IDisposable
    {
        StringBuilder sbout;
        StringBuilder sberr;
        StringWriter sout;
        StringWriter serr;
        TextWriter cur_out;
        TextWriter cur_err;

        public string StdOut => sbout.ToString();
        public string StdErr => sberr.ToString();

        /// <summary>
        /// Starts capturing the standard output and error.
        /// </summary>
        public StdCapture()
        {
            sbout = new StringBuilder();
            sberr = new StringBuilder();
            sout = new StringWriter(sbout);
            serr = new StringWriter(sberr);
            cur_out = Console.Out;
            cur_err = Console.Error;
            Console.SetOut(sout);
            Console.SetError(serr);
        }

        /// <summary>
        /// Puts back the standard streams.
        /// </summary>
        public void Dispose()
        {
            Console.SetOut(cur_out);
            Console.SetError(cur_err);
        }
    }
}
