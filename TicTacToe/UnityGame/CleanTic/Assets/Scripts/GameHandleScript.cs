using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

public class GameHandleScript : MonoBehaviour
{
    [Header("Sprites")]
    [SerializeField] private Sprite xSprite;
    [SerializeField] private Sprite oSprite;
    [SerializeField] private Sprite emptySprite;

    [Header("Buttons")]
    [SerializeField] private Button[] buttons;

    [Header("UI Elements")]
    [SerializeField] private GameObject endUI;
    [SerializeField] private GameObject mainMenuUI;
    [SerializeField] private GameObject GameUI;

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

    private bool currentPlayerIsX = true;
    private string[] gameBoard = new string[9];
    private int xNumberWins;
    private int oNumberWins;
    private int roundCount;

    void Start()
    {
        xNumberWins = 0;
        oNumberWins = 0;
        roundCount = 0;

        endUI.SetActive(false);

        InitializeButtons();
        ResetBoard();
    }

    private void InitializeButtons()
    {
        for (int i = 0; i < buttons.Length; i++)
        {
            int index = i;
            buttons[i].gameObject.GetComponent<Image>().sprite = emptySprite;
            buttons[i].onClick.AddListener(() => ButtonGridClick(index));
            buttons[i].enabled = true;
        }
    }

    void ResetButtons()
    {
        for (int i = 0; i < buttons.Length; i++)
        {
            int index = i;
            buttons[i].gameObject.GetComponent<Image>().sprite = emptySprite;
            buttons[i].enabled = true;
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
            buttons[index].gameObject.GetComponent<Image>().sprite = xSprite;

            // Change the values of the board according to the player
            gameBoard[index] = "x";
        }
        else
        {
            buttons[index].gameObject.GetComponent<Image>().sprite = oSprite;

            gameBoard[index] = "o";
        }

        // Deactivate Button without the disabled color
        buttons[index].enabled = false;

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

        mainMenuUI.SetActive(true);
        GameUI.SetActive(false);
        endUI.SetActive(false);
    }
}
