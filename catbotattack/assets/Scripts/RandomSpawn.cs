using System.Collections.Generic;
using UnityEngine;

public class RandomSpawn : MonoBehaviour
{
    public GameObject spawnObject;  

    private List<Vector3> positions = new List<Vector3>
    {
        new Vector3(4.67681789f, 11.2758751f, -30.9624233f),
        new Vector3(44.6899986f, 11.0500002f, -38.4300003f),
        new Vector3(-13.0200005f, 10.3500004f, 56.2000008f),
        new Vector3(31.5f, 10.0299997f, 28.4099998f),
        new Vector3(7.48000002f, 13.0100002f, 5.23999977f),
        new Vector3(-51.7999992f, 10.1899996f, 56.0800018f),
        new Vector3(43.1800003f, 10.1899996f, -53.9000015f),
        new Vector3(62.8400002f, 12.5600004f, -49.2700005f),
        new Vector3(1.5f, 11.6300001f, -35.8499985f),
        new Vector3(-56.4000015f, 13.1000004f, -18.5f)
    };

    void Awake()
    {
        Vector3 spawnPosition = positions[Random.Range(0, positions.Count)];

        Instantiate(spawnObject, spawnPosition, Quaternion.identity);
    }
}
