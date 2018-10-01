// See the LICENSE file in the project root for more information.

using System;
using System.Text;
using Microsoft.ML.Runtime.Data;
using Scikit.ML.DataManipulation;
using Scikit.ML.PipelineHelper;


namespace CSharPyMLExtension
{
    /// <summary>
    /// Easier functions to use from Python.
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

        public static void AddColumnToDataFrameInt(DataFrame df, string name, int[] values)
        {
            var bval = new int[values.Length];
            for (int i = 0; i < values.Length; ++i)
                bval[i] = values[i];
            df.AddColumn(name, bval);
        }

        public static void AddColumnToDataFrameInt64(DataFrame df, string name, Int64[] values)
        {
            var bval = new Int64[values.Length];
            for (int i = 0; i < values.Length; ++i)
                bval[i] = values[i];
            df.AddColumn(name, bval);
        }

        public static void AddColumnToDataFrameUint(DataFrame df, string name, uint[] values)
        {
            var cpy = new uint[values.Length];
            Array.Copy(values, cpy, values.Length);
            df.AddColumn(name, cpy);
        }

        public static void AddColumnToDataFrameFloat(DataFrame df, string name, float[] values)
        {
            var cpy = new float[values.Length];
            Array.Copy(values, cpy, values.Length);
            df.AddColumn(name, cpy);
        }

        public static void AddColumnToDataFrameFloat64(DataFrame df, string name, double[] values)
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
        /// Creates a dataframe from a IDataView.
        /// </summary>
        public static DataFrame ReadView(IDataView view, int nrows = -1)
        {
            return DataFrameIO.ReadView(view, nrows);
        }

        /// <summary>
        /// Reads a string as a IDataView.
        /// Follows pandas API.
        /// </summary>
        public static DataFrame ReadStr(string content, char sep = ',', bool header = true,
                                    string[] names = null, int[] dtypes = null,
                                    int nrows = -1, int guess_rows = 10, bool index = false)
        {
            var kinds = IntToColumnTypes(dtypes);
            return DataFrameIO.ReadStr(content, sep, header, names, kinds, nrows, guess_rows, index);
        }

        static ColumnType[] IntToColumnTypes(int[] dtypes)
        {
            ColumnType[] kinds = null;
            if (dtypes != null)
            {
                kinds = new ColumnType[dtypes.Length];
                for (int i = 0; i < kinds.Length; ++i)
                {
                    if (dtypes[i] < 0)
                        kinds[i] = null;
                    else
                    {
                        var kind = (DataKind)dtypes[i];
                        var ctype = SchemaHelper.DataKind2ColumnType(kind);
                        kinds[i] = ctype;
                    }
                }
            }
            return kinds;
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
            var kinds = IntToColumnTypes(dtypes);
            return DataFrameIO.ReadCsv(filename, sep, header, names, kinds, nrows, guess_rows,
                                     encoding == null ? null : Encoding.GetEncoding(encoding),
                                     index: index);
        }

        public static string DataFrameToString(DataFrame df)
        {
            using (var capture = new StdCapture())
                return df.ToString();
        }

        public static bool[] DataFrameColumnToArrrayBool(DataFrame df, int i)
        {
            var col = df.GetColumn(i).Column as DataColumn<bool>;
            if (col == null)
                throw new TypeError($"Column {i} is not of type bool.");
            return col.Data;
        }

        public static int[] DataFrameColumnToArrrayInt(DataFrame df, int i)
        {
            var col = df.GetColumn(i).Column as DataColumn<int>;
            if (col == null)
                throw new TypeError($"Column {i} is not of type int.");
            return col.Data;
        }

        public static uint[] DataFrameColumnToArrrayUint(DataFrame df, int i)
        {
            var col = df.GetColumn(i).Column as DataColumn<uint>;
            if (col == null)
                throw new TypeError($"Column {i} is not of type uint.");
            return col.Data;
        }

        public static Int64[] DataFrameColumnToArrrayInt64(DataFrame df, int i)
        {
            var col = df.GetColumn(i).Column as DataColumn<Int64>;
            if (col == null)
                throw new TypeError($"Column {i} is not of type Int64.");
            return col.Data;
        }

        public static float[] DataFrameColumnToArrrayFloat(DataFrame df, int i)
        {
            var col = df.GetColumn(i).Column as DataColumn<float>;
            if (col == null)
                throw new TypeError($"Column {i} is not of type float.");
            return col.Data;
        }

        public static double[] DataFrameColumnToArrrayFloat64(DataFrame df, int i)
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
