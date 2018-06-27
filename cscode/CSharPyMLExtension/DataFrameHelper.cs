// See the LICENSE file in the project root for more information.

using System;
using Microsoft.ML.Runtime.Data;
using Microsoft.ML.Ext.DataManipulation;


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

        /// <summary>
        /// Adds a column to an existing dataframe.
        /// Column type is generic. Data is copied.
        /// </summary>
        /// <param name="df">DataFrame</param>
        /// <param name="name">column name</param>
        /// <param name="values">values (must not be empty)</param>
        static void AddGenericColumnToDataFrame<DType>(DataFrame df, string name, DType[] values, bool copy)
            where DType : IEquatable<DType>, IComparable<DType>
        {
            DType[] col;
            if (copy)
            {
                col = new DType[values.Length];
                for (int i = 0; i < values.Length; ++i)
                    col[i] = values[i];
            }
            else
                col = values;
            df.AddColumn(name, col);
        }

        public static void AddColumnToDataFrame(DataFrame df, string name, bool[] values)
        {
            var bval = new DvBool[values.Length];
            for (int i = 0; i < values.Length; ++i)
                bval[i] = values[i];
            AddGenericColumnToDataFrame(df, name, values, false);
        }

        public static void AddColumnToDataFrame(DataFrame df, string name, Int32[] values)
        {
            var bval = new DvInt4[values.Length];
            for (int i = 0; i < values.Length; ++i)
                bval[i] = values[i];
            AddGenericColumnToDataFrame(df, name, values, false);
        }

        public static void AddColumnToDataFrame(DataFrame df, string name, Int64[] values)
        {
            var bval = new DvInt8[values.Length];
            for (int i = 0; i < values.Length; ++i)
                bval[i] = values[i];
            AddGenericColumnToDataFrame(df, name, values, false);
        }

        public static void AddColumnToDataFrame(DataFrame df, string name, float[] values)
        {
            AddGenericColumnToDataFrame(df, name, values, true);
        }

        public static void AddColumnToDataFrame(DataFrame df, string name, double[] values)
        {
            AddGenericColumnToDataFrame(df, name, values, true);
        }

        public static void AddColumnToDataFrame(DataFrame df, string name, string[] values)
        {
            var bval = new DvText[values.Length];
            for (int i = 0; i < values.Length; ++i)
                bval[i] = new DvText(values[i]);
            AddGenericColumnToDataFrame(df, name, values, false);
        }

        /// <summary>
        /// Reads a string as a IDataView.
        /// Follows pandas API.
        /// </summary>
        public static DataFrame ReadStr(string content, char sep = ',', bool header = true,
                                    string[] names = null, int[] dtypes = null,
                                    int nrows = -1, int guess_rows = 10)
        {
            DataKind?[] kinds = null;
            if (dtypes != null)
            {
                kinds = new DataKind?[dtypes.Length];
                for (int i = 0; i < kinds.Length; ++i)
                    kinds[i] = dtypes[i] < 0 ? (DataKind?)null : (DataKind?)(DataKind)dtypes[i];
            }
            return DataFrame.ReadStr(content, sep, header, names, kinds, nrows, guess_rows);
        }

        /// <summary>
        /// Reads a string as a IDataView.
        /// Follows pandas API.
        /// </summary>
        public static DataFrame ReadCsv(string filename, char sep = ',', bool header = true,
                                    string[] names = null, int[] dtypes = null,
                                    int nrows = -1, int guess_rows = 10)
        {
            DataKind?[] kinds = null;
            if (dtypes != null)
            {
                kinds = new DataKind?[dtypes.Length];
                for (int i = 0; i < kinds.Length; ++i)
                    kinds[i] = dtypes[i] < 0 ? null : (DataKind?)(DataKind)dtypes[i];
            }
            return DataFrame.ReadCsv(filename, sep, header, names, kinds, nrows, guess_rows);
        }

        public static string DataFrameToString(DataFrame df)
        {
            using (var capture = new StdCapture())
            {
                return df.ToString();
            }
        }
    }
}
