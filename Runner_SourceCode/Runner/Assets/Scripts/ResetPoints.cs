using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ResetPoints : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        PlayerPrefs.SetInt("Points", 0);
        PlayerPrefs.Save();

        /*PlayerPrefs.SetInt("RecordPoints", 0);
        PlayerPrefs.Save();*/
    }
}
