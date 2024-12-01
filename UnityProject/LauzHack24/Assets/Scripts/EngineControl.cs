using System.Collections;
using System.Collections.Generic;
using TMPro;
using Unity.VisualScripting;
using UnityEngine;
using UnityEngine.UI;

public class EngineControl : MonoBehaviour
{
    public static EngineControl current;

    private void Awake()
    {
        if (current != null) Destroy(this);
        else current = this;
    }

    [SerializeField]
    public CustomToggle powerToggle, reverseToggle;
    [SerializeField]
    public Slider velocitySlider;
    [SerializeField]
    TextMeshProUGUI Vtxt, Itxt, Ptxt, VelTxt, errnoTxt;

    public float velocity = 0;
    bool reversed = false;
    bool powered = false;

    private void OnEnable()
    {
        powerToggle.OnToggle += OnPowerChanged;
        reverseToggle.OnToggle += OnReverseChanged;
        DataReciever.current.OnLoadFirstData += OnFirstData;
        DataReciever.current.OnDataRecieved += OnData;
        AlertSystem.current.OnRestore += ResetVisuals;
    }

    private void OnDisable()
    {
        powerToggle.OnToggle -= OnPowerChanged;
        reverseToggle.OnToggle -= OnReverseChanged;
        DataReciever.current.OnLoadFirstData -= OnFirstData;
        DataReciever.current.OnDataRecieved -= OnData;
        AlertSystem.current.OnRestore -= ResetVisuals;
    }

    void OnPowerChanged(bool value)
    {
        powered = value;

        if (powered)
            SendVelocity();
        else
            SendPowerOff();
    }

    void OnReverseChanged(bool value)
    {
        reversed = value;
        SendVelocity();
    }

    public void OnSpeedChanged()
    {
        velocity = velocitySlider.value;
        SendVelocity();
    }

    async void SendVelocity()
    {
        if (!powered) return;

        float vel = reversed ? -velocity : velocity;
        string ret = await Networking.SendGetRequest(Requests.changeVelocity, vel.ToString());
    }

    async void SendPowerOff()
    {
        string ret = await Networking.SendGetRequest(Requests.powerOff);
    }

    void ResetVisuals()
    {
        powered = false;
        velocity = 0;

        reverseToggle._LoadValue(false);
        velocitySlider.SetValueWithoutNotify(0);
        powerToggle._LoadValue(false);
    }

    void OnData(DataReciever.Data data)
    {
        if (data.errno != 0 && !AlertSystem.current.inAlert)
        {
            ResetVisuals();
        }

        UpdateConstraints(data);
    }

    void OnFirstData(DataReciever.Data data)
    {
        powered = data.isServoRunning;
        velocity = Mathf.Abs(data.normalizedServoSpeed);

        reverseToggle._LoadValue(data.normalizedServoSpeed < 0);
        velocitySlider.SetValueWithoutNotify(velocity);
        powerToggle._LoadValue(data.isServoRunning);
    }

    void UpdateConstraints(DataReciever.Data data)
    {
        Vtxt.text = $"Voltage: {data.voltage}V";
        Itxt.text = $"Intensity: {(int)(data.current * 1000)}mA";
        Ptxt.text = $"Power: {(int)(data.power * 1000)}mW";
        VelTxt.text = $"Conveyor speed: {(int)(data.realVelocity * 1000)}mm/s";

        switch (data.errno)
        {
            case 0:
                errnoTxt.text = "System state: Ok";
                break;
            case 1:
                errnoTxt.text = "System state: Blocked (emergency break)";
                break;
            case 2:
                errnoTxt.text = "System state: Blocked (conveyor failure)";
                break;
            default:
                break;
        }
    }
}
