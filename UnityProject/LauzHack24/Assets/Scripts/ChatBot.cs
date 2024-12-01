using System.Collections;
using System.Collections.Generic;
using System.Threading.Tasks;
using UnityEngine;
using UnityEngine.UI;

public class ChatBot : MonoBehaviour
{
    [SerializeField]
    GameObject bobTextPrefab, meTextPrefab;

    [SerializeField]
    Transform content;

    [SerializeField]
    ScrollRect scrollRect;

    public bool test;
    private void Update()
    {
        if (test)
        {
            test = false;
            InsertNewText(Random.Range(0, 2) == 0, "This is some random text to prove if this thing works correctly!");
        }
    }

    async void InsertNewText(bool isBob, string txt)
    {
        GameObject inst = Instantiate(isBob ? bobTextPrefab : meTextPrefab, content);
        ChatText text = inst.GetComponent<ChatText>();
        text.SetText(txt);

        await Task.Delay(10);
        scrollRect.verticalNormalizedPosition = 0f;
    }
}
