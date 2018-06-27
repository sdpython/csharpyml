// See the LICENSE file in the project root for more information.

using System;

namespace CSharPyMLExtension
{
    public class TypeError : Exception
    {
        public TypeError(string msg) : base(msg) { }
    }
}
