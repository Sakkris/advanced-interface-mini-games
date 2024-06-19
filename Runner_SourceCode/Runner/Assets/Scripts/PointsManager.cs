using TMPro;
using UnityEngine;

public class PointsManager : MonoBehaviour
{
    public static PointsManager instance;
    public TMP_Text pointsText;
    public TMP_Text recordPointsText;
    private int points = 0;
    private int recordPoints = 0;

    void Start()
    {

        // Load points from PlayerPrefs
        points = PlayerPrefs.GetInt("Points", 0);
        pointsText.text = points.ToString();

        // Load record points from PlayerPrefs
        recordPoints = PlayerPrefs.GetInt("RecordPoints", 0);
        recordPointsText.text = recordPoints.ToString();
    }

    void Awake()
    {
        if (instance == null)
        {
            instance = this;
        }
        else
        {
            Destroy(gameObject);
        }
    }

    public void AddPoints()
    {
        points += 1;
        PlayerPrefs.SetInt("Points", points);
        PlayerPrefs.Save();
        pointsText.text = points.ToString();

        if (points > recordPoints)
        {
            recordPoints = points;
            recordPointsText.text = recordPoints.ToString();
            // Save record points to PlayerPrefs
            PlayerPrefs.SetInt("RecordPoints", recordPoints);
            PlayerPrefs.Save();
        }
    }
}
