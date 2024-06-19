using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PointsTrigger : MonoBehaviour
{
    public PointsManager pointsManager;
    public AudioSource coinCollectSound;
    private bool canAddPoints = true;  // Flag to prevent multiple triggers

    private void OnTriggerEnter(Collider other)
    {
        if (other.gameObject.CompareTag("Coin") && canAddPoints)
        {
            coinCollectSound.Play();   // Play the coin collection sound
            pointsManager.AddPoints();
            Destroy(other.gameObject);
            StartCoroutine(ResetCanAddPoints());
        }
    }

    private IEnumerator ResetCanAddPoints()
    {
        canAddPoints = false;
        yield return new WaitForSeconds(0.1f);  // Adjust the delay as needed
        canAddPoints = true;
    }
}
