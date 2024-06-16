using System;
using System.Net;
using System.Net.Sockets;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading;
using UnityEditor.PackageManager.UI;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.InputSystem.LowLevel;
using UnityEngine.UI;

public class HandRecognitionServer : MonoBehaviour
{
    // Variables for the TCP server
    private TcpListener server;
    private Thread serverThread;

    // Variables to keep the last info given by Pitão
    private Vector2 fingerPosition = new Vector2(0,0);
    private string gesture;
    private bool isRightHandDetected = false;
    private bool isLeftHandDetected = false;

    // Other variables
    [SerializeField] private RectTransform virtualMouse;
    [SerializeField] private float clickTimerCooldown = 3f;
    private float clickTimer = 0f;
    private bool clickTimerLockedOut = false;

    private void Start()
    {
        clickTimer = clickTimerCooldown;

        serverThread = new Thread(StartServer);
        serverThread.Start();
    }

    private void Update()
    {
        // Update cursor position only right hand is detected
        if (isRightHandDetected)
        {
            Debug.Log("Here");
            Vector3 cursorPosition = new Vector3(fingerPosition.x, (Screen.height - fingerPosition.y), 0);

            virtualMouse.anchoredPosition = cursorPosition;
            Mouse.current.WarpCursorPosition(cursorPosition);
        } else
        {
            // If right hand is not detected, make the cursor game object follow the real mouse
            virtualMouse.anchoredPosition = Input.mousePosition;
        }


        // Timer Cooldown for clicking, otherwise this will be spammed :D
        if (clickTimerLockedOut)
        {
            clickTimer -= Time.deltaTime;

            if (clickTimer <= 0f)
            {
                clickTimer = clickTimerCooldown;
                clickTimerLockedOut = false;
            }
        }

        // Handle gestures only if left hand is detected
        if (isLeftHandDetected)
        {
            if (!clickTimerLockedOut && String.Equals(gesture, "click"))
            {
                clickTimerLockedOut = true;

                Debug.Log("Clicked for sure");
                MouseOperations.MouseEvent(MouseOperations.MouseEventFlags.LeftUp | MouseOperations.MouseEventFlags.LeftDown);
            }
        }
    }

    private void StartServer()
    {
        server = new TcpListener(IPAddress.Any, 1313);
        server.Start();
        Debug.Log("Server started, waiting for connections...");

        while (true)
        {
            try
            {
                TcpClient client = server.AcceptTcpClient();
                Debug.Log("Client connected");

                NetworkStream stream = client.GetStream();

                byte[] buffer = new byte[1024];
                int bytesRead = stream.Read(buffer, 0, buffer.Length);
                string data = Encoding.UTF8.GetString(buffer, 0, bytesRead);

                var gestureData = JsonUtility.FromJson<GestureData>(data);
                
                fingerPosition = new Vector2(gestureData.x, gestureData.y);
                gesture = gestureData.gesture;
                isRightHandDetected = gestureData.right_hand_detected;
                isLeftHandDetected = gestureData.left_hand_detected;

                client.Close();
            }
            catch (Exception e)
            {
                Debug.LogError($"Server exception: {e}");
            }
        }
    }

    public void OnApplicationQuit()
    {
        server.Stop();
        serverThread.Abort();
    }
}

[Serializable]
public class GestureData
{
    public float x;
    public float y;
    public string gesture;
    public bool right_hand_detected;
    public bool left_hand_detected;
}


/* *
 * As seen here:
 *  https://discussions.unity.com/t/how-can-i-control-the-mouse-move-and-send-mouse-click-signals-via-the-keyboard/85297/2
 * */
public class MouseOperations
{
    [Flags]
    public enum MouseEventFlags
    {
        LeftDown = 0x00000002,
        LeftUp = 0x00000004,
        MiddleDown = 0x00000020,
        MiddleUp = 0x00000040,
        Move = 0x00000001,
        Absolute = 0x00008000,
        RightDown = 0x00000008,
        RightUp = 0x00000010
    }

    [DllImport("user32.dll", EntryPoint = "SetCursorPos")]
    [return: MarshalAs(UnmanagedType.Bool)]
    private static extern bool SetCursorPos(int x, int y);

    [DllImport("user32.dll")]
    [return: MarshalAs(UnmanagedType.Bool)]
    private static extern bool GetCursorPos(out MousePoint lpMousePoint);

    [DllImport("user32.dll")]
    private static extern void mouse_event(int dwFlags, int dx, int dy, int dwData, int dwExtraInfo);

    public static void SetCursorPosition(int x, int y)
    {
        SetCursorPos(x, y);
    }

    public static void SetCursorPosition(MousePoint point)
    {
        SetCursorPos(point.X, point.Y);
    }

    public static MousePoint GetCursorPosition()
    {
        MousePoint currentMousePoint;
        var gotPoint = GetCursorPos(out currentMousePoint);
        if (!gotPoint) { currentMousePoint = new MousePoint(0, 0); }
        return currentMousePoint;
    }

    public static void MouseEvent(MouseEventFlags value)
    {
        MousePoint position = GetCursorPosition();

        mouse_event
            ((int)value,
             position.X,
             position.Y,
             0,
             0)
            ;
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct MousePoint
    {
        public int X;
        public int Y;

        public MousePoint(int x, int y)
        {
            X = x;
            Y = y;
        }
    }
}