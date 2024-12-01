using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Part : MonoBehaviour
{
    [SerializeField]
    Material transparentMaterial;
    [SerializeField]
    MeshRenderer[] partMeshes;
    List<Material> originalMaterial = new List<Material>();

    private void Start()
    {
        for (int i = 0; i < partMeshes.Length; i++)
        {
            originalMaterial.Add(partMeshes[i].materials[0]);
        }
    }

    public void ShowPart()
    {
        for (int i = 0; i < partMeshes.Length; i++)
        {
            partMeshes[i].material = originalMaterial[i];
        }
    }

    public void HidePart()
    {
        for (int i = 0; i < partMeshes.Length; i++)
        {
            partMeshes[i].material = transparentMaterial;
        }
    }
}
