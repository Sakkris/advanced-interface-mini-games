using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SectionTrigger : MonoBehaviour
{
    public GameObject[] roadSections;  // Array to hold different road sections

    private bool hasTriggered = false;  // Flag to track if the trigger has already been activated

    private int currentIndex = 0;

    private void OnTriggerEnter(Collider other)
    {
        if (other.gameObject.CompareTag("Trigger") && !hasTriggered)
        {
            // Instantiate the selected road section at the calculated position
            Instantiate(roadSections[currentIndex], new Vector3(-3.459214f-0.249607f-0.036538815f-2, 0,0), Quaternion.identity);

            // Update the index to alternate between sections
            currentIndex = (currentIndex + 1) % roadSections.Length;

            hasTriggered = true;

            // Start a coroutine to reset hasTriggered after 1 second
            StartCoroutine(ResetTrigger());
        }
    }

    IEnumerator ResetTrigger()
    {
        // Wait for 1 second
        yield return new WaitForSeconds(1f);

        // Reset hasTriggered to false
        hasTriggered = false;
    }
}
