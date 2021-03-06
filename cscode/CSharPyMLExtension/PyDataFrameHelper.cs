﻿// See the LICENSE file in the project root for more information.

using System;
using System.IO;
using System.Text;
using Microsoft.ML.Runtime.Data;
using Scikit.ML.DataManipulation;
using Scikit.ML.PipelineHelper;


namespace CSharPyMLExtension
{
    /// <summary>
    /// Easier functions to use from Python.
    /// </summary>
    public static class PyDataFrameHelper
    {
        /// <summary>
        /// Captures standard output and error.
        /// </summary>
        private class StdCapture : IDisposable
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

        public static void AddColumnToDataFrameString(DataFrame df, string name, string[] values)
        {
            var bval = new DvText[values.Length];
            for (int i = 0; i < values.Length; ++i)
                bval[i] = new DvText(values[i]);
            df.AddColumn(name, bval);
        }

        /// <summary>
        /// Creates a <see cref="DataFrame"/> from a IDataView.
        /// </summary>
        public static DataFrame ReadView(IDataView view, int nrows = -1)
        {
            return DataFrameIO.ReadView(view, nrows);
        }

        /// <summary>
        /// Creates a <see cref="StreamingDataFrame"/> from a IDataView.
        /// </summary>
        public static StreamingDataFrame ReadStreamingView(IDataView view)
        {
            return new StreamingDataFrame(view);
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
        /// Reads a file as a <see cref="DataFrame"/>.
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

        /// <summary>
        /// Reads a file as a <see cref="StreamingDataFrame"/>
        /// Follows pandas API.
        /// </summary>
        public static StreamingDataFrame ReadStreamingCsv(string filename, char sep = ',', bool header = true,
                                                         string[] names = null, int[] dtypes = null,
                                                         int nrows = -1, int guess_rows = 10, string encoding = null,
                                                         bool index = false)
        {
            var kinds = IntToColumnTypes(dtypes);
            return StreamingDataFrame.ReadCsv(filename, sep, header, names, kinds, nrows, guess_rows,
                                     encoding == null ? null : Encoding.GetEncoding(encoding),
                                     index: index);
        }

        /// <summary>
        /// Reads a set of files as a <see cref="StreamingDataFrame"/>
        /// Follows pandas API.
        /// </summary>
        public static StreamingDataFrame ReadStreamingCsvs(string[] filenames, char sep = ',', bool header = true,
                                                           string[] names = null, int[] dtypes = null,
                                                           int nrows = -1, int guess_rows = 10, string encoding = null,
                                                           bool index = false)
        {
            var kinds = IntToColumnTypes(dtypes);
            return StreamingDataFrame.ReadCsv(filenames, sep, header, names, kinds, nrows, guess_rows,
                                     encoding == null ? null : Encoding.GetEncoding(encoding),
                                     index: index);
        }

        public static string DataFrameToString(DataFrame df)
        {
            using (var capture = new StdCapture())
                return df.ToString();
        }

        public static bool[] DataFrameColumnToArrayBool(DataFrame df, int i)
        {
            var col = df.GetColumn(i).Column as DataColumn<bool>;
            if (col == null)
                throw new TypeError($"Column {i} is not of type bool.");
            return col.Data;
        }

        public static int[] DataFrameColumnToArrayInt(DataFrame df, int i)
        {
            var col = df.GetColumn(i).Column as DataColumn<int>;
            if (col == null)
                throw new TypeError($"Column {i} is not of type int.");
            return col.Data;
        }

        public static uint[] DataFrameColumnToArrayUint(DataFrame df, int i)
        {
            var col = df.GetColumn(i).Column as DataColumn<uint>;
            if (col == null)
                throw new TypeError($"Column {i} is not of type uint.");
            return col.Data;
        }

        public static Int64[] DataFrameColumnToArrayInt64(DataFrame df, int i)
        {
            var col = df.GetColumn(i).Column as DataColumn<Int64>;
            if (col == null)
                throw new TypeError($"Column {i} is not of type Int64.");
            return col.Data;
        }

        public static float[] DataFrameColumnToArrayFloat(DataFrame df, int i)
        {
            var col = df.GetColumn(i).Column as DataColumn<float>;
            if (col == null)
                throw new TypeError($"Column {i} is not of type float.");
            return col.Data;
        }

        public static double[] DataFrameColumnToArrayFloat64(DataFrame df, int i)
        {
            var col = df.GetColumn(i).Column as DataColumn<double>;
            if (col == null)
                throw new TypeError($"Column {i} is not of type double.");
            return col.Data;
        }

        public static DvText[] DataFrameColumnToArrayDvText(DataFrame df, int i)
        {
            var col = df.GetColumn(i).Column as DataColumn<DvText>;
            if (col == null)
                throw new TypeError($"Column {i} is not of type string.");
            return col.Data;
        }

        public static string[] DataFrameColumnToArrayString(DataFrame df, int i)
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
