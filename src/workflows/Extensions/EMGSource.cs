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
        NumChannels = 64;
    }
    public int BufferSize{get;set;} 
    public int NumChannels{get;set;} 
    public IObservable<int[]> Process()
    {
        return Observable.Create<int[]>((observer, cancellationToken) =>
        {
            return Task.Factory.StartNew(() =>
            {
                // https://stackoverflow.com/questions/1318933/c-sharp-int-to-byte
                // int start_digits = 49496; // little
                short start_digits = 22721; // big
                byte[] start_command = BitConverter.GetBytes(start_digits);
                if (BitConverter.IsLittleEndian)
                    Array.Reverse(start_command);
                Console.WriteLine("start command {0}", String.Join(",", start_command));

                // int stop_digits = 49240; // 0b1100000001011000; // little endian
                short stop_digits = 22720; // 0b101100011000000; // big endian
                byte[] stop_command = BitConverter.GetBytes(stop_digits);
                if (BitConverter.IsLittleEndian)
                    Array.Reverse(stop_command);
                Console.WriteLine("stop command {0}", String.Join(",", stop_command));

                // channels * bytes_per_sample
                int sample_size = 68*3*BufferSize;
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
                    while (!cancellationToken.IsCancellationRequested)
                    {
                        var num_recvd = 0;
                        var output_buffer = new int[68*BufferSize];
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
                        // Console.WriteLine(num_recvd);

                        // Thread.Sleep(500);
                        observer.OnNext(output_buffer);
                    }
                    Console.WriteLine("Stop and shutdown.");
                    client.Client.Send(stop_command);
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