using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GlobalConstraints : MonoBehaviour
{
    public static GlobalConstraints current;

    public bool ChatOpen = false;

    private void Awake()
    {
        if (current != null) Destroy(this);
        else current = this;
    }

    public void OpenCloseChat()
    {
        ChatOpen = !ChatOpen;
    }
}
