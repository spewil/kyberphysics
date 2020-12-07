using Bonsai;
using System;
using System.ComponentModel;
using System.Reactive.Linq;
using System.Threading.Tasks;
using System.Net.Sockets;
using System.Net;
using OpenCV.Net;

[Combinator]
[Description("Captures multi-channel and auxiliary analog data from an OT Bio sessanta quattro EMG device.")]
[WorkflowElementCategory(ElementCategory.Source)]
public class FakeEMG
{
    const string EmgAddress = "192.168.1.2";
    const int EmgPort = 45454;

    public FakeEMG()
    {
        BufferSize = 10;
        NumChannels = 8;
    }

    [Description("The number of samples to capture with each read command.")]
    public int BufferSize { get; set; }

    [Description("The number of channels connected to the EMG device.")]
    public int NumChannels { get; set; }

    public IObservable<Mat> Process()
    {
        return Observable.Create<Mat>((observer) =>
        {
            var NumChannels = 32;
            var NumTotalChannels = NumChannels + 4;
            var result = new Mat(NumTotalChannels, BufferSize, Depth.S32, 1);
            var seed = 42;
            var rng = CV.Rng(seed);
            return Task.Factory.StartNew(() =>
            {
               
                var random_value = CV.RandInt(ref rng);
                result = random_value * result;
                observer.OnNext(result);
            },
            TaskCreationOptions.LongRunning,
            TaskScheduler.Default);
        });
    }
}

// nodes are classes
// sources == not required to have inputs 