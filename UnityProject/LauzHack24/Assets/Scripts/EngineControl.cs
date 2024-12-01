using System.Collections;
using System.Collections.Generic;
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

    public float velocity = 0;
    bool reversed = false;
    bool powered = false;

    private void OnEnable()
    {
        powerToggle.OnToggle += OnPowerChanged;
        reverseToggle.OnToggle += OnReverseChanged;
        DataReciever.current.OnLoadFirstData += OnFirstData;
    }

    private void OnDisable()
    {
        powerToggle.OnToggle -= OnPowerChanged;
        reverseToggle.OnToggle -= OnReverseChanged;
        DataReciever.current.OnLoadFirstData -= OnFirstData;
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

    void OnFirstData(DataReciever.Data data)
    {
        powered = data.isServoRunning;
        velocity = Mathf.Abs(data.normalizedServoSpeed);

        reverseToggle._LoadValue(data.normalizedServoSpeed < 0);
        velocitySlider.SetValueWithoutNotify(velocity);
        powerToggle._LoadValue(data.isServoRunning);
    }
}
