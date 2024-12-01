using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Rotator : MonoBehaviour
{
    float speed = 0;
    [SerializeField]
    Vector3 axis;

    public void SetSpeed(float speed)
    {
        this.speed = speed;
    }

    private void Update()
    {
        transform.Rotate(axis * speed * Time.deltaTime);
    }
}
