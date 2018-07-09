// See the LICENSE file in the project root for more information.

using System;
using System.Text;
using Microsoft.ML.Runtime.Data;
using Scikit.ML.DataManipulation;


namespace CSharPyMLExtension
{
    /// <summary>
    /// Easier function to use from Python.
    /// </summary>
    public static class DataFrameHelper
    {
        /// <summary>
        /// Creates an empty dataframe.
        /// </summary>
        public static DataFrame CreateEmptyDataFrame()
        {
            return new DataFrame();
        }

        public static void AddColumnToDataFramebool(DataFrame df, string name, bool[] values)
        {
            var bval = new DvBool[values.Length];
            for (int i = 0; i < values.Length; ++i)
                bval[i] = values[i];
            df.AddColumn(name, bval);
        }

        public static void AddColumnToDataFrameint32(DataFrame df, string name, Int32[] values)
        {
            var bval = new DvInt4[values.Length];
            for (int i = 0; i < values.Length; ++i)
                bval[i] = values[i];
            df.AddColumn(name, bval);
        }

        public static void AddColumnToDataFrameint64(DataFrame df, string name, Int64[] values)
        {
            var bval = new DvInt8[values.Length];
            for (int i = 0; i < values.Length; ++i)
                bval[i] = values[i];
            df.AddColumn(name, bval);
        }

        public static void AddColumnToDataFrameuint(DataFrame df, string name, uint[] values)
        {
            var cpy = new uint[values.Length];
            Array.Copy(values, cpy, values.Length);
            df.AddColumn(name, cpy);
        }

        public static void AddColumnToDataFramefloat32(DataFrame df, string name, float[] values)
        {
            var cpy = new float[values.Length];
            Array.Copy(values, cpy, values.Length);
            df.AddColumn(name, cpy);
        }

        public static void AddColumnToDataFramefloat64(DataFrame df, string name, double[] values)
        {
            var cpy = new double[values.Length];
            Array.Copy(values, cpy, values.Length);
            df.AddColumn(name, cpy);
        }

        public static void AddColumnToDataFramestring(DataFrame df, string name, string[] values)
        {
            var bval = new DvText[values.Length];
            for (int i = 0; i < values.Length; ++i)
                bval[i] = new DvText(values[i]);
            df.AddColumn(name, bval);
        }

        /// <summary>
        /// Reads a string as a IDataView.
        /// Follows pandas API.
        /// </summary>
        public static DataFrame ReadStr(string content, char sep = ',', bool header = true,
                                    string[] names = null, int[] dtypes = null,
                                    int nrows = -1, int guess_rows = 10, bool index = false)
        {
            DataKind?[] kinds = null;
            if (dtypes != null)
            {
                kinds = new DataKind?[dtypes.Length];
                for (int i = 0; i < kinds.Length; ++i)
                    kinds[i] = dtypes[i] < 0 ? (DataKind?)null : (DataKind?)(DataKind)dtypes[i];
            }
            return DataFrame.ReadStr(content, sep, header, names, kinds, nrows, guess_rows, index);
        }

        /// <summary>
        /// Reads a string as a IDataView.
        /// Follows pandas API.
        /// </summary>
        public static DataFrame ReadCsv(string filename, char sep = ',', bool header = true,
                                    string[] names = null, int[] dtypes = null,
                                    int nrows = -1, int guess_rows = 10, string encoding = null,
                                    bool index = false)
        {
            DataKind?[] kinds = null;
            if (dtypes != null)
            {
                kinds = new DataKind?[dtypes.Length];
                for (int i = 0; i < kinds.Length; ++i)
                    kinds[i] = dtypes[i] < 0 ? null : (DataKind?)(DataKind)dtypes[i];
            }
            return DataFrame.ReadCsv(filename, sep, header, names, kinds, nrows, guess_rows,
                                     encoding == null ? null : Encoding.GetEncoding(encoding),
                                     index: index);
        }

        public static string DataFrameToString(DataFrame df)
        {
            using (var capture = new StdCapture())
                return df.ToString();
        }

        public static DvBool[] DataFrameColumnToArrrayDvBool(DataFrame df, int i)
        {
            var col = df.GetColumn(i).Column as DataColumn<DvBool>;
            if (col == null)
                throw new TypeError($"Column {i} is not of type bool.");
            return col.Data;
        }

        public static bool[] DataFrameColumnToArrraybool(DataFrame df, int i)
        {
            var col = df.GetColumn(i).Column as DataColumn<DvBool>;
            if (col == null)
                throw new TypeError($"Column {i} is not of type bool.");
            var copy = new bool[col.Length];
            for (int j = 0; j < copy.Length; ++j)
                copy[j] = (bool)col.Data[j];
            return copy;
        }

        public static DvInt4[] DataFrameColumnToArrrayDvInt4(DataFrame df, int i)
        {
            var col = df.GetColumn(i).Column as DataColumn<DvInt4>;
            if (col == null)
                throw new TypeError($"Column {i} is not of type int.");
            return col.Data;
        }

        public static uint[] DataFrameColumnToArrrayuint32(DataFrame df, int i)
        {
            var col = df.GetColumn(i).Column as DataColumn<uint>;
            if (col == null)
                throw new TypeError($"Column {i} is not of type uint.");
            return col.Data;
        }

        public static Int32[] DataFrameColumnToArrrayint32(DataFrame df, int i)
        {
            var col = df.GetColumn(i).Column as DataColumn<DvInt4>;
            if (col == null)
                throw new TypeError($"Column {i} is not of type int.");
            var copy = new Int32[col.Length];
            for (int j = 0; j < copy.Length; ++j)
                copy[j] = (int)col.Data[j];
            return copy;
        }

        public static DvInt8[] DataFrameColumnToArrrayDvInt8(DataFrame df, int i)
        {
            var col = df.GetColumn(i).Column as DataColumn<DvInt8>;
            if (col == null)
                throw new TypeError($"Column {i} is not of type Int64.");
            return col.Data;
        }

        public static Int64[] DataFrameColumnToArrrayint64(DataFrame df, int i)
        {
            var col = df.GetColumn(i).Column as DataColumn<DvInt8>;
            if (col == null)
                throw new TypeError($"Column {i} is not of type Int64.");
            var copy = new Int64[col.Length];
            for (int j = 0; j < copy.Length; ++j)
                copy[j] = (Int64)col.Data[j];
            return copy;
        }

        public static float[] DataFrameColumnToArrrayfloat32(DataFrame df, int i)
        {
            var col = df.GetColumn(i).Column as DataColumn<float>;
            if (col == null)
                throw new TypeError($"Column {i} is not of type float.");
            return col.Data;
        }

        public static double[] DataFrameColumnToArrrayfloat64(DataFrame df, int i)
        {
            var col = df.GetColumn(i).Column as DataColumn<double>;
            if (col == null)
                throw new TypeError($"Column {i} is not of type double.");
            return col.Data;
        }

        public static DvText[] DataFrameColumnToArrrayDvText(DataFrame df, int i)
        {
            var col = df.GetColumn(i).Column as DataColumn<DvText>;
            if (col == null)
                throw new TypeError($"Column {i} is not of type string.");
            return col.Data;
        }

        public static string[] DataFrameColumnToArrraystring(DataFrame df, int i)
        {
            var col = df.GetColumn(i).Column as DataColumn<DvText>;
            if (col == null)
                throw new TypeError($"Column {i} is not of type Int64.");
            var copy = new string[col.Length];
            for (int j = 0; j < copy.Length; ++j)
                copy[j] = col.Data[j].ToString();
            return copy;
        }
    }
}
