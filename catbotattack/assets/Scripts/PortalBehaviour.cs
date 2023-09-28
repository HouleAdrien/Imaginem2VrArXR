using UnityEngine;
using UnityEngine.SceneManagement;

public class PortalBehaviour : MonoBehaviour
{

    void Start()
    {
    }

    void Update()
    {

    }

    void OnTriggerEnter(Collider other)
    { // OnCollisionEnter
        if (other.tag == "Player")
        {
            SceneManager.LoadScene("BossScene");
        }
    }
}