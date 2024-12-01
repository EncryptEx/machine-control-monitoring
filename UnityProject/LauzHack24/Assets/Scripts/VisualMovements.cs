using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class VisualMovements : MonoBehaviour
{
    float engineVel;

    [SerializeField]
    Transform transmissionWheel;

    [SerializeField]
    Rotator transmissionRotator;

    private void OnEnable()
    {
        DataReciever.current.OnDataRecieved += OnDataRecieved;
    }

    private void OnDisable()
    {
        DataReciever.current.OnDataRecieved -= OnDataRecieved;
    }

    void UpdateValues()
    {
        transmissionRotator.SetSpeed(engineVel);
    }

    void OnDataRecieved(DataReciever.Data data)
    {
        engineVel = data.normalizedServoSpeed;
        UpdateValues();
    }
}
