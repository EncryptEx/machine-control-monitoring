using System;
using System.Collections;
using System.Collections.Generic;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;


public enum Requests
{
    powerOn,
    powerOff,
    changeVelocity,
    readall,
}

public static class Networking
{
    public const string raspi_base = "http://10.0.4.60:8000";
    public const string chat_base = "http://10.0.4.43:8000/chatbot";

    private static Dictionary<Requests, string> requestUrl = new Dictionary<Requests, string>()
    {
        { Requests.powerOn, raspi_base + "/motors/enable" },
        { Requests.powerOff, raspi_base + "/motors/disable" },
        { Requests.changeVelocity, raspi_base + "/motors/enable/" },
        { Requests.readall, raspi_base + "/read/all" },
    };

    private static readonly HttpClient client = new HttpClient();

    public static async Task<string> SendGetRequest(string url)
    {
        string ret;
        ret = await client.GetStringAsync(url);

        return ret;
    }

    public static async Task<string> SendGetRequest(Requests request, string data = "")
    {
        string ret;
        ret = await SendGetRequest(requestUrl[request] + data);

        return ret;
    }

    public static async Task<HttpResponseMessage> SendPostRequest(string url, string jsonData)
    {
        var content = new StringContent(jsonData, Encoding.UTF8, "application/json");
        var ret = await client.PostAsync(url, content);

        return ret;
    }
}
