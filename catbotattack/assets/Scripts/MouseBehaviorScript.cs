using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MouseBehaviorScript : MonoBehaviour
{
    [SerializeField]
    private float speed = 5.0F;

    void Start()
    {
        
    }

    public void Update()
    {
        float speed = 5.0F; 
        float x = Input.GetAxis("Horizontal") * Time.deltaTime * speed;
        float z = Input.GetAxis("Vertical") * Time.deltaTime * speed;
        transform.Translate(x, 0, z);
    }
}
