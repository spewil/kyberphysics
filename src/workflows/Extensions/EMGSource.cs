using Bonsai;
using System;
using System.ComponentModel;
using System.Collections.Generic;
using System.Linq;
using System.Reactive.Linq;
using System.Threading.Tasks;
using System.Net.Sockets;
using System.Threading;
using System.Net;
using OpenCV.Net;

// attributes == metadata (decorators)
// ElemCat == type of node
[Combinator]
[Description("")]
[WorkflowElementCategory(ElementCategory.Source)]
public class EMGSource
{
    public EMGSource()
    {
        BufferSize = 10;
        NumChannels = 8;
    }
    public int BufferSize{get;set;} 
    public int NumChannels{get;set;} 
    static short CreateCommand(int num_channels, bool start = true)
    {
        // FSAMP
        // # if MODE != 3: 0 = 500 Hz,  1 = 1000 Hz, 2 = 2000 Hz
        // # if MODE == 3: 0 = 2000 Hz, 1 = 4000 Hz, 2 = 8000 Hz
        // NCH
        // # 0 = 8 channels, 1 = 16 channels, 2 = 32 channels, 3 = 64 channels
        // MODE
        // # 0 = Monopolar, 1 = Bipolar, 2 = Differential, 3 = Accelerometers, 6 = Impedance check, 7 = Test Mode
        // Config.HRES
        // # 0 = 16 bits, 1 = 24 bits
        // HPF
        // # 0 = DC coupled, 1 = High pass filter active
        // EXTEN
        // # 0 = standard input range, 1 = double range, 2 = range x 4, 3 = range x 8
        // TRIG
        // # 0 = Data transfer and REC on SD controlled remotely, 3 = REC on SD controlled from the pushbutton
        // GETSET
        // # 0 = Set settings, 1 = Get settings (this will close the socket)
        // REC
        // 1 = record to SD card, 0 = don't

        int fsamp = 2;
        int nch = 0;
        int mode = 0;
        int hres = 1;       
        int hpf = 1;        
        int ext = 0;
        int trig = 0;
        int getset = 0;
        int rec = 0;

        if (num_channels == 8)
        {
            nch = 0;
        }
        else if (num_channels == 16)
        {
            nch = 1;
        }
        else if (num_channels == 32)
        {
            nch = 2;
        }
        else if (num_channels == 64)
        {
            nch = 3;
        }
        else
            {
                throw new Exception("Incorrect number of channels specified.");
            }

        int start_command;
        if (start)
        {
            start_command = 1;
        }
        else
        {
            start_command = 0;
        }

        int command = start_command + (rec * 2) + (trig * 4) + (ext * 16) + (hpf * 64) + (hres * 128) + (mode * 256) + (nch * 2048) + (fsamp * 8192) + (getset * 32768);

        return (short) command;
    }
    static byte[] ConvertToBytes(short command_digits)
    {
        byte[] command = BitConverter.GetBytes(command_digits);
        if (BitConverter.IsLittleEndian)
            Array.Reverse(command);
        return command;
    }
    public IObservable<byte[]> Process()
    {
        return Observable.Create<byte[]>((observer, cancellationToken) =>
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

                short start_digits = EMGSource.CreateCommand(NumChannels, true);
                short stop_digits = EMGSource.CreateCommand(NumChannels, false);
                byte[] stop_command = ConvertToBytes(stop_digits);
                byte[] start_command = ConvertToBytes(start_digits);

                Console.WriteLine("Computed start command: {0}", String.Join(",", start_digits));
                Console.WriteLine("Computed start command: {0}", String.Join(",", start_command));
                Console.WriteLine("Computed stop command: {0}", String.Join(",", stop_digits));
                Console.WriteLine("Computed stop command: {0}", String.Join(",", stop_command));

                // channels * bytes_per_sample = number of bytes per sample buffer
                var NumTotalChannels = NumChannels + 4;
                int sample_size = NumTotalChannels*3*BufferSize;
                var sample_buffer = new byte[sample_size];
                var listener = new TcpListener(new IPEndPoint(IPAddress.Parse("192.168.1.2"), 45454));
                listener.Start(1);
                Console.WriteLine("Accepting...");
                using (var client = listener.AcceptTcpClient())
                using (var stream = client.GetStream())
                {
                    Console.WriteLine("Got Stream.");
                    // Send start command to the device.
                    stream.Write(start_command, 0, start_command.Length);
                    Console.WriteLine("Sent start command.");
                    while (!cancellationToken.IsCancellationRequested)
                    {
                        var num_recvd = 0;
                        var output_buffer = new int[NumTotalChannels*BufferSize];
                        while (num_recvd < sample_buffer.Length)
                        {
                        num_recvd += stream.Read(sample_buffer, num_recvd, sample_buffer.Length-num_recvd);
                        }
                        // Array.Reverse(sample_buffer);
                        for (int i = 0; i < output_buffer.Length; i++)
                        {
                            var value = sample_buffer[i*3 + 0]*ushort.MaxValue+sample_buffer[i*3 + 1]*byte.MaxValue + sample_buffer[i*3 + 2]; 
                            if(value >= 8388608)
                            {
                                value -= 16777216;
                            }
                            output_buffer[i] = value;
                        }
                        var outputArray = Mat.FromArray(output_buffer).Reshape(1,NumTotalChannels);
                        // var transposeArray = new Mat(outputArray.Cols,outputArray.Rows,outputArray.Depth,outputArray.Channels);
                        // CV.Transpose(outputArray,transposeArray);
                        observer.OnNext(sample_buffer);
                    }
                    Console.WriteLine("Stop and shutdown.");
                    client.Client.Send(stop_command);
                    Console.WriteLine("Sent stop command.");
                    client.Client.Shutdown(SocketShutdown.Send);
                }

                // using (var socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp))
                // {
                //     socket.Bind(new IPEndPoint(IPAddress.Parse("192.168.1.2"), 45454));
                //     socket.Listen(1); // blocks
                //     Console.WriteLine("Accepting...");
                //     var connection = socket.Accept();
                //     Console.WriteLine("Connected!");
                //     while (!cancellationToken.IsCancellationRequested)
                //     {
                //         Console.WriteLine(connection);
                //         Thread.Sleep(500);
                //     }
                //     Console.WriteLine("Stop and shutdown.");
                //     connection.Send(stop_command);
                //     connection.Shutdown(SocketShutdown.Send);
                //     // socket.Shutdown(SocketShutdown.Both);
                //     connection.Close();
                //     // socket.Close();
                // }
            },
            cancellationToken,
            TaskCreationOptions.LongRunning,
            TaskScheduler.Default);
        });
    }
}

// nodes are classes
// sources == not required to have inputs 