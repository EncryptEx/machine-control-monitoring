using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class ChatText : MonoBehaviour
{
    TextMeshProUGUI text;

    public void SetText(string txt)
    {
        text = GetComponent<TextMeshProUGUI>();

        text.text = txt;
    }
}
