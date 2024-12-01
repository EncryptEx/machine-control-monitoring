using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MovementController : MonoBehaviour
{
    [SerializeField]
    float rotSpeed = 50;
    [SerializeField]
    float zoomSpeed = 100;
    [SerializeField]
    Transform cameraTransform;

    // Update is called once per frame

    void RotateCamera()
    {
        // Get the movement axis input values (W, A, S, D / <-, ^, v, ->)
        float hor = -Input.GetAxis("Horizontal");
        float ver = -Input.GetAxis("Vertical");


        float xRot = ver * rotSpeed * Time.deltaTime;
        float yRot = hor * rotSpeed * Time.deltaTime;

        float currentXRot = transform.rotation.eulerAngles.x < 180 ? 
                                transform.rotation.eulerAngles.x : 
                                transform.rotation.eulerAngles.x - 360;

        transform.rotation = Quaternion.Euler(new Vector3(
            Mathf.Clamp(currentXRot + xRot, -90f, 90f),
            transform.rotation.eulerAngles.y + yRot,
            0));
    }

    void CameraZoom()
    {
        float scroll = Input.GetAxis("Mouse ScrollWheel");

        float newZ = cameraTransform.localPosition.z - scroll * zoomSpeed * Time.deltaTime;
        newZ = Mathf.Clamp(newZ, 10, 50);

        cameraTransform.localPosition = new Vector3(
            cameraTransform.localPosition.x, 
            cameraTransform.localPosition.y, 
            newZ);
    }

    void Update()
    {
        if (GlobalConstraints.current.ChatOpen) return;

        RotateCamera();
        CameraZoom();
    }
}
