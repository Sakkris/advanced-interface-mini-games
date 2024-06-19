using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.Windows.Speech;

public class PlayerMove : MonoBehaviour
{
    public CharacterController player;
    public Transform playerTransform;
    private float moveDistance = 0.23f; // Fixed distance to move left or right
    private float smoothTime = 0.1f;    // Smooth time for lerp
    private float jumpHeight = 0.15f;   // Height of the jump

    private bool isJumping = false;
    private float verticalSpeed = 0f;
    private float targetZPosition = 0f;  // Target Z position for smooth movement
    private float initialYPosition;      // Initial y position of the player

    private KeywordRecognizer keywordRecognizer;
    private Dictionary<string, Action> actions = new Dictionary<string, Action>();

    public Animator m_Animator;

    private void Start()
    {
        player = GetComponent<CharacterController>();
        playerTransform = transform; // Using transform directly since it's attached to the same GameObject
        initialYPosition = playerTransform.localPosition.y; // Store the initial y position

        actions.Add("left", Left);
        actions.Add("right", Right);
        actions.Add("jump", Jump);

        keywordRecognizer = new KeywordRecognizer(actions.Keys.ToArray());
        keywordRecognizer.OnPhraseRecognized += RecognizedSpeech;
        keywordRecognizer.Start();
    }

    private void RecognizedSpeech(PhraseRecognizedEventArgs speech)
    {
        Debug.Log(speech.text);
        actions[speech.text].Invoke();
    }

    private void Left()
    {
        targetZPosition = Mathf.Clamp(targetZPosition - moveDistance, -moveDistance, moveDistance);
    }

    private void Right()
    {
        targetZPosition = Mathf.Clamp(targetZPosition + moveDistance, -moveDistance, moveDistance);
    }

    private void Jump()
    {
        if (!isJumping)
        {
            isJumping = true;
            verticalSpeed = CalculateJumpSpeed(jumpHeight);
            m_Animator.SetTrigger("Jump");
        }
    }

    void Update()
    {
        // Smoothly move player towards the target position
        Vector3 currentPosition = playerTransform.localPosition;
        Vector3 newPosition = new Vector3(currentPosition.x, currentPosition.y, targetZPosition);
        playerTransform.localPosition = Vector3.Lerp(currentPosition, newPosition, smoothTime);
        
        if (isJumping)
        {
            verticalSpeed += Physics.gravity.y * 0.5f * Time.deltaTime;
            Vector3 verticalMovement = new Vector3(0, verticalSpeed, 0) * Time.deltaTime;
            player.Move(verticalMovement);

            // Check if the player has landed
            if (player.isGrounded && verticalSpeed < 0)
            {
                isJumping = false;
                verticalSpeed = 0f;
                // Reset the y position to the initial value to ensure the player is grounded correctly
                Vector3 groundedPosition = playerTransform.localPosition;
                groundedPosition.y = initialYPosition;
                playerTransform.localPosition = groundedPosition;
                m_Animator.ResetTrigger("Jump");
            }
        }
    }

    float CalculateJumpSpeed(float jumpHeight)
    {
        // Calculate the initial upward speed required to achieve the desired jump height
        return Mathf.Sqrt(2 * Mathf.Abs(Physics.gravity.y) * jumpHeight);
    }
}
