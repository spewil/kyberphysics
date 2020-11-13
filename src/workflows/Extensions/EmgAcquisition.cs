using Bonsai;
using System;
using System.ComponentModel;
using System.Reactive.Linq;
using System.Threading.Tasks;
using System.Net.Sockets;
using System.Net;
using OpenCV.Net;

// attributes == metadata (decorators)
// ElemCat == type of node
[Combinator]
[Description("Captures multi-channel and auxiliary analog data from an OT Bio sessanta quattro EMG device.")]
[WorkflowElementCategory(ElementCategory.Source)]
public class EmgAcquisition
{
    const string EmgAddress = "192.168.1.2";
    const int EmgPort = 45454;

    public EmgAcquisition()
    {
        BufferSize = 10;
        NumChannels = 8;
    }

    [Description("The number of samples to capture with each read command.")]
    public int BufferSize { get; set; }

    [Description("The number of channels connected to the EMG device.")]
    public int NumChannels { get; set; }

    static ushort CreateCommand(int numChannels, bool start = true)
    {
        var command =
            AcquisitionFlags.Sampling8000Hz |
            AcquisitionFlags.Monopolar |
            AcquisitionFlags.Depth24 |
            AcquisitionFlags.HighPassFilter |
            AcquisitionFlags.Range1x |
            AcquisitionFlags.TriggerExternal |
            AcquisitionFlags.RecordNone |
            AcquisitionFlags.WriteSettings |
            (start ? AcquisitionFlags.Start : AcquisitionFlags.Stop);
        switch (numChannels)
        {
            case 8: command |= AcquisitionFlags.Channels8; break;
            case 16: command |= AcquisitionFlags.Channels16; break;
            case 32: command |= AcquisitionFlags.Channels32; break;
            case 64: command |= AcquisitionFlags.Channels64; break;
            default: throw new Exception("Incorrect number of channels specified.");
        }

        return (ushort) command;
    }

    static byte[] ConvertToBytes(ushort commandDigits)
    {
        var command = BitConverter.GetBytes(commandDigits);
        if (BitConverter.IsLittleEndian)
            Array.Reverse(command);
        return command;
    }

    public IObservable<Mat> Process()
    {
        return Observable.Create<Mat>((observer, cancellationToken) =>
        {
            return Task.Factory.StartNew(() =>
            {
                // https://stackoverflow.com/questions/1318933/c-sharp-int-to-byte
                // command ints for 64 channels
                // int start_digits = 49496; // little
                // short start_digits = 22721; // big -- this is what is used
                // byte[] start_command = ConvertToBytes(start_digits); 

                // these are the digits to setup the device, add 1 to start recording
                // int stop_digits = 49240; // 0b1100000001011000; // little endian
                // short stop_digits = 22720; // 0b101100011000000; // big endian
                // byte[] stop_command = ConvertToBytes(stop_digits);
                var startDigits = CreateCommand(NumChannels, true);
                var stopDigits = CreateCommand(NumChannels, false);
                byte[] stopCommand = ConvertToBytes(stopDigits);
                byte[] startCommand = ConvertToBytes(startDigits);

                // channels * bytes_per_sample = number of bytes per sample buffer
                var NumTotalChannels = NumChannels + 4;
                int readBufferSize = NumTotalChannels * 3 * BufferSize;
                var readBuffer = new byte[readBufferSize];
                var conversionBuffer = new int[NumTotalChannels * BufferSize];
                var listener = new TcpListener(new IPEndPoint(IPAddress.Parse(EmgAddress), EmgPort));
                listener.Start(1);

                using (var cancellation = cancellationToken.Register(listener.Stop))
                using (var client = listener.AcceptTcpClient())
                using (var stream = client.GetStream())
                {
                    // Send start command to the device.
                    stream.Write(startCommand, 0, startCommand.Length);
                    while (!cancellationToken.IsCancellationRequested)
                    {
                        var bytesReceived = 0;
                        while (bytesReceived < readBuffer.Length)
                        {
                            bytesReceived += stream.Read(readBuffer, bytesReceived, readBuffer.Length - bytesReceived);
                        }

                        for (int i = 0; i < conversionBuffer.Length; i++)
                        {
                            var value = readBuffer[i * 3 + 0] * ushort.MaxValue +
                                        readBuffer[i * 3 + 1] * byte.MaxValue +
                                        readBuffer[i * 3 + 2]; 
                            if (value >= 8388608)
                            {
                                value -= 16777216;
                            }
                            conversionBuffer[i] = value;
                        }

                        var result = new Mat(NumTotalChannels, BufferSize, Depth.S32, 1);
                        using (var bufferHeader = Mat.CreateMatHeader(conversionBuffer, BufferSize, NumTotalChannels, Depth.S32, 1))
                        {
                            CV.Transpose(bufferHeader, result);
                        }
                        observer.OnNext(result);
                    }
                    client.Client.Send(stopCommand);
                    client.Client.Shutdown(SocketShutdown.Send);
                }
            },
            cancellationToken,
            TaskCreationOptions.LongRunning,
            TaskScheduler.Default);
        });
    }

    enum AcquisitionFlags : ushort
    {
        Stop = 0 << 0,
        Start = 1 << 0,

        // REC
        // 1 = record to SD card, 0 = don't
        RecordNone = 0 << 1,
        RecordSdCard = 1 << 1,

        // TRIG
        // # 0 = Data transfer and REC on SD controlled remotely, 3 = REC on SD controlled from the pushbutton
        TriggerExternal = 0 << 2,
        TriggerButton = 3 << 2,

        // EXTEN
        // # 0 = standard input range, 1 = double range, 2 = range x 4, 3 = range x 8
        Range1x = 0 << 4,
        Range2x = 1 << 4,
        Range4x = 2 << 4,
        Range8x = 3 << 4,

        // HPF
        // # 0 = DC coupled, 1 = High pass filter active
        CoupledDc = 0 << 6,
        HighPassFilter = 1 << 6,

        // Config.HRES
        // # 0 = 16 bits, 1 = 24 bits
        Depth16 = 0 << 7,
        Depth24 = 1 << 7,

        // MODE
        // # 0 = Monopolar, 1 = Bipolar, 2 = Differential, 3 = Accelerometers, 6 = Impedance check, 7 = Test Mode
        Monopolar = 0 << 8,
        Bipolar = 1 << 8,
        Differential = 2 << 8,
        Accelerometers = 3 << 8,
        ImpedanceCheck = 6 << 8,
        TestMode = 7 << 8,

        // NCH
        // # 0 = 8 channels, 1 = 16 channels, 2 = 32 channels, 3 = 64 channels
        Channels8 = 0 << 11,
        Channels16 = 1 << 11,
        Channels32 = 2 << 11,
        Channels64 = 3 << 11,

        // FSAMP
        // # if MODE != 3: 0 = 500 Hz,  1 = 1000 Hz, 2 = 2000 Hz
        // # if MODE == 3: 0 = 2000 Hz, 1 = 4000 Hz, 2 = 8000 Hz
        Sampling2000Hz = 0 << 13,
        Sampling4000Hz = 1 << 13,
        Sampling8000Hz = 2 << 13,

        // GETSET
        // # 0 = Set settings, 1 = Get settings (this will close the socket)
        WriteSettings = 0 << 15,
        ReadSettings = 1 << 15
    }
}

// nodes are classes
// sources == not required to have inputs 