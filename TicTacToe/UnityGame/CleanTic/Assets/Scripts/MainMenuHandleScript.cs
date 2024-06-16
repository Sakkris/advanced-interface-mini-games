using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MainMenuHandleScript : MonoBehaviour
{
    [SerializeField] private GameObject mainMenuUI;
    [SerializeField] private GameObject gameUI;
    [SerializeField] private GameObject endUI;


    private void Start()
    {
        mainMenuUI.SetActive(true);
        gameUI.SetActive(false);
        endUI.SetActive(false);
    }

    public void PlayGameButton()
    {
        mainMenuUI.SetActive(false);
        gameUI.SetActive(true);
    }

    public void ExitGameButton()
    {
#if UNITY_EDITOR
        UnityEditor.EditorApplication.isPlaying = false;
#else
				Application.Quit();
#endif
    }
}
