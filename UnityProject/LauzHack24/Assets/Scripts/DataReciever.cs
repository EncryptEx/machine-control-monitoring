using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DataReciever : MonoBehaviour
{
    public static DataReciever current;
    [SerializeField]
    float requestPeriod = 2;

    public struct Data
    {
        public bool IR_LED;
        public bool isServoRunning;
        public float normalizedServoSpeed;
        public float realServoDutyCycle;
    }

    public Data lastData;

    private void Awake()
    {
        if (current != null) Destroy(this);
        else current = this;
    }

    // Start is called before the first frame update
    async void Start()
    {
        string ret = await Networking.SendGetRequest(Requests.readall);
        lastData = JsonUtility.FromJson<Data>(ret);
        OnLoadFirstData?.Invoke(lastData);
    }

    float t = 0;

    // Update is called once per frame
    void Update()
    {
        t += Time.deltaTime;
        if (t > requestPeriod)
        {
            t = 0;
            GetData();
        }
    }

    async void GetData()
    {
        string ret = await Networking.SendGetRequest(Requests.readall);
        lastData = JsonUtility.FromJson<Data>(ret);
        OnDataRecieved?.Invoke(lastData);
    }

    public event Action<Data> OnLoadFirstData;
    public event Action<Data> OnDataRecieved;
}
