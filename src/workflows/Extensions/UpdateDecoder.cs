using Bonsai;
using System;
using System.ComponentModel;
using System.Linq;
using System.Reactive.Linq;
using OpenCV.Net;
using System.IO;

[Combinator]
[Description("")]
[WorkflowElementCategory(ElementCategory.Transform)]
public class UpdateDecoder
{

    [Description("The number of state vectors to update at once; must match upstream.")]
    public int BufferSize { get; set; }

    [Editor("Bonsai.Design.OpenFileNameEditor, Bonsai.Design", DesignTypes.UITypeEditor)]
    public string DecoderFileName { get; set; }

    [Editor("Bonsai.Design.OpenFileNameEditor, Bonsai.Design", DesignTypes.UITypeEditor)]
    public string DynamicsFileName { get; set; }

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
            // subscribe action (i.e. starting bonsai)
            var decoder = LoadMatrix(DecoderFileName, rows: 6);
            var dynamics = LoadMatrix(DynamicsFileName, rows: 6);
            var state = Mat.Zeros(6, BufferSize, Depth.F32, 1);
            // return our processed sequence (with decoder captured in the closure)
            return source.Select(input =>
            {
                var control = new Mat(decoder.Rows, input.Cols, decoder.Depth, decoder.Channels);
                // s_t+1 = As_t + M*e_t
                // (state_dim,num_channels)*(num_channels,acquisition_buffer_length)
                // + 
                // (state_dim,state_dim)*(state_dim,1)
                // Console.WriteLine(input.Size);
                // Console.WriteLine(decoder.Size);
                // Console.WriteLine(dynamics.Size);
                DotProduct(decoder,input,control);
                DotProduct(dynamics,state,state);
                CV.Add(control,state,state);
                // have to copy this for the outside world
                return state.Clone();
            });
        });
    }
}