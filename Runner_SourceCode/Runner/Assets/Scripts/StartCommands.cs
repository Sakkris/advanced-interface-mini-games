using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.Windows.Speech;
using UnityEngine.SceneManagement;

public class StartCommands : MonoBehaviour
{

    private KeywordRecognizer keywordRecognizer;
    private Dictionary<string, Action> actions = new Dictionary<string, Action>();

    private void Start()
    {
        actions.Add("start", StartButton);
        actions.Add("how to", HowToButton);
        actions.Add("exit", ExitButton);

        keywordRecognizer = new KeywordRecognizer(actions.Keys.ToArray());
        keywordRecognizer.OnPhraseRecognized += RecognizedSpeech;
        keywordRecognizer.Start();
    }

    private void RecognizedSpeech(PhraseRecognizedEventArgs speech)
    {
        Debug.Log(speech.text);
        actions[speech.text].Invoke();
    }

    private void StartButton()
    {
        SceneManager.LoadScene("RunnerGame");
    }

    private void HowToButton()
    {
        SceneManager.LoadScene("HowTo");
    }

    private void ExitButton()
    {
        Application.Quit();
    }

}
