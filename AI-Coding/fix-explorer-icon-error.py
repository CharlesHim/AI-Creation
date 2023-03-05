import os
import ctypes
import subprocess


def clear_thumbcache():

    appdata = os.getenv("LOCALAPPDATA")
    thumbcache_path = os.path.join(appdata, "Microsoft", "Windows", "Explorer")
    
    for file in os.listdir(thumbcache_path):
        
        if file.startswith("thumbcache"):

            file_path = os.path.join(thumbcache_path, file)

            try:
                os.remove(file_path)
                print(f"已删除{file}")
                
            except Exception as e:
                print(f"删除文件{file}失败，原因是{e}")

##这个版本的代码无法正常工作，于是让ai改了一版
##def restart_explorer():
##
##    explorer_handle = ctypes.windll.kernel32.OpenProcess(1, False, ctypes.windll.kernel32.GetCurrentProcessId())
##
##    try:
##        ctypes.windll.kernel32.TerminateProcess(explorer_handle, 0)
##        print("已结束资源管理器进程")
##
##    except Exception as e:
##        print(f"结束资源管理器进程失败，原因是{e}")
##
##    finally:
##        ctypes.windll.kernel32.CloseHandle(explorer_handle)
##
##    try:
##        os.startfile("explorer.exe")
##        print("已重启资源管理器进程")
##
##    except Exception as e:
##        print(f"重启资源管理器进程失败，原因是{e}")


##新代码如下
##import ctypes
##import os
##import subprocess

def restart_explorer():

    # 枚举所有进程的ID
    process_ids = (ctypes.c_ulong * 1024)()
    size = ctypes.sizeof(process_ids)
    count = ctypes.c_ulong()
    ctypes.windll.psapi.EnumProcesses(ctypes.byref(process_ids), size, ctypes.byref(count))

    # 找到资源管理器的ID和名称
    explorer_id = None
    explorer_name = "explorer.exe"
    for i in range(int(count.value / ctypes.sizeof(ctypes.c_ulong))):
        process_id = process_ids[i]
        if process_id:
            handle = ctypes.windll.kernel32.OpenProcess(0x1000, False, process_id)
            if handle:
                name_buffer = ctypes.create_unicode_buffer(1024)
                length = ctypes.c_ulong()
                if ctypes.windll.psapi.GetProcessImageFileNameW(handle, name_buffer, ctypes.byref(length)):
                    name = name_buffer.value
                    if name.endswith(explorer_name):
                        explorer_id = process_id
                        break
                ctypes.windll.kernel32.CloseHandle(handle)

    # 结束资源管理器进程
    if explorer_id:
        handle = ctypes.windll.kernel32.OpenProcess(1, False, explorer_id)
        try:
            ctypes.windll.kernel32.TerminateProcess(handle, 0)
            print("已结束资源管理器进程")
        except Exception as e:
            print(f"结束资源管理器进程失败，原因是{e}")
        finally:
            ctypes.windll.kernel32.CloseHandle(handle)

    # 重启资源管理器进程
    try:
        subprocess.Popen("explorer.exe")
        print("已重启资源管理器进程")
    except Exception as e:
        print(f"重启资源管理器进程失败，原因是{e}")


clear_thumbcache()
restart_explorer()
        





























            
