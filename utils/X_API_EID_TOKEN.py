import time, requests, sys, re, threading, os, json, random, uuid
from urllib.parse import unquote_plus, quote

def getUUID(x="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", t=0):
    if isinstance(x, int):
        x = "x" * x
    uuid = re.sub("[xy]", lambda x: str(int((16 * random.random()) // 1) if x.group() == "x" else ((3 & int(x.group(), 16)) | 8)), x)
    return uuid

def getTimestamp():
    return int(round(time.time() * 1000))
def TDEncrypt(m):
    m = json.dumps(m, separators=(',', ':'))
    m = quote(m)
    n = ""
    g = 0
    s64 = "23IL<N01c7KvwZO56RSTAfghiFyzWJqVabGH4PQdopUrsCuX*xeBjkltDEmn89.-"
    m_l = len(m)
    while g < m_l:
        f = ord(m[g])
        g += 1
        d = ord(m[g]) if g < m_l else 0
        g += 1
        a = ord(m[g]) if g < m_l else 0
        g += 1
        b = f >> 2
        f = (f & 3) << 4 | d >> 4
        e = (d & 15) << 2 | a >> 6
        c = a & 63
        if d == 0:
            e = c = 64
        elif a == 0:
            c = 64

        if b < 64: n += s64[b]
        if f < 64: n += s64[f]
        if e < 64: n += s64[e]
        if c < 64: n += s64[c]
    return n + "/"

def x_api_eid_token(ua, cookie):
    t = getTimestamp()
    g = {
        'pin': '',
        'oid': '',
        'bizId': 'jd-babelh5',
        'fc': '',
        'mode': 'strict',
        'p': 's',
        'fp': '26402d879256c911a19f750ac9e6137b',
        'ctype': 1,
        'v': '3.1.1.1',
        'f': '3',
        'o': 'pro.m.jd.com/jdlite/active/23CeE8ZXA4uFS9M9mTjtta9T4S5x/index.html',
        # 'qs': 'babelChannel=ttt6&lng=104.624159&lat=28.765053&sid=aa6042f7bd594f9ef8c2bc549246161w&un_area=22_2005_36315_57211',
        # 'jsTk': '',
        'qi': ''
    }
    a = TDEncrypt(g)
    d = '{"ts":{"deviceTime":1684749932883,"deviceEndTime":1684749932968},"ca":{"tdHash":"ae7bb88f7eac3baa052a6d2fd3c4eab8","contextName":"webgl,experimental-webgl","webglversion":"WebGL 1.0 (OpenGL ES 2.0 Chromium)","shadingLV":"WebGL GLSL ES 1.0 (OpenGL ES GLSL ES 1.0 Chromium)","vendor":"WebKit","renderer":"WebKit WebGL","extensions":["ANGLE_instanced_arrays","EXT_blend_minmax","EXT_color_buffer_half_float","EXT_float_blend","EXT_texture_filter_anisotropic","WEBKIT_EXT_texture_filter_anisotropic","EXT_sRGB","OES_element_index_uint","OES_fbo_render_mipmap","OES_standard_derivatives","OES_texture_float","OES_texture_float_linear","OES_texture_half_float","OES_texture_half_float_linear","OES_vertex_array_object","WEBGL_color_buffer_float","WEBGL_compressed_texture_astc","WEBGL_compressed_texture_etc","WEBGL_compressed_texture_etc1","WEBGL_debug_renderer_info","WEBGL_debug_shaders","WEBGL_depth_texture","WEBKIT_WEBGL_depth_texture","WEBGL_lose_context","WEBKIT_WEBGL_lose_context","WEBGL_multi_draw"],"wuv":"Qualcomm","wur":"Adreno (TM) 730"},"m":{"compatMode":"CSS1Compat"},"fo":["Bauhaus 93","Casual"],"n":{"vendorSub":"","productSub":"20030107","vendor":"Google Inc.","maxTouchPoints":5,"hardwareConcurrency":8,"cookieEnabled":true,"appCodeName":"Mozilla","appName":"Netscape","appVersion":"","platform":"Linux aarch64","product":"Gecko","userAgent":"","language":"zh-CN","onLine":true,"webdriver":false,"javaEnabled":false,"deviceMemory":8,"enumerationOrder":["vendorSub","productSub","vendor","maxTouchPoints","userActivation","doNotTrack","geolocation","connection","plugins","mimeTypes","webkitTemporaryStorage","webkitPersistentStorage","hardwareConcurrency","cookieEnabled","appCodeName","appName","appVersion","platform","product","userAgent","language","languages","onLine","webdriver","getBattery","getGamepads","javaEnabled","sendBeacon","vibrate","scheduling","mediaCapabilities","locks","wakeLock","usb","clipboard","credentials","keyboard","mediaDevices","storage","serviceWorker","deviceMemory","bluetooth","getUserMedia","requestMIDIAccess","requestMediaKeySystemAccess","webkitGetUserMedia","clearAppBadge","setAppBadge"]},"p":[],"w":{"devicePixelRatio":3,"screenTop":0,"screenLeft":0},"s":{"availHeight":904,"availWidth":407,"colorDepth":24,"height":904,"width":407,"pixelDepth":24},"sc":{"ActiveBorder":"rgb(255, 255, 255)","ActiveCaption":"rgb(204, 204, 204)","AppWorkspace":"rgb(255, 255, 255)","Background":"rgb(99, 99, 206)","ButtonFace":"rgb(221, 221, 221)","ButtonHighlight":"rgb(221, 221, 221)","ButtonShadow":"rgb(136, 136, 136)","ButtonText":"rgb(0, 0, 0)","CaptionText":"rgb(0, 0, 0)","GrayText":"rgb(128, 128, 128)","Highlight":"rgb(181, 213, 255)","HighlightText":"rgb(0, 0, 0)","InactiveBorder":"rgb(255, 255, 255)","InactiveCaption":"rgb(255, 255, 255)","InactiveCaptionText":"rgb(127, 127, 127)","InfoBackground":"rgb(251, 252, 197)","InfoText":"rgb(0, 0, 0)","Menu":"rgb(247, 247, 247)","MenuText":"rgb(0, 0, 0)","Scrollbar":"rgb(255, 255, 255)","ThreeDDarkShadow":"rgb(102, 102, 102)","ThreeDFace":"rgb(192, 192, 192)","ThreeDHighlight":"rgb(221, 221, 221)","ThreeDLightShadow":"rgb(192, 192, 192)","ThreeDShadow":"rgb(136, 136, 136)","Window":"rgb(255, 255, 255)","WindowFrame":"rgb(204, 204, 204)","WindowText":"rgb(0, 0, 0)"},"ss":{"cookie":true,"localStorage":true,"sessionStorage":true,"globalStorage":false,"indexedDB":true},"tz":-480,"lil":"","wil":""}'
    d = json.loads(d)
    d["ts"]["deviceTime"] = t
    d["ts"]["deviceEndTime"] = t + 77
    d["n"]["appVersion"] = ua[ua.find("appBuild/") + 9:]
    d["n"]["userAgent"] = ua
    d = TDEncrypt(d)
    data = {"d": d}
    url = f'https://gia.jd.com/jsTk.do?a={a}'
    headers = {
        "Host": "gia.jd.com",
        "User-Agent": ua,
        "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Accept": "*/*",
        "Origin": "https://pro.m.jd.com",
        "X-Requested-With": "com.jd.jdlite",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://pro.m.jd.com/jdlite/active/23CeE8ZXA4uFS9M9mTjtta9T4S5x/index.html?babelChannel=ttt6",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": cookie + ";cid=8"
    }
    x_api_eid_token = ""
    try:
        res = requests.post(url=url, data=data, headers=headers, proxies={}, timeout=2).text
        try:
            res = json.loads(res)
            if res['code'] == 0:  # res.data
                x_api_eid_token = res['data']['token']
            else:
                print(f"{res}")
        except Exception as e:
            print(f"x_api_eid_token异常：{str(e)}")
    except Exception as e:
        print(f"x_api_eid_token异常：{str(e)}")
    return x_api_eid_token
