using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.Threading.Tasks;
using UnityEngine.UI;
using System.Threading;

public class CustomToggle : MonoBehaviour
{
    bool value = false;

    [SerializeField]
    Image background;
    [SerializeField]
    Color activatedColor;
    [SerializeField]
    Color offColor;
    [SerializeField]
    Transform knob;

    CancellationTokenSource cancellationTokenSource;

    private void Start()
    {
        cancellationTokenSource = new CancellationTokenSource();
        TransitionAnimation(cancellationTokenSource.Token);
    }

    public void Toggle()
    {
        value = !value;
        OnToggle?.Invoke(value);

        cancellationTokenSource.Cancel();
        cancellationTokenSource = new CancellationTokenSource();
        TransitionAnimation(cancellationTokenSource.Token);
    }

    public void _LoadValue(bool value)
    {
        this.value = value;

        cancellationTokenSource.Cancel();
        cancellationTokenSource = new CancellationTokenSource();
        TransitionAnimation(cancellationTokenSource.Token);
    }

    public void _ToggleToValue(bool value)
    {
        this.value = value;
        OnToggle?.Invoke(value);

        cancellationTokenSource.Cancel();
        cancellationTokenSource = new CancellationTokenSource();
        TransitionAnimation(cancellationTokenSource.Token);
    }

    async void TransitionAnimation(CancellationToken cancellationToken)
    {
        float startValue = value ? 0f : 1f;
        float endValue = value ? 1f : 0f;

        float t = 0f;
        while (t < 1)
        {
            float v = Mathf.Lerp(startValue, endValue, t);

            knob.transform.localPosition = new Vector3(-15f + v * 30, 0, 0);
            background.color = Color.Lerp(offColor, activatedColor, v);

            t += 5*Time.deltaTime;
            await Task.Yield();

            if (cancellationToken.IsCancellationRequested)
            {
                print("toggle animation cancelled");
                break;
            }
        }

        if (value)
            background.color = activatedColor;
        else
            background.color = offColor;
    }

    public event Action<bool> OnToggle;
}
