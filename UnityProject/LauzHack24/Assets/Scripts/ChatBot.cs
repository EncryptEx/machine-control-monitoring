using System.Collections;
using System.Collections.Generic;
using System.Threading.Tasks;
using TMPro;
using Unity.VisualScripting;
using UnityEngine;
using UnityEngine.UI;
using System.Net.Http;
using System;
using System.Text.RegularExpressions;
using System.Linq;

public class ChatBot : MonoBehaviour
{
    [SerializeField]
    GameObject bobTextPrefab, meTextPrefab;

    [SerializeField]
    Transform content;

    [SerializeField]
    ScrollRect scrollRect;

    [SerializeField]
    TMP_InputField inputField;
    [SerializeField]
    TextMeshProUGUI placeHolder;

    [SerializeField]
    GameObject LoadingObj;
    [SerializeField]
    Button SubmitBtt;

    bool thinking = false;

    string lastResponse = "";

    struct ChatResponse
    {
        public string answer;
        public int action;
        public string parameter;
    }

    private void Update()
    {
        if (inputField.text.Length < 3 || thinking)
            SubmitBtt.enabled = false;
        else
            SubmitBtt.enabled = true;
    }

    async void InsertNewText(bool isBob, string txt)
    {
        GameObject inst = Instantiate(isBob ? bobTextPrefab : meTextPrefab, content);
        ChatText text = inst.GetComponent<ChatText>();
        text.SetText(txt);

        await Task.Delay(10);
        scrollRect.verticalNormalizedPosition = 0f;
    }

    public async void SendPrompt()
    {
        string prompt = inputField.text;
        prompt = prompt.Replace("\n", " ");
        inputField.text = "";

        InsertNewText(false, prompt);
        LoadingObj.SetActive(true);
        inputField.enabled = false;
        placeHolder.text = "";
        thinking = true;

        //Send prompt
        var jsonData = $"{{ \"user_input\": \"{prompt}\", \"sensors_info\": {DataReciever.current.lastJsonData}}}";
        HttpResponseMessage response = await Networking.SendPostRequest(Networking.chat_base, jsonData);

        // Response got

        LoadingObj.SetActive(false);
        inputField.enabled = true;
        thinking = false;

        if (response.IsSuccessStatusCode)
        {
            // Get the response body as a string
            string responseBody = await response.Content.ReadAsStringAsync();

            // Deserialize the JSON response into an object
            var responseObject = JsonUtility.FromJson<ChatResponse>(responseBody);

            switch (responseObject.action)
            {
                case 1:
                    if (EngineControl.current.velocity == 0)
                        EngineControl.current.velocitySlider.value = 5;
                    EngineControl.current.powerToggle._ToggleToValue(true);
                    break;
                case 2:
                    EngineControl.current.powerToggle._ToggleToValue(false);
                    break;
                case 3:
                    if (responseObject.parameter.ToUpper().Contains("B"))
                        EngineControl.current.reverseToggle._ToggleToValue(true);
                    else if (responseObject.parameter.ToUpper().Contains("F"))
                        EngineControl.current.reverseToggle._ToggleToValue(false);
                    break;
                case 4:
                    EngineControl.current.velocitySlider.value = int.Parse(responseObject.parameter);
                    break;
                default:
                    print("action was null");
                    break;
            }

            InsertNewText(true, responseObject.answer);
            lastResponse = responseObject.answer;
        }
        else
        {
            print("Request failed: " + response.StatusCode);
        }

        
    }
}
