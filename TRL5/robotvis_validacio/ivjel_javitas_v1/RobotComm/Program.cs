using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Globalization;
//using HSEthernet;

//namespace HSEthernet
//{
public class Program
{
    private const int TIMEOUT = 2000;
    private const int RETRY = 5;

    private bool stub = false;

    // Ívjel a robotvezérlő I/O-jából (HSE IORead). -1 = kikapcsolva, ekkor az üzenet a régi 6 mezős formátum.
    // A logikai számot és a bitet a cella I/O-kiosztásából kell megadni: --arc-io <logikai szám> --arc-bit <0..7>
    private int arcIo = -1;
    private int arcBit = 0;

    HSEClient hsec;
    TcpListener server;

    public Program(string IPAddress, bool stub, int arcIo, int arcBit)
    {
        this.stub = stub;
        this.arcIo = arcIo;
        this.arcBit = arcBit;

        if (arcIo >= 0) {
            Console.WriteLine("Arc signal from robot I/O: logical number " + arcIo + ", bit " + arcBit);
        }

        Console.WriteLine("Setting up connection to the robot at " + IPAddress + " ...");

        hsec = new HSEClient(IPAddress, TIMEOUT, RETRY);

        if (!stub) {
            // We need to query something, HSEClient doesn't seem to have methods to just query connection status / connect
            GetCoordinates();
        }

        Console.WriteLine("Robot connection has been setup.");
    }

    private string GetCoordinates()
    {
        RobotPositionCoordinate robotPos;

        string coords = "";

        if (hsec.GetRobotPosition(1, HSEClientCoordinateType.Robot, 1, out robotPos).IsOk)
        {
            
            coords += Convert.ToString(robotPos.X, CultureInfo.InvariantCulture) + ",";
            coords += Convert.ToString(robotPos.Y, CultureInfo.InvariantCulture) + ",";
            coords += Convert.ToString(robotPos.Z, CultureInfo.InvariantCulture) + ",";
            coords += Convert.ToString(robotPos.Rx, CultureInfo.InvariantCulture) + ",";
            coords += Convert.ToString(robotPos.Ry, CultureInfo.InvariantCulture) + ",";
            coords += Convert.ToString(robotPos.Rz, CultureInfo.InvariantCulture);

            if (arcIo >= 0) {
                byte io;
                // 7. mező: 1 = ív, 0 = nincs ív, -1 = az I/O olvasása nem sikerült
                if (hsec.IORead(arcIo, out io).IsOk) {
                    coords += "," + (((io >> arcBit) & 1) == 1 ? "1" : "0");
                } else {
                    coords += ",-1";
                }
            }
        }

        coords += ";";

        return coords;
    }

    double stubx = 641;
    int steps = 0;

    private string GetCoordinatesStub()
    {
        steps += 1;

        if (steps > 10) {
            //641.141
            stubx += 0.0001;
            steps = 0;
        }

        if (arcIo >= 0) {
            return stubx + ",0.011,340.194,0.0078,74.4678,0.0097,0;";
        }

        return stubx + ",0.011,340.194,0.0078,74.4678,0.0097;";
    }

    public void MainLoop()
    {
        TcpListener server = new TcpListener(IPAddress.Any, 9999);
        // we set our IP address as server's address, and we also set the port: 9999

        server.Start();  // this will start the server

        Console.WriteLine("Waiting for RobotVis client!");

        while (true)   //we wait for a connection
        {
            TcpClient client = server.AcceptTcpClient();  //if a connection exists, the server will accept it

            Console.WriteLine("RobotVis client connected!");

            NetworkStream ns = client.GetStream(); //networkstream is used to send/receive messages

            try
            {
                while (client.Connected)  //while the client is connected, we look for incoming messages
                {
                    string coords = GetCoordinates();

                    byte[] bts = Encoding.ASCII.GetBytes(coords);

                    ns.Write(bts, 0, bts.Length);     //sending the message
                    //Console.WriteLine(coords);
                }

                Console.WriteLine("RobotVis client disconnected!");
            }
            catch (Exception)
            {
                //ignore
                Console.WriteLine("RobotVis client disconnected!");
            }
        }

    }

    public void MainLoopStub()
    {
        TcpListener server = new TcpListener(IPAddress.Any, 9999);
        // we set our IP address as server's address, and we also set the port: 9999

        server.Start();  // this will start the server

        Console.WriteLine("Waiting for RobotVis client!");

        while (true)   //we wait for a connection
        {
            TcpClient client = server.AcceptTcpClient();  //if a connection exists, the server will accept it

            Console.WriteLine("RobotVis client connected!");

            NetworkStream ns = client.GetStream(); //networkstream is used to send/receive messages

            try
            {
                while (client.Connected)  //while the client is connected, we look for incoming messages
                {
                    string coords = GetCoordinatesStub();

                    byte[] bts = Encoding.ASCII.GetBytes(coords);

                    ns.Write(bts, 0, bts.Length);     //sending the message
                    //Console.WriteLine(coords);
                }

                Console.WriteLine("RobotVis client disconnected!");
            }
            catch (Exception)
            {
                //ignore
                Console.WriteLine("RobotVis client disconnected!");
            }
        }

    }


    public static void Main(string[] args)
    {
        bool stub = false;
        int arcIo = -1;
        int arcBit = 0;

        for (int i = 0; i < args.Length; ++i) {
            if (args[i] == "--stub") {
                stub = true;

                Console.WriteLine("Using stub client!");
            } else if (args[i] == "--arc-io" && i + 1 < args.Length) {
                arcIo = int.Parse(args[++i], CultureInfo.InvariantCulture);
            } else if (args[i] == "--arc-bit" && i + 1 < args.Length) {
                arcBit = int.Parse(args[++i], CultureInfo.InvariantCulture);
            }
        }

        Program p = new Program("10.192.70.130", stub, arcIo, arcBit);

        if (!stub) {
            p.MainLoop();
        } else {
            p.MainLoopStub();
        }
    }
}
//}
