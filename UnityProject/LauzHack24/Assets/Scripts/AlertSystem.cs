using System;
using System.Collections;
using System.Collections.Generic;
using System.Threading.Tasks;
using UnityEngine;

public enum Errnos
{
    ok = 0,
    movementDetected,
    badVelocity
}

public class AlertSystem : MonoBehaviour
{
    public static AlertSystem current;

    [SerializeField]
    GameObject AlertPrefab;
    [SerializeField]
    Transform AlertsParent;

    public bool inAlert = false;

    private void Awake()
    {
        if (current != null) Destroy(this);
        else current = this;

        DataReciever.current.OnDataRecieved += OnData;
    }

    private void OnDestroy()
    {
        DataReciever.current.OnDataRecieved -= OnData;
    }

    public void Show(Errnos errno)
    {
        GameObject inst = Instantiate(AlertPrefab, AlertsParent);
        Alert alert = inst.GetComponent<Alert>();
        alert.OnAlertClosed += AlertClosed;

        switch (errno)
        {
            case Errnos.movementDetected:
                alert.SetText("Emergency break");
                break;
            case Errnos.badVelocity:
                alert.SetText("Conveyor failure");
                break;
            default:
                break;
        }
    }

    private void Update()
    {
        if (Input.GetKeyDown(KeyCode.F1))
            AlertClosed();
    }

    async void AlertClosed()
    {
        string ret = await Networking.SendGetRequest(Requests.rearm);
        inAlert = false;
        OnRestore?.Invoke();
        print(ret);
    }

    async void OnData(DataReciever.Data data)
    {
        if (data.errno != 0 && !inAlert)
        {
            Show((Errnos)data.errno);
            await Task.Yield();
            inAlert = true;
        }
    }

    public event Action OnRestore;
}
