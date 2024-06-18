using System;
using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.UI;
using WebSocketSharp;

public class GameHandleScript : MonoBehaviour
{
    [Header("Sprites")]
    [SerializeField] private Sprite xSprite;
    [SerializeField] private Sprite oSprite;
    [SerializeField] private Sprite emptySprite;
    [SerializeField] private Sprite cleanMainBackground;
    [SerializeField] private Sprite cameraMainBackground;
    [SerializeField] private Sprite cleanGameBackground;
    [SerializeField] private Sprite cameraGameBackground;

    [Header("Buttons")]
    [SerializeField] private Button[] gameButtons;

    [Header("UI")]
    [SerializeField] private GameObject mainMenuUI;
    [SerializeField] private GameObject gameUI;
    [SerializeField] private GameObject endUI;

    [Header("UI Elements")]
    [SerializeField] private TextMeshProUGUI p1Text;
    [SerializeField] private TextMeshProUGUI p2Text;
    [SerializeField] private GameObject p1Turn;
    [SerializeField] private GameObject p2Turn;
    [SerializeField] private Sprite p1Sprite;
    [SerializeField] private Sprite p2Sprite;
    [SerializeField] private Sprite drawSprite;
    [SerializeField] private Image endImage;
    [SerializeField] private TextMeshProUGUI endText;
    [SerializeField] private Image mainBackground;
    [SerializeField] private Image gameBackground;
    [SerializeField] private RawImage cameraImage;

    private WebCamTexture webcam;

    private bool currentPlayerIsX = true;
    private string[] gameBoard = new string[9];
    private int xNumberWins;
    private int oNumberWins;
    private int roundCount;
    private bool isCameraOn = false;

    void Start()
    {
        WebSocketServerManager.Instance.OnVoiceTextChange += WSManager_OnVoiceTextChange;

        webcam = new WebCamTexture();
        cameraImage.texture = webcam;
        isCameraOn = false;

        xNumberWins = 0;
        oNumberWins = 0;
        roundCount = 0;

        endUI.SetActive(false);
        gameUI.SetActive(false);
        mainMenuUI.gameObject.SetActive(true);

        InitializeButtons();
        ResetBoard();
    }

    private void WSManager_OnVoiceTextChange(object sender, System.EventArgs e)
    {
        AssignVoiceToUi();
    }

    private void AssignVoiceToUi()
    {
        string voiceText = WebSocketServerManager.Instance.GetCurrentVoiceText();

        if (!voiceText.IsNullOrEmpty())
        {
            if (endUI.activeSelf)
            {
                EndUiVoiceHandler(voiceText);
            }
            else if (gameUI.activeSelf)
            {
                GameUiVoiceHandler(voiceText);
            }
            else if (mainMenuUI.activeSelf)
            {
                Debug.Log("nao esta ativo?: ");
                MainMenuUiVoiceHandler(voiceText);
            }
        }
        return;
    }

    private void EndUiVoiceHandler(string voiceText)
    {
        // In the endUI we have two buttons, one to continue playing, one for exiting
        if (ContainsIgnoreCase(voiceText, "continue game") || ContainsIgnoreCase(voiceText, "play again"))
        {
            Transform playAgainButtonTransform = endUI.transform.Find("PlayAgainBtn");
            if (playAgainButtonTransform != null)
            {
                Button playBtn = playAgainButtonTransform.gameObject.GetComponent<Button>();
                if (playBtn != null)
                {
                    playBtn.onClick.Invoke();
                }
            }
        }
        else if (ContainsIgnoreCase(voiceText, "exit"))
        {
            Transform exitButtonTransform = mainMenuUI.transform.Find("ExitBtn");
            if (exitButtonTransform != null)
            {
                Button exitBtn = exitButtonTransform.gameObject.GetComponent<Button>();
                if (exitBtn != null)
                {
                    exitBtn.onClick.Invoke();
                }
            }
        }
    }

    private void GameUiVoiceHandler(string voiceText)
    {
        // In the gameUI we have 9 buttons, one for each block of the grid

        string gridPos = "";

        if (ContainsIgnoreCase(voiceText, "A1") || ContainsIgnoreCase(voiceText, "Hay one"))
        {
            gridPos = "A1";
        }
        else if (ContainsIgnoreCase(voiceText, "B1") || ContainsIgnoreCase(voiceText, "Be one"))
        {
            gridPos = "B1";
        }
        else if (ContainsIgnoreCase(voiceText, "C1") || ContainsIgnoreCase(voiceText, "See one"))
        {
            gridPos = "C1";
        }
        else if (ContainsIgnoreCase(voiceText, "A2") || ContainsIgnoreCase(voiceText, "Hay two"))
        {
            gridPos = "A2";
        }
        else if (ContainsIgnoreCase(voiceText, "B2") || ContainsIgnoreCase(voiceText, "Be two"))
        {
            gridPos = "B2";
        }
        else if (ContainsIgnoreCase(voiceText, "C2") || ContainsIgnoreCase(voiceText, "See three"))
        {
            gridPos = "C2";
        }
        else if (ContainsIgnoreCase(voiceText, "A3") || ContainsIgnoreCase(voiceText, "Hay three"))
        {
            gridPos = "A3";
        }
        else if (ContainsIgnoreCase(voiceText, "B3") || ContainsIgnoreCase(voiceText, "Be three"))
        {
            gridPos = "B3";
        }
        else if (ContainsIgnoreCase(voiceText, "C3") || ContainsIgnoreCase(voiceText, "See three"))
        {
            gridPos = "C3";
        }
        else return;

        if (!gridPos.IsNullOrEmpty())
        {
            Transform playSquareButtonTransform = endUI.transform.Find(gridPos);
            if (playSquareButtonTransform != null)
            {
                Button playBtn = playSquareButtonTransform.gameObject.GetComponent<Button>();
                if (playBtn != null)
                {
                    playBtn.onClick.Invoke();
                }
            }
        }
    }

    public void ToggleCameraOnBackground()
    {
        if (isCameraOn)
        {
            mainBackground.sprite = cleanMainBackground;
            gameBackground.sprite = cleanGameBackground;

            isCameraOn = false;

            webcam.Stop();
        } 
        else
        {
            mainBackground.sprite = cameraMainBackground;
            gameBackground.sprite = cameraGameBackground;

            isCameraOn = true;

            webcam.Play();
        }
  
    }

    private void MainMenuUiVoiceHandler(string voiceText)
    {
        // In the mainMenuUI we have three buttons, one to play, one for exiting, and a toggle
        if (ContainsIgnoreCase(voiceText, "play game") || ContainsIgnoreCase(voiceText, "play the game"))
        {
            Transform playButtonTransform = mainMenuUI.transform.Find("Buttons/PlayBtn");
            if (playButtonTransform != null)
            {
                Button playBtn = playButtonTransform.gameObject.GetComponent<Button>();
                if (playBtn != null)
                {
                    playBtn.onClick.Invoke();
                }
            }
        }
        else if (ContainsIgnoreCase(voiceText, "exit"))
        {
            Transform exitButtonTransform = mainMenuUI.transform.Find("Buttons/ExitBtn");
            if (exitButtonTransform != null)
            {
                Button exitBtn = exitButtonTransform.gameObject.GetComponent<Button>();
                if (exitBtn != null)
                {
                    exitBtn.onClick.Invoke();
                }
            }
        }
    }

    bool ContainsIgnoreCase(string source, string target)
    {
        return source.IndexOf(target, System.StringComparison.OrdinalIgnoreCase) >= 0;
    }

    private void InitializeButtons()
    {
        for (int i = 0; i < gameButtons.Length; i++)
        {
            int index = i;
            gameButtons[i].gameObject.GetComponent<Image>().sprite = emptySprite;
            gameButtons[i].onClick.AddListener(() => ButtonGridClick(index));
            gameButtons[i].enabled = true;
        }
    }

    void ResetButtons()
    {
        for (int i = 0; i < gameButtons.Length; i++)
        {
            int index = i;
            gameButtons[i].gameObject.GetComponent<Image>().sprite = emptySprite;
            gameButtons[i].enabled = true;
        }
    }

    private void ResetBoard()
    {
        for (int i = 0; i < gameBoard.Length; i++)
        {
            gameBoard[i] = "";
        }
        currentPlayerIsX = true;

        roundCount = 0;

        p1Turn.SetActive(true);
        p2Turn.SetActive(false);
    }

    public void ButtonGridClick(int index)
    {
        // Set button sprite depending on the player
        if (currentPlayerIsX)
        {
            gameButtons[index].gameObject.GetComponent<Image>().sprite = xSprite;

            // Change the values of the board according to the player
            gameBoard[index] = "x";
        }
        else
        {
            gameButtons[index].gameObject.GetComponent<Image>().sprite = oSprite;

            gameBoard[index] = "o";
        }

        // Deactivate Button without the disabled color
        gameButtons[index].enabled = false;

        // Check for Win
        CheckForWin();

        // Check for game ending in a draw
        if (roundCount >= 8)
        {
            EndInDraw();
        }
        roundCount++;

        // Change player turn
        currentPlayerIsX = !currentPlayerIsX;
        p1Turn.SetActive(!p1Turn.activeInHierarchy);
        p2Turn.SetActive(!p2Turn.activeInHierarchy);
    }

    private void CheckForWin()
    {
        // Check rows
        for (int i = 0; i < 9; i += 3)
        {
            if (gameBoard[i] != "" && gameBoard[i] == gameBoard[i + 1] && gameBoard[i] == gameBoard[i + 2])
            {
                ShowWinner();
            }
        }

        // Check columns
        for (int i = 0; i < 3; i++)
        {
            if (gameBoard[i] != "" && gameBoard[i] == gameBoard[i + 3] && gameBoard[i] == gameBoard[i + 6])
            {
                ShowWinner();
            }
        }

        // Check diagonals
        if (gameBoard[0] != "" && gameBoard[0] == gameBoard[4] && gameBoard[0] == gameBoard[8])
        {
            ShowWinner();
        }
        if (gameBoard[2] != "" && gameBoard[2] == gameBoard[4] && gameBoard[2] == gameBoard[6])
        {
            ShowWinner();
        }

        return;
    }

    private void ShowWinner()
    {
        if (currentPlayerIsX)
        {
            xNumberWins++;
            p1Text.text = "Number of wins: " + xNumberWins;
            endImage.sprite = p1Sprite;
        } 
        else 
        {
            oNumberWins++;
            p2Text.text = "Number of wins: " + oNumberWins;
            endImage.sprite = p2Sprite;
        }

        endText.text = "IS THE WINNER!";

        endUI.SetActive(true);
    }

    private void EndInDraw()
    {
        endImage.sprite = drawSprite;

        endText.text = "IT'S A DRAW!";

        endUI.SetActive(true);
    }

    public void ContinuePlayButton()
    {
        ResetButtons();
        ResetBoard();

        endUI.SetActive(false);
    }

    public void ExitButton()
    {
        ResetButtons();
        ResetBoard();

        mainMenuUI.gameObject.SetActive(true);
        gameUI.SetActive(false);
        endUI.SetActive(false);
    }

    // Unsubscribe from the events we subbed to in Start()
    //
    private void OnDestroy()
    {
        WebSocketServerManager.Instance.OnVoiceTextChange += WSManager_OnVoiceTextChange;
    }
}
