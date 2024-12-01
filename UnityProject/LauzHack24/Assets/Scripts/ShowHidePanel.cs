using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ShowHidePanel : MonoBehaviour
{
    Animator anim;

    bool shown = false;

    private void Start()
    {
        anim = GetComponent<Animator>();
    }

    public void Show()
    {
        shown = !shown;
        anim.SetBool("Shown", shown);
    }
}
