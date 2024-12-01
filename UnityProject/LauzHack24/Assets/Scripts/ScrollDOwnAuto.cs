using System.Collections;
using System.Collections.Generic;
using System.Threading.Tasks;
using UnityEngine;
using UnityEngine.UI;

public class ScrollDOwnAuto : MonoBehaviour
{
    [SerializeField]
    ScrollRect scrollRect;


    public async void GoDown()
    {
        await Task.Delay(5);
        scrollRect.verticalNormalizedPosition = 0f;
    }
}
