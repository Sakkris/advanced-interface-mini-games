using TMPro;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;

public class HubManager : MonoBehaviour
{
    [SerializeField] TextMeshProUGUI[] btnText;
    public TextMeshProUGUI[] BtnText { get {  return btnText; } }

    [SerializeField] string[] btnTitles;
    public string[] BtnTitles { get { return btnTitles; } }

    [SerializeField] TextMeshProUGUI title;
    public TextMeshProUGUI Title { get { return title; } }

    [SerializeField] string[] descriptions;
    public string[] Descriptions { get { return descriptions; } }

    [SerializeField] TextMeshProUGUI descriptionBox;
    public TextMeshProUGUI DescriptionBox { get { return descriptionBox; } }

    private int activeButtonIndex = -1;

    void Update()
    {
        CheckEvents();
    }

    void CheckEvents()
    {
        if (Input.GetKeyDown(KeyCode.Space))
            UpdateActiveButton(activeButtonIndex);
        
        if (Input.GetKeyDown(KeyCode.W))
        {
            if (activeButtonIndex <= 0)
                UpdateActiveButton(btnTitles.Length - 1);
            else
                UpdateActiveButton(activeButtonIndex - 1);
        }

        if (Input.GetKeyDown(KeyCode.S))
        {
            if (activeButtonIndex == btnTitles.Length - 1)
                UpdateActiveButton(0);
            else
                UpdateActiveButton(activeButtonIndex + 1);
        }
            
    }

    // switch to the game execution
    void StartGame()
    {
        switch (activeButtonIndex)
        {
            case 0:
                // exec tic-tac-toe
                break;
            case 1:
                // exec pong
                break;
            case 2:
                // exec 3rd game
                break;
        }

    }

    public void UpdateActiveButton(int index)
    {
        // in case anything goes wrong
        if (index >= btnTitles.Length || index < 0)
            return;
        
        if (index == activeButtonIndex)
        {
            StartGame();
            return;
        }

        if (activeButtonIndex != -1) 
            btnText[activeButtonIndex].color = Color.gray;

        activeButtonIndex = index;
        btnText[activeButtonIndex].color = Color.white;
        DescriptionBox.text = descriptions[activeButtonIndex];
        title.text = btnTitles[activeButtonIndex];
    }
}
