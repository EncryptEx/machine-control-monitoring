using System;
using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class Alert : MonoBehaviour
{
    [SerializeField]
    TextMeshProUGUI titleText;
    [SerializeField]
    Animator anim;

    public void SetText(string title)
    {
        titleText.text = title;
    }

    public void Close()
    {
        anim.SetTrigger("Close");
        OnAlertClosed?.Invoke();
    }

    public void DestroyAlert()
    {
        Destroy(gameObject);
    }

    public event Action OnAlertClosed;
}
