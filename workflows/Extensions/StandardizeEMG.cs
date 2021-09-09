using Bonsai;
using System;
using System.ComponentModel;
using System.Collections.Generic;
using System.Linq;
using System.Reactive.Linq;
using OpenCV.Net;
using System.IO;

[Combinator]
[Description("Divide channels by diagonal variance array from file.")]
[WorkflowElementCategory(ElementCategory.Transform)]
public class StandardizeEMG
{

    [Editor("Bonsai.Design.OpenFileNameEditor, Bonsai.Design", DesignTypes.UITypeEditor)]
    public string VarianceFileName { get; set; }

    [Description("The dimensionality of the EMG; must match upstream.")]
    public int NumChannels { get; set; }

    static void DotProduct(Mat lhs, Mat rhs, Mat result)
    {
        CV.GEMM(lhs,rhs,1,null,1,result);
    }

    static Mat LoadMatrix(string fileName, int rows = 0, int cols = 0)
    {
        if (rows == 0 && cols == 0) throw new ArgumentException("At least one of the dimensions must be non-zero.", "rows");
        using (var stream = File.OpenRead(fileName))
        using (var reader = new BinaryReader(stream))
        {
            rows = rows == 0 ? (int)stream.Length / cols / sizeof(float) : rows;
            cols = cols == 0 ? (int)stream.Length / rows / sizeof(float) : cols;
            var data = new byte[stream.Length];
            reader.Read(data, 0, data.Length);
            return Mat.FromArray(data, rows, (int)cols, Depth.F32, 1);
        }
    }

    public IObservable<Mat> Process(IObservable<Mat> source)
    {   
         
        return Observable.Defer(() =>
        {
            var variance = LoadMatrix(VarianceFileName, rows: NumChannels, cols: NumChannels+4);

        return source.Select(input => 
        {
            //     V . EMG 
            // 64x68 . 68xbuffer
            var result = new Mat(variance.Rows, input.Cols, variance.Depth, variance.Channels);
            DotProduct(variance,input,result);
            return result.Clone();

        });
        });
    }
}