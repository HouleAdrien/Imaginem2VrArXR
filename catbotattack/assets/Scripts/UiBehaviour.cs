using TMPro;
using UnityEngine;
using System.Collections;
using UnityEngine.SceneManagement;

public class UIBehaviour : MonoBehaviour
{
    public TMP_Text headText;
    public TMP_Text timerText;
    public GameObject portal;
    public int CatsToFound = 10;
    int nbCats = 0;


    void Start()
    {
        int hours = (int)(WorldInstance.Instance.currentTime / 3600);
        int minutes = (int)((WorldInstance.Instance.currentTime % 3600) / 60);
        int seconds = (int)(WorldInstance.Instance.currentTime % 60);

        timerText.text = string.Format("Temp restant : {0} h {1} min {2} s", hours, minutes, seconds);
        if(SceneManager.GetActiveScene().name != "BossScene")
        {
            headText.text = "Catbots touchés : " + nbCats + "/" + CatsToFound;
        }
        

        StartCoroutine(TimerTick());
    }

    void Update()
    {
    }

    public void AddHit()
    {
        if (SceneManager.GetActiveScene().name != "BossScene" && nbCats < CatsToFound)
        {
            nbCats++;
            headText.text = "Catbots touchés : " + nbCats + "/" + CatsToFound;
            if (nbCats == CatsToFound)
            {
                portal.SetActive(true);
                headText.text = "Va vers le portail le plus vite possible pour passer a la suite !!!";
            }
        }
    }

    IEnumerator TimerTick()
    {
        while (WorldInstance.Instance.currentTime > 0)
        {
            yield return new WaitForSeconds(1);
            WorldInstance.Instance.currentTime--;

            int hours = (int)(WorldInstance.Instance.currentTime / 3600);
            int minutes = (int)((WorldInstance.Instance.currentTime % 3600) / 60);
            int seconds = (int)(WorldInstance.Instance.currentTime % 60);

            timerText.text = string.Format("Temp restant : {0} h {1} min {2} s", hours, minutes, seconds);
        }

        SceneManager.LoadScene("dragonHouse");
    }
}
