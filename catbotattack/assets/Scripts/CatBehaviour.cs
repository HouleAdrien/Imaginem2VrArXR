using UnityEngine;

public class CatBehaviour : MonoBehaviour
{
    public GameObject fx;
    public GameObject worldObject;

    void Start()
    {
        this.worldObject = WorldInstance.Instance.worldObject;
    }

    void Update()
    {

    }

    void OnTriggerEnter(Collider other)
    { // OnCollisionEnter
        if (other.tag == "Player")
        {
            AudioSource collisionSound = WorldInstance.Instance.audioSource;
            Instantiate(fx, transform.position, Quaternion.identity);
            if (collisionSound)
            {
                collisionSound.Play();
            }
            this.worldObject.SendMessage("AddHit");
            Destroy(gameObject);
        }
    }
}