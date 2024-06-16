using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class Loader
{
    public enum Scene
    {
        MainMenuScene,
        GameScene,
        LoadingScene
    }

    private static Scene targetScene;

    public static void Load(string scene)
    {
        if (scene != null && scene != "")
        {
            Scene targetScene = (Scene)Enum.Parse(typeof(Scene), scene);
            Load(targetScene);
        }
    }

    public static void Load(Scene targetScene)
    {
        // Load the scene we want to access
        Loader.targetScene = targetScene;

        // While the target Scene is Loading, show LoadingScene
        SceneManager.LoadScene(Scene.LoadingScene.ToString());
    }

    public static void LoaderCallback()
    {
        SceneManager.LoadScene(targetScene.ToString());
    }
}
