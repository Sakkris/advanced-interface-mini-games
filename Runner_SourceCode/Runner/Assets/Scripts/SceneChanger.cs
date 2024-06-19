using UnityEngine;
using UnityEngine.SceneManagement;

public class SceneChanger : MonoBehaviour
{
    [Tooltip("Name of the scene to load")]
    public string targetScene;

    // Call this method to change the scene
    public void ChangeScene()
    {
        if (!string.IsNullOrEmpty(targetScene))
        {
            SceneManager.LoadScene(targetScene);
        }
        else
        {
            Debug.LogError("Target scene name is not set.");
        }
    }
}
