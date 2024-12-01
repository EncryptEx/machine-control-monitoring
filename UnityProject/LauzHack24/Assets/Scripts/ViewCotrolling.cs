using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public enum ContraptionPart
{
    casing,
    engine,
    belt,
    transmition
};

public class ViewCotrolling : MonoBehaviour
{
    [SerializeField]
    GameObject[] unShownSprite;
    [SerializeField]
    GameObject[] focusedSprite;
    [SerializeField]
    Part[] parts;
    [SerializeField]
    Material transparentMaterial;

    private Dictionary<ContraptionPart, bool> ShownParts = new Dictionary<ContraptionPart, bool>()
    {
        { ContraptionPart.casing, true },
        { ContraptionPart.engine, true },
        { ContraptionPart.belt, true },
        { ContraptionPart.transmition, true }
    };

    int focusedPart = -1;

    void UnFocusButtons()
    {
        for (int i = 0; i < focusedSprite.Length; i++)
        {
            focusedSprite[i].SetActive(false);
        }
    }

    void FocusButton(int i)
    {
        focusedSprite[i].SetActive(true);
    }


    void UpdateShownButtonState(int i)
    {
        if (ShownParts[(ContraptionPart)i])
        {
            unShownSprite[i].SetActive(false);
        }
        else
        {
            unShownSprite[i].SetActive(true);
        }
    }

    void UpdateShowState()
    {
        for (int i = 0; i < parts.Length; i++)
        {
            if (ShownParts[(ContraptionPart)i])
                parts[i].ShowPart();
            else
                parts[i].HidePart();
        }
    }

    public void FocusPressed(int part_id)
    {
        UnFocusButtons();
        
        if (focusedPart == part_id)
        {
            focusedPart = -1;   
        }
        else
        {
            focusedPart = part_id;

            for (int i = 0; i < parts.Length; i++)
            {
                ShownParts[(ContraptionPart)i] = false;
                UpdateShownButtonState(i);
            }
            ShownParts[(ContraptionPart)part_id] = true;
            UpdateShownButtonState(part_id);

            FocusButton(part_id);
        }

        UpdateShowState();
        
    }

    public void ShowHide(int part_id)
    {
        if (focusedPart != -1)
            FocusPressed(focusedPart);

        ContraptionPart part = (ContraptionPart)part_id;
        ShownParts[part] = !ShownParts[part];

        UpdateShownButtonState(part_id);
        UpdateShowState();
    } 

    public void ChangeAll(bool value)
    {
        if (focusedPart != -1)
            FocusPressed(focusedPart);

        for (int i = 0; i < parts.Length; i++)
        {
            ShownParts[(ContraptionPart)i] = value;
            UpdateShownButtonState(i);
        }

        UpdateShowState();
    }
}
