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
    public IObservable<int> Process()
    {
        return Observable.Create<int>((observer, cancellationToken) =>
        {
            return Task.Factory.StartNew(() =>
            {
                // https://stackoverflow.com/questions/1318933/c-sharp-int-to-byte
                int stop_digits = 49240; // 0b1100000001011000; // little endian
                // int stop_command = 22720; // 0b101100011000000; // big endian
                byte[] intBytes = BitConverter.GetBytes(stop_digits);
                if (BitConverter.IsLittleEndian)
                    Array.Reverse(intBytes);
                byte[] stop_command = intBytes;
                Console.WriteLine("stop command", stop_command.ToString());
                using (var client = new TcpClient("192.168.1.2", 45454))
                // using (var socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp))
                {
                    client.Connect("192.168.1.2", 45454);
                    Console.WriteLine("Connected!");
                    NetworkStream stream = client.GetStream();

                    Byte[] data = System.Text.Encoding.ASCII. GetBytes(message);

                    // Send the message to the connected TcpServer.
                    stream.Write(data, 0, data.Length);

                    Console.WriteLine("Sent: {0}", message);

                    // Receive the TcpServer.response.

                    // Buffer to store the response bytes.
                    data = new Byte[256];

                    // String to store the response ASCII representation.
                    String responseData = String.Empty;

                    // Read the first batch of the TcpServer response bytes.
                    Int32 bytes = stream.Read(data, 0, data.Length);
                    responseData = System.Text.Encoding.ASCII.GetString(data, 0, bytes);
                    Console.WriteLine("Received: {0}", responseData);

                    // Close everything.
                    stream.Close();
                    client.Close();

                    while (!cancellationToken.IsCancellationRequested)
                    {
                        Console.WriteLine(client.ToString());
                        Thread.Sleep(500);
                    }
                    Console.WriteLine("Closing connection and socket.");

                    // socket.Bind(new IPEndPoint(IPAddress.Parse("192.168.1.2"), 45454));
                    // socket.Listen(1); // blocks
                    // Console.WriteLine("Accepting...");
                    // var connection = socket.Accept();
                    // Console.WriteLine("Connected!");
                    // connection.Send(stop_command);
                    // connection.Shutdown(SocketShutdown.Send);
                    // socket.Shutdown(SocketShutdown.Both);
                    // connection.Close();
                    // socket.Close();
                }
            },
            cancellationToken,
            TaskCreationOptions.LongRunning,
            TaskScheduler.Default);
        });
    }
}

// nodes are classes
// sources == not required to have inputs 