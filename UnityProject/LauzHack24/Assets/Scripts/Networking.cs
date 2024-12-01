using System;
using System.Collections;
using System.Collections.Generic;
using System.Net.Http;
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
    const string base_url = "http://10.0.4.60:8000";

    private static Dictionary<Requests, string> requestUrl = new Dictionary<Requests, string>()
    {
        { Requests.powerOn, base_url + "/motors/enable" },
        { Requests.powerOff, base_url + "/motors/disable" },
        { Requests.changeVelocity, base_url + "/motors/enable/" },
        { Requests.readall, base_url + "/read/all" },
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
}
