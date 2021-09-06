using Bonsai;
using System;
using System.ComponentModel;
using System.Linq;
using System.Reactive.Linq;
using OpenCV.Net;
using System.IO;

[Combinator]
[Description("Converts a 2x1 or 1x2 matrix into a Vector2.")]
[WorkflowElementCategory(ElementCategory.Transform)]
public class DivideMatrices
{

    [Description("The number of state vectors to update at once; must match upstream.")]
    public int BufferSize { get; set; }
    [Editor("Bonsai.Design.OpenFileNameEditor, Bonsai.Design", DesignTypes.UITypeEditor)]
    public string ScalerFileName { get; set; }

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
            // subscribe action (i.e. starting bonsai)
            var scaler = LoadMatrix(ScalerFileName, rows: 6);

            return source.Select(value => 
            {
                // divide the scale matrix and the input matrix
                return new Mat(10,10,Depth.F32,1);
            });
        });
    }
}
